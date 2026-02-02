# 🤖 AI Coding Assistant (Gemini / Ollama)

## 📌 Project Overview

This project is an **AI-powered Coding Assistant** built using **Large Language Models (LLMs)** and deployed with **Streamlit**.
It helps users with:

* Writing and debugging code
* Explaining programming concepts
* Generating code snippets
* Answering technical questions
* Context-aware conversations (with memory support)

The assistant supports **multiple backends** such as **Google Gemini API** and **Local Ollama models**, making it flexible for both **cloud-based** and **offline** usage.

---

## 🧠 Architecture Overview

The system follows a **prompt → LLM → response** pipeline.

### 🔹 Core Components

* **User Interface**: Streamlit web app
* **Prompt Handling**: Structured prompts for coding tasks
* **LLM Layer**:

  * Google Gemini (cloud-based)
  * Ollama (local models like LLaMA)
* **Memory Module** (optional): Maintains conversation context

### 🔄 Flow

User Query → Prompt Template → LLM (Gemini / Ollama) → Response → UI

---

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* Google Gemini API
* Ollama (Local LLMs)
* dotenv
* NumPy / Pandas (optional utilities)

---

## 📁 Project Structure

```text
Coding-Assistant/
├── Coding_Assistant_Gemini.py
├── Coding_Assistant_Ollama.py
├── Coding_Assistant_Ollama_memory.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation Steps

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Adi3042/Coding-Assistant.git
cd Coding-Assistant
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Setup

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

> ⚠️ Required only for **Gemini-based assistant**

---

## ▶️ Run the Application

### 🔹 Gemini-based Coding Assistant

```bash
streamlit run Coding_Assistant_Gemini.py
```

### 🔹 Ollama-based Coding Assistant (Local LLM)

```bash
streamlit run Coding_Assistant_Ollama.py
```

### 🔹 Ollama with Conversation Memory

```bash
streamlit run Coding_Assistant_Ollama_memory.py
```

> Make sure Ollama is installed and the required model is pulled:

```bash
ollama pull llama3.2
```

---
