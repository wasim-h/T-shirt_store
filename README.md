# 👕 T-Shirt Store AI Analyst

A Natural Language to SQL (NL2SQL) application that allows store managers to ask questions about their inventory in plain English. The system uses LangChain, Ollama (Gemma 2), and a MySQL database to generate accurate SQL queries and return real-time answers.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20App-green)
![LangChain](https://img.shields.io/badge/LangChain-Framework-orange)
![Ollama](https://img.shields.io/badge/Ollama-Gemma%202-purple)

## 🚀 Features

* **Natural Language Queries:** Ask questions like "How many white Nike t-shirts do we have?" without writing SQL.
* **Few-Shot Learning:** Uses vector embeddings (ChromaDB) to select relevant SQL examples, improving accuracy.
* **SQL Generation & Execution:** Automatically generates syntactically correct MySQL queries and executes them safely.
* **Clean UI:** A responsive web interface built with HTML/CSS and JavaScript.
* **Model:** Powered by the local Gemma 2 model via Ollama.

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **LLM Orchestration:** LangChain (SQLDatabaseChain)
* **LLM:** Ollama (Model: `gemma2:2b`)
* **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
* **Vector Store:** ChromaDB
* **Database:** MySQL
* **Frontend:** HTML5, CSS3, JavaScript

## 📂 Project Structure

```text
├── static/
│   └── style.css        # Frontend styling
├── templates/
│   └── index.html       # Chat interface
├── app.py               # Flask application entry point
├── langHelp.py          # LangChain & Ollama logic
├── few_shots.py         # Training examples for the LLM
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation