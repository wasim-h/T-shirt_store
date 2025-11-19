# import streamlit as st
# from langchain_community.utilities import SQLDatabase
# from langchain_experimental.sql import SQLDatabaseChain
# from langchain_core.example_selectors import SemanticSimilarityExampleSelector
# from langchain_huggingface import HuggingFaceEmbeddings  
# from langchain_chroma import Chroma  
# from langchain_core.prompts import FewShotPromptTemplate
# from langchain_experimental.sql import prompt as sql_prompts
# from langchain_core.prompts import PromptTemplate
# from langchain_ollama import ChatOllama
# from few_shots import few_shots

# llm = ChatOllama(model="mistral:7b", temperature=0.1)
# @st.cache_resource  
# def get_few_shot_db_chain():
#     print("--- LOADING MODELS AND CREATING CHAIN ---")
#     db_user = 'root'
#     db_password = '2363'
#     db_host = 'localhost'
#     db_name = 'tshirt_store'

#     db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}", sample_rows_in_table_info=3)
#     # print(db.table_info)

#     embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
#     to_vectorize = [" ".join(example.values()) for example in few_shots]
#     vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
#     example_selector = SemanticSimilarityExampleSelector(
#         vectorstore=vectorstore,
#         k=2,
#     )
    
#     mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
# Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
# Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
# Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
# Pay attention to use CURDATE() function to get the current date, if the question involves "today".

# Use the following format:

# Question: Question here
# SQLQuery: Query to run with no pre-amble
# SQLResult: Result of the SQLQuery
# Answer: Final answer here

# No pre-amble.
# """

#     example_prompt = PromptTemplate(
#         input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
#         template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
#     )

#     few_shot_prompt = FewShotPromptTemplate(
#         example_selector=example_selector,
#         example_prompt=example_prompt,
#         prefix=mysql_prompt,
#         suffix=sql_prompts.PROMPT_SUFFIX,
#         input_variables=["input", "table_info", "top_k"], 
#     )
    
#     chain = SQLDatabaseChain(
#     llm=llm,
#     database=db,
#     prompt=few_shot_prompt
# )
#     return chain


import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_huggingface import HuggingFaceEmbeddings  
from langchain_chroma import Chroma  
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from few_shots import few_shots
import re

llm = ChatOllama(
    model="gemma2:2b",
    temperature=0,
    num_predict=128  
)

@st.cache_resource  
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
        k=2,
    )
    
    # Simplified prompt that focuses on generating SQL only
    mysql_prompt = """You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run.

IMPORTANT: Output ONLY the SQL query, no markdown formatting, no code blocks, no explanations.

Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL.

Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.

Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Pay attention to use CURDATE() function to get the current date, if the question involves "today".

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


def clean_sql_query(query):
    """Extract and clean SQL query from LLM output"""
    query = re.sub(r'```sql\s*', '', query)
    query = re.sub(r'```\s*', '', query)
    
    if ';' in query:
        query = query.split(';')[0] + ';'
    
    query = re.sub(r'SQLResult:.*', '', query, flags=re.DOTALL)
    query = re.sub(r'Answer:.*', '', query, flags=re.DOTALL)
    
    return query.strip()

class CleanSQLDatabase(SQLDatabase):
    def run(self, command, fetch="all", include_columns=False, **kwargs):
        """Execute SQL command after cleaning it"""
        if isinstance(command, str):
            command = clean_sql_query(command)
        return super().run(command, fetch, include_columns, **kwargs)