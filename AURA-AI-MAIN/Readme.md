# Aura.AI Backend

This is the backend service for **Aura.AI**, built with **FastAPI**.  
It provides APIs for fetching, analyzing, and serving city vibes data.

---

## 🚀 Getting Started

### 1. Create a Virtual Environment
Using uv:
```bash
uv venv venv
```

Activate it:
- Linux / macOS
  ```bash
  source venv/bin/activate
  ```
- Windows (PowerShell)
  ```bash
  .\venv\Scripts\activate
  ```

### 2. Install Dependencies
Make sure you have a `requirements.txt` file (already included in this repo).  
Install all dependencies with:
```bash
uv pip install -r requirements.txt
```

### 3. Run the Server
Start the FastAPI backend with:
```bash
uvicorn main:app --reload --port 8000
```

This will run the app in development mode with hot-reload enabled.

### 4. API Documentation
Once the server is running, open your browser at:

- Swagger UI → http://127.0.0.1:8000/docs
- ReDoc → http://127.0.0.1:8000/redoc

---

## 📦 Project Structure
```
AURA DATA [WSL: UBUN...]
├── __pycache__
├── models
│   ├── __pycache__
│   ├── schemas.py
├── services
│   ├── __pycache__
│   ├── data_collector_122.py
│   ├── data_collector.py
│   ├── database.py
│   ├── llm_service.py
│   ├── rag_service.py
├── venv
├── .env
├── .gitignore
├── requirement.txt.swp
├── aura_data_20250813_234214.json
├── aura_data_20250813_234826.json
├── aura_data.db
├── main.py
├── notebook.ipynb
├── requirements.txt
```