# With Memory
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain_community.memory import ConversationBufferMemory
# from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory


# Load environment variables
load_dotenv()

history = StreamlitChatMessageHistory(key="chat_history")

# LangSmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

# Page Configuration
st.set_page_config(page_title="Coding Assistant", page_icon="💻", layout="centered")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    language = st.selectbox(
        "Preferred Language",
        ["General", "Python", "SQL", "Machine Learning", "Data Science"]
    )
    st.markdown("---")
    st.markdown("💡 **Tip:** Ask clear coding questions")
    st.markdown("✅ Memory is ON. The assistant will remember previous interactions.")

# Main UI
st.title("💻 Coding Assistant with Memory")
st.caption("Persistent AI • Coding & Computer Science Only")
st.info(f"📌 Current Mode: {language} (Memory Enabled)")

st.markdown(
    """
    Ask questions related to:
    - Programming
    - Data Structures & Algorithms
    - SQL
    - Machine Learning
    - Computer Science concepts
    """
)

# Domain-restricted prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a DOMAIN-LOCKED coding assistant with memory.

            SELECTED DOMAIN = {language}

            Remember previous questions and answers in this conversation.
            Your job is to answer ONLY within this domain.

            ======================
            ALLOWED DOMAINS
            ======================

            • SQL
            - Queries (SELECT, JOIN, GROUP BY, WINDOW FUNCTIONS)
            - Indexes, constraints, normalization
            - Stored procedures, views
            - Database concepts ONLY

            • Python
            - Python syntax, functions, OOP
            - Algorithms implemented in Python
            - Libraries like numpy, pandas, matplotlib

            • Machine Learning
            - ML algorithms, math intuition
            - Model training, evaluation
            - Scikit-learn, deep learning concepts

            • Data Science
            - EDA, statistics
            - Feature engineering
            - Data pipelines, visualization

            • General
            - Basic CS theory only
            - No coding unless explicitly asked

            ======================
            STRICT RULES (NO EXCEPTIONS)
            ======================

            1. If the question DOES NOT belong to the SELECTED DOMAIN,
            DO NOT answer it.

            2. Do NOT translate the question into another domain.

            3. If the question is invalid for the domain,
            respond with EXACTLY this sentence and nothing else:

            "Please ask a question related to {language} only."

            4. NEVER provide partial hints, logic, or alternative solutions
            outside the selected domain.

            5. Be concise, correct, and domain-pure.
            """
        ),
        ("user", "{question}")
    ]
)

# Memory
# memory = ConversationBufferMemory(return_messages=True)

# LLM & Chain
llm = Ollama(model="llama3.2")
output_parser = StrOutputParser()
base_chain = prompt | llm | output_parser
chain = RunnableWithMessageHistory(
    base_chain,
    lambda session_id: history,
    input_messages_key="question",
    history_messages_key="history",
)
# chain = prompt | llm | output_parser | memory  # Added memory here

# Input Section
question = st.text_area(
    "🧠 Enter your coding question:", 
    placeholder="e.g. Write a SQL query to find duplicate records", 
    height=120
)

col1, col2 = st.columns([1, 1])

with col1:
    ask_btn = st.button("🚀 Ask")

with col2:
    clear_btn = st.button("🧹 Clear")

# Clear Input & Memory
if clear_btn:
    history.clear()
    st.rerun()


# Generate Response
if ask_btn and question.strip():
    with st.spinner("Thinking... 🤔"):
        response = chain.invoke(
            {"question": question, "language": language},
            config={"configurable": {"session_id": "streamlit-session"}}
        )

    st.markdown("### ✅ Answer")
    st.markdown(response)


    with st.expander("📌 Conversation History"):
        for msg in history.messages:
            st.write(f"{msg.type.upper()}: {msg.content}")