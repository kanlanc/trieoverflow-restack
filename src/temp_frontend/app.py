import streamlit as st
from restack_ai import Restack
import asyncio
import time
import requests
import tomli
from pathlib import Path

# Load config
config_path = Path(__file__).parent.parent.parent / "config.toml"
with open(config_path, "rb") as f:
    config = tomli.load(f)

# API configuration
API_BASE_URL = config["restack"]["RESTACK_ENGINE_API_ADDRESS"]
if not API_BASE_URL.startswith("http"):
    API_BASE_URL = f"https://{API_BASE_URL}"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": config["restack"]["RESTACK_ENGINE_API_KEY"]
}

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
        color: #E0E0E0;
    }
    .stTextArea textarea {
        background-color: #2D2D2D;
        color: #E0E0E0;
        border: 1px solid #404040;
        border-radius: 4px;
    }
    .stButton button {
        background-color: #4A4A4A;
        color: #FFFFFF;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        transition: background-color 0.3s;
    }
    .stButton button:hover {
        background-color: #5A5A5A;
    }
    .result-container {
        background-color: #2D2D2D;
        padding: 1.5rem;
        border-radius: 4px;
        border: 1px solid #404040;
        margin: 1rem 0;
    }
    .header {
        background-color: #2D2D2D;
        padding: 1.5rem;
        border-radius: 4px;
        margin-bottom: 2rem;
        border-bottom: 2px solid #404040;
    }
    .responses-container {
        display: flex;
        gap: 2rem;
        margin: 1rem 0;
    }
    .responses-container > div {
        flex: 1;
        background-color: #2D2D2D;
        padding: 1rem;
        border-radius: 4px;
        border: 1px solid #404040;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state if not exists
if 'last_query' not in st.session_state:
    st.session_state.last_query = ""

# Header
st.markdown('<div class="header">', unsafe_allow_html=True)
st.title("🔍 TrieOverflow")
st.markdown("_Powered by Snowflake_")
st.markdown('</div>', unsafe_allow_html=True)

def process_query(query: str) -> dict:
    """Process a query using the query_question_workflow"""
    
    workflow_id = f"{int(time.time() * 1000)}-query_question_workflow"
    
    # Prepare the request payload
    payload = {
        "workflow_id": workflow_id,
        "input": {
            "query": query
        }
    }
    
    # Send POST request to the query workflow endpoint
    response = requests.post(
        f"{API_BASE_URL}/api/workflows/query_question_workflow",
        headers=headers,
        json=payload
    )
    
    if response.status_code != 200:
        return {
            'error': f"Error: {response.status_code} - {response.text}"
        }
    
    result = response.json()
    return {
        'workflow_id': workflow_id,
        'result': result
    }

def submit_answer(answer: str) -> str:
    """Submit an answer using the submit_answer_workflow"""
    if not st.session_state.last_query:
        return """
### ❌ Error
No query has been submitted yet! Please submit a query first before providing an answer.
"""

    workflow_id = f"{int(time.time() * 1000)}-submit_answer_workflow"
    
    # Prepare the request payload
    payload = {
        "workflow_id": workflow_id,
        "input": {
            "query": st.session_state.last_query,
            "answer": answer
        }
    }
    
    try:
        # Send POST request to the submit answer workflow endpoint
        response = requests.post(
            f"{API_BASE_URL}/api/workflows/submit_answer_workflow",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            return f"""
### ❌ Error
Failed to submit answer: {response.text}
"""
        
        result = response.json()
        
        return f"""
### ✅ Submission Status
Your answer has been successfully submitted and stored! Thank you for contributing.

**Query:** {st.session_state.last_query}
**Your Answer:** {answer}
**Result:** {result}
"""
        
    except Exception as e:
        return f"""
### ❌ Error
An error occurred while submitting your answer: {str(e)}
"""

# Initialize response state if not exists
if 'has_response' not in st.session_state:
    st.session_state.has_response = False
if 'current_response' not in st.session_state:
    st.session_state.current_response = None

# Main query section
st.markdown("### Submit Query")
query = st.text_area(
    "Enter your query",
    placeholder="How do I deploy a Next.js application with Restack?",
    height=150
)

if st.button("🚀 Submit Query"):
    if query:
        with st.spinner('🔄 Processing your query... Please wait.'):
            response = process_query(query)
            st.session_state.current_response = response
            st.session_state.has_response = True
            
            
    else:
        st.error("Please enter a query first!")

# Display response if exists
if st.session_state.has_response and st.session_state.current_response:
    response_data = st.session_state.current_response.get('result', {})
    workflow_id = st.session_state.current_response.get('workflow_id', '')
    
    if isinstance(response_data, dict):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🤖 Perplexity Response")
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            perplexity_response = response_data.get('perplexity_response', 'No Perplexity response available')
            # Clean up the response text
            perplexity_response = perplexity_response.strip().replace('\n        ', '\n')
            st.markdown(perplexity_response, unsafe_allow_html=False)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("#### 🤖 Github Response")
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            github_response = response_data.get('github_response', 'No Github response available')
            # Clean up the response text
            github_response = github_response.strip().replace('\n        ', '\n')
            st.markdown(github_response, unsafe_allow_html=False)
            st.markdown('</div>', unsafe_allow_html=True)

            # st.markdown("#### 🤖 Discord Response")
            # st.markdown('<div class="result-container">', unsafe_allow_html=True)
            # discord_response = response_data.get('discord_response', 'No Discord response available')
            # # Clean up the response text
            # discord_response = discord_response.strip().replace('\n        ', '\n')
            # st.markdown(discord_response, unsafe_allow_html=False)
            # st.markdown('</div>', unsafe_allow_html=True)

            # st.markdown("#### 🤖 Docs Response")
            # st.markdown('<div class="result-container">', unsafe_allow_html=True)
            # docs_response = response_data.get('docs_response', 'No Docs response available')
            # # Clean up the response text
            # docs_response = docs_response.strip().replace('\n        ', '\n')
            # st.markdown(docs_response, unsafe_allow_html=False)
            # st.markdown('</div>', unsafe_allow_html=True)


        
        with col2:
            st.markdown("#### 📚 Snowflake RAG Response")
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            rag_response = response_data.get('rag_results', 'No RAG response available')  # Changed from rag_response to rag_results
            # Clean up the response text
            rag_response = rag_response.strip().replace('\n        ', '\n')
            st.markdown(rag_response, unsafe_allow_html=False)
            st.markdown('</div>', unsafe_allow_html=True)
        
        
    else:
        st.error(f"Unexpected response format: {response_data}")
    
    # Show answer section only after getting a response
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Submit Answer")
        answer = st.text_area(
            "Enter the answer",
            placeholder="Enter your detailed answer here...",
            height=100
        )
        if st.button("✨ Submit Answer"):
            if answer:
                with st.spinner('🔄 Processing your answer... Please wait.'):
                    result = submit_answer(answer)
                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    st.markdown(result, unsafe_allow_html=False)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Please enter an answer first!")