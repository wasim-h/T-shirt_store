# import streamlit as st
# from langHelp import get_few_shot_db_chain

# st.title('T-Shirt Store 👕')

# question = st.text_input("Question : ")

# if question:
#     chain =  get_few_shot_db_chain()
#     with st.spinner("Thinking..."):
#         answer = chain.invoke({"query": question})
#         st.header("Answer")
#         st.write(answer.get("result", "Sorry, I couldn't find an answer."))




import streamlit as st
from langHelp import get_few_shot_db_chain
import re

st.title('T-Shirt Store 👕')

question = st.text_input("Question: ")

def format_answer(result_data):
    """Format the SQL result into a readable answer"""
    if isinstance(result_data, str):
        number_match = re.search(r"Decimal\('([^']+)'\)", result_data)
        if number_match:
            return number_match.group(1)
        number_match = re.search(r'\[\(([^,\)]+)', result_data)
        if number_match:
            return number_match.group(1)
        return result_data
    
    if isinstance(result_data, list) and len(result_data) > 0:
        if isinstance(result_data[0], tuple) and len(result_data[0]) > 0:
            return str(result_data[0][0])
    
    return str(result_data)

if question:
    chain = get_few_shot_db_chain()
    with st.spinner("Thinking..."):
        try:
            response = chain.invoke({"query": question})
            
            st.header("Answer")
            
            result = response.get("result", "")
            formatted_answer = format_answer(result)
            st.success(formatted_answer)
            
            if "intermediate_steps" in response:
                for step in response["intermediate_steps"]:
                    if isinstance(step, str) and "SELECT" in step.upper():
                        with st.expander("Show SQL Query"):
                            st.code(step, language="sql")
                        break
                
        except Exception as e:
            st.error("An error occurred while processing your question.")
            error_msg = str(e)
            
            if "syntax" in error_msg.lower():
                st.warning("The generated SQL query has a syntax error. Please try rephrasing your question.")
            else:
                st.warning("Please try rephrasing your question or check if the data exists.")