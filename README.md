# 📘 LangChain Memory System

**LangChain Memory System** is a memory-focused project designed to deeply understand and demonstrate the difference between **short-term memory** and **long-term memory** in LangChain-based systems.

---

## 🎯 Core Objective

The primary goal of this project is to answer one fundamental question:

> **How does memory actually work in LLM systems built with LangChain?**

Specifically, this project explores:

- What *short-term memory* is and when it exists
- Why LangChain memory is **not persistent**
- How *long-term memory* must be implemented explicitly
- How both memory types coexist in a real system design

This project avoids advanced features on purpose so the memory behavior is **clear, observable, and explainable**.

---

## 🧠 Memory Architecture (Key Concept)

This system uses **two completely separate memory layers**, each with a clear responsibility.

---

### 1️⃣ Short-Term Memory (Execution-Time Memory)

**Purpose:**  
Maintain conversational context and reasoning **within a single run**.

**Implementation:**
- `InMemoryChatMessageHistory`
- Integrated via `RunnableWithMessageHistory`

**Characteristics:**
- Stored in RAM
- Exists only while the program is running
- Automatically cleared when the program exits
- Used only for conversation and reasoning
- Not suitable for storing knowledge or facts

---

### 2️⃣ Long-Term Memory (Persistent Memory)

**Purpose:**  
Store user-provided learnings **across days and executions**.

**Implementation:**
- JSON file (`long_term_memory.json`)

**Characteristics:**
- Stored on disk
- Persists across program restarts
- Independent of LangChain
- Deterministic and auditable
- Used for recall by date

---

### 🔑 Key Insight

> **LangChain handles short-term conversational context, not long-term memory.**  
> Persistent memory must be implemented explicitly.

This distinction is the central learning outcome of the project.

---

## 🔁 Daily Workflow (End-to-End)

1. A daily email reminder is sent using GitHub Actions  
2. The user manually runs the program  
3. The user enters their learning for the day  
4. The learning is stored persistently in JSON  
5. The system can later recall learnings by date  

This design keeps a **human-in-the-loop** to avoid hallucinated or autonomous memory creation.

---

## 🧩 Why Human-in-the-Loop Matters

This project intentionally **does not auto-run**.

Reasons:
- Prevents hallucinated knowledge
- Keeps memory trustworthy
- Ensures learning is intentional
- Mirrors real reflective learning behavior

This design choice is deliberate and important.

---

## 📂 Project Structure

```text
langchain_memory_system/
├── agent.py                 # Main LLM interaction logic
├── reminder_email.py        # Email reminder script
├── long_term_memory.json    # Persistent long-term memory
├── requirements.txt
├── .env                     # Local secrets
├── .github/
│   └── workflows/
│       └── daily_reminder.yml
└── README.md
```

---

## 🧰 Technology Stack

### Programming Language
- **Python 3.10+**

### AI / LLM
- **LangChain (modern runnable-based API)**
- **Groq API (LLaMA model)**

### Memory
- **Short-term memory:** In-memory chat history (execution-time only)
- **Long-term memory:** JSON file (`long_term_memory.json`) stored on disk

### Automation
- **GitHub Actions** – for daily email reminders

### Email
- **Gmail SMTP** – sends reminder emails

### Environment & Tooling
- **Virtual Environment (venv)**
- **python-dotenv** – for environment variables
- **Git & GitHub** – version control

---

## ▶️ Running the System

**Install dependencies by running:** pip install -r requirements.txt

**Create a `.env` file in the project root with the following values:**
- GROQ_API_KEY=your_groq_api_key
- EMAIL_USER=your_email@gmail.com
- EMAIL_PASS=your_gmail_app_password
- EMAIL_TO=your_email@gmail.com

**Run using:** python agent.py

After running, you should see the following menu:

```
=== LangChain Memory System ===
- Add today's learning (long-term memory)
- Recall learning by date (long-term memory)
- Chat with LLM (short-term memory demo)
- Exit
```
