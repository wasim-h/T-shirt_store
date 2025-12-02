from flask import Flask, render_template, request, jsonify
from langHelp import get_few_shot_db_chain
import re

app = Flask(__name__)

chain = get_few_shot_db_chain()

from decimal import Decimal 

def format_answer(result):
    text = str(result)
    
    for char in "[](),'":
        text = text.replace(char, "")
    
    text = text.replace("Decimal", "")
    
    return text.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_answer', methods=['POST'])
def get_answer():
    question = request.form.get('question')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    try:
        response = chain.invoke({"query": question})
        
        result = response.get("result", "")
        formatted_answer = format_answer(result)
        
        sql_query = "SQL not available"
        if "intermediate_steps" in response:
            for step in response["intermediate_steps"]:
                if isinstance(step, str) and "SELECT" in step.upper():
                    sql_query = step
                    break
                    
        return jsonify({
            'answer': formatted_answer,
            'sql_query': sql_query
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)