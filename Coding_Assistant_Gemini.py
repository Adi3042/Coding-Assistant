import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# LangSmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

# Gemini API key
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

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
    st.markdown("❌ No memory is stored")

# Main UI
st.title("💻 Coding Assistant")
st.caption("Stateless AI • Coding & Computer Science Only")
st.info(f"📌 Current Mode: {language} (No memory)")

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
            You are a DOMAIN-LOCKED coding assistant.

            SELECTED DOMAIN = {language}

            Your job is to answer ONLY within this domain.
            You must FIRST classify the user's question internally before answering.

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
            Example:
            - SQL selected + "prime number program" ❌
            - SQL selected + "loop logic" ❌
            - SQL selected + "DSA" ❌

            3. If the question is invalid for the domain,
            respond with EXACTLY this sentence and nothing else:

            "Please ask a question related to {language} only."

            4. NEVER provide partial hints, logic, or alternative solutions
            outside the selected domain.

            5. Be concise, correct, and domain-pure.

            6. Stateless behavior. No memory.
                        """
                    ),
                    ("user", "{question}")
                ]
)


# Gemini LLM & Chain
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Input Section
question = st.text_area("🧠 Enter your coding question:", 
                        placeholder="e.g. Write a SQL query to find duplicate records", 
                        height=120)

col1, col2 = st.columns([1, 1])

with col1:
    ask_btn = st.button("🚀 Ask")

with col2:
    clear_btn = st.button("🧹 Clear")

# Clear Input
if clear_btn:
    st.rerun()

# Generate Response
if ask_btn and question.strip():
    with st.spinner("Thinking... 🤔"):
        response = chain.invoke({
            "question": question,
            "language": language
        })

    st.markdown("### ✅ Answer")
    st.markdown(response)

    with st.expander("📌 Why this answer?"):
        st.markdown(
            """
            - Generated using a **stateless coding assistant**
            """
        )

# Footer
st.markdown("---")
st.caption("⚡ Powered by Gemini • LangChain • Streamlit")