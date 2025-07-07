# 📚 Library Management System API

A FastAPI-based Library Management System that handles authors, books, and members with file-based JSON storage. This project provides clean API endpoints for managing library 
resources and is ideal for learning and experimenting with FastAPI, Pydantic models, and modular API design.

## 🚀 Features

- Add, update, delete, and list authors, books, and members
- File-based data persistence using JSON
- Data validation with Pydantic
- Organized using FastAPI APIRouter
- Custom error handling
- Auto-generated interactive docs (Swagger UI)

## 🧱 Tech Stack

- 🐍 Python 3.10+
- ⚡ FastAPI
- 🔒 Pydantic
- 💾 JSON for file-based data storage

## 🛠️ Installation & Setup

1. Clone the repository
git clone https://github.com/manvigargg/library_management_system-fastapi.git
cd library_management_system-fastapi

2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
pip install fastapi uvicorn

4. Run the app
uvicorn main:app --reload

5. 📬 API Documentation
Once running, visit:
Swagger UI: http://127.0.0.1:8000/docs




