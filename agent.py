"""
Learning Memory AI Agent

Goal of this file:
------------------
To clearly demonstrate the difference between:
1. Short-term memory (LangChain, in-RAM, execution-time)
2. Long-term memory (JSON, persistent across runs)

This project is intentionally simple.
No semantic memory, no vectors, no routing.
"""

import json
from datetime import date
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

# --------------------------------------------------
# ENVIRONMENT SETUP
# --------------------------------------------------
# Loads environment variables such as GROQ_API_KEY.
# This happens every time the program starts.
load_dotenv()

# --------------------------------------------------
# SHORT-TERM MEMORY (LANGCHAIN)
# --------------------------------------------------
# This memory:
# - Lives ONLY during program execution
# - Is stored in RAM
# - Is cleared when the program exits
# - Is used ONLY for conversational context and reasoning
#
# This is equivalent to "working memory" in humans.
llm = ChatGroq(model="llama-3.3-70b-versatile")

# Correct short-term memory primitive
short_term_memory = InMemoryChatMessageHistory()

# Prompt explicitly includes conversation history
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ]
)

# Chain = prompt → LLM
chain = prompt | llm

# RunnableWithMessageHistory:
# - Reads from short_term_memory before each call
# - Writes new messages back after each call
chat_agent = RunnableWithMessageHistory(
    chain,
    lambda session_id: short_term_memory,
    input_messages_key="input",
    history_messages_key="history",
)

# --------------------------------------------------
# LONG-TERM MEMORY (JSON FILE)
# --------------------------------------------------
# This memory:
# - Is stored on disk
# - Persists across multiple program runs
# - Stores factual learning entered by the user
# - Is NOT managed by LangChain
#
# This is equivalent to "long-term memory" in humans.
MEMORY_FILE = "long_term_memory.json"


def load_long_term_memory():
    """Reads all stored learning entries from disk."""
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_long_term_memory(data):
    """Writes updated learning entries back to disk."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def store_learning(text):
    """Stores a new learning entry in long-term memory."""
    data = load_long_term_memory()
    data.append({
        "date": str(date.today()),
        "learning": text
    })
    save_long_term_memory(data)


def recall_by_date(target_date):
    """Retrieves learning from long-term memory by date."""
    data = load_long_term_memory()
    for entry in data:
        if entry["date"] == target_date:
            return entry["learning"]
    return "No learning found for that date."


# --------------------------------------------------
# COMMAND LINE INTERFACE (HUMAN-IN-THE-LOOP)
# --------------------------------------------------
print("\n=== Learning Memory AI Agent ===")
print("1. Add today's learning (long-term memory)")
print("2. Recall learning by date (long-term memory)")
print("3. Chat with agent (short-term memory demo)")
print("4. Exit")

while True:
    choice = input("\nChoose an option: ").strip()

    if choice == "1":
        # User provides ground-truth learning.
        learning = input("What did you learn today? ")
        store_learning(learning)
        print("Saved to long-term memory.")

    elif choice == "2":
        # Reads from persistent memory on disk.
        day = input("Enter date (YYYY-MM-DD): ")
        print("Learning:", recall_by_date(day))

    elif choice == "3":
        # Demonstrates short-term memory behavior.
        user_input = input("You: ")

        response = chat_agent.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": "cli-session"}}
        )

        print("Agent:", response.content)

        # Debug output to SHOW what is in short-term memory
        print("\n[DEBUG] Short-term memory contents:")
        print(short_term_memory.messages)

    elif choice == "4":
        # When the program exits:
        # - Short-term memory is destroyed
        # - Long-term memory remains on disk
        print("Exiting agent.")
        break

    else:
        print("Invalid choice.")
