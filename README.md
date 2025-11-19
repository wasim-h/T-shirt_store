# 👕 AI-Powered T-Shirt Store Assistant

A GenAI-powered application that helps users find t-shirts using natural language. Instead of applying manual filters, users can simply ask: *"Show me extra large white t-shirts under $20"* or *"Do you have any Levi's t-shirts in stock?"*

## 🚀 Features
- **Natural Language Search:** Uses an LLM to interpret user queries.
- **Database Integration:** Automatically converts user questions into SQL queries (Text-to-SQL).
- **Few-Shot Learning:** Uses `few_shots.py` to train the model on specific examples for higher accuracy.

## 🛠️ Tech Stack
- **Python**
- **Streamlit** (Frontend)
- **LangChain** (LLM Framework)
- **Google Gemini / OpenAI** (LLM)
- **ChromaDB / FAISS** (Vector Store for few-shots)

## 📂 Project Structure
- `main.py`: The main Streamlit application entry point.
- `langHelp.py`: Helper functions for LLM interaction and chain management.
- `few_shots.py`: Contains training examples to guide the LLM's SQL generation.

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/wasim-h/T-shirt_store.git](https://github.com/wasim-h/T-shirt_store.git)