# Campus Assistant | SIH 2025 🏛️

A premium, multilingual AI-powered campus helpdesk designed for Rajasthan DTE. This assistant uses a **Hybrid RAG (Retrieval-Augmented Generation)** pipeline to provide accurate information about fees, scholarships, and admissions directly from college documents.

## ✨ Key Features

* **Premium UI**: Modern Glassmorphism design with full Dark Mode support.
* **Hybrid AI Extraction**: Automatically switches to **Llama 4 Scout Vision AI** if standard PDF text extraction fails (perfect for scanned notices).
* **Multilingual Support**: Real-time switching between English, Hindi, Marathi, and Tamil.
* **Admin Dashboard**: Secure portal for department heads to upload, sync, and delete knowledge base documents.
* **Token Optimization**: Optimized for `llama-3.1-8b-instant` to stay within daily rate limits during heavy usage.

## 🛠️ Tech Stack

* **Backend**: Flask (Python 3.11+)
* **AI Engine**: Groq (Llama 3.1 & Llama 4 Scout)
* **Database**: SQLite3
* **Frontend**: Bootstrap 5, Custom CSS (Glassmorphism), Vanilla JS

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed. It is recommended to use a virtual environment.
```powershell
python -m venv .venv
.\.venv\Scripts\activate
