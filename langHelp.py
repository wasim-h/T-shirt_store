import re
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_huggingface import HuggingFaceEmbeddings  
from langchain_chroma import Chroma  
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from few_shots import few_shots

llm = ChatOllama(
    model="gemma2:2b",
    temperature=0,
    num_predict=128  
)

class CleanSQLDatabase(SQLDatabase):
    def run(self, command, fetch="all", include_columns=False, **kwargs):
        """Execute SQL command after cleaning it"""
        if isinstance(command, str):
            command = clean_sql_query(command)
        return super().run(command, fetch, include_columns, **kwargs)

def clean_sql_query(query):
    """Extract and clean SQL query from LLM output"""
    query = re.sub(r'```sql\s*', '', query)
    query = re.sub(r'```\s*', '', query)
    
    if ';' in query:
        query = query.split(';')[0] + ';'
    
    query = re.sub(r'SQLResult:.*', '', query, flags=re.DOTALL)
    query = re.sub(r'Answer:.*', '', query, flags=re.DOTALL)
    
    return query.strip()

def get_few_shot_db_chain():
    print("--- LOADING MODELS AND CREATING CHAIN ---")
    db_user = 'root'
    db_password = '2363' 
    db_host = 'localhost'
    db_name = 'tshirt_store'

    db = CleanSQLDatabase.from_uri(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}", 
        sample_rows_in_table_info=3
    )

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=4,
    )
    
    mysql_prompt = """You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run.
IMPORTANT RULES:
1. Output ONLY the SQL query. No markdown, no explanations.
2. Unless specified, use LIMIT {top_k}.
3. When asked for "how many items" or "stock", use SUM(stock_quantity).
4. When asked for "how many types" or "varieties", use COUNT(*).
5. CRITICAL: When asked for "total value", "total price", or "revenue", you MUST calculate SUM(price * stock_quantity). Never select just the price column.
6. FILTER RULES: Do not filter by brand, size, or color unless the user explicitly asks for it in the question.
7. SELECTION RULES: When asked "what is" or "which is" (e.g., "most expensive", "top selling"), you must SELECT the 'brand' AND the relevant metric (e.g., price), not just the number.

Only use the following tables:
{table_info}

Below are examples of questions and their corresponding SQL queries:
"""

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery"],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}",
    )

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=mysql_prompt,
        suffix="\nQuestion: {input}\nSQLQuery: ",
        input_variables=["input", "table_info", "top_k"], 
    )
    
    chain = SQLDatabaseChain.from_llm(
        llm=llm,
        db=db,
        prompt=few_shot_prompt,
        verbose=True,
        use_query_checker=False,
        return_intermediate_steps=True,
        return_direct=True 
    )
    return chain