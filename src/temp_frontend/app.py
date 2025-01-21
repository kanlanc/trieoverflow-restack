import streamlit as st
from restack_ai import Restack
import asyncio
import time

# Initialize Restack client
client = Restack()

# Initialize session state if not exists
if 'last_query' not in st.session_state:
    st.session_state.last_query = ""

st.title("Restack Query Interface")

async def submit_query(query: str) -> str:
    """Submit a query to the query_question_workflow"""
    workflow_id = f"{int(time.time() * 1000)}-query_question_workflow"
    input = {"query": query}
    
    run_id = await client.schedule_workflow(
        workflow_name="query_question_workflow",
        workflow_id=workflow_id,
        input=input
    )

    # Wait for the result
    result = await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=run_id
    )
    
    st.session_state.last_query = query
    return f"Query result: {result}"

def submit_answer(answer: str) -> str:
    """Submit an answer using the submit_answer_workflow"""
    if not st.session_state.last_query:
        return "Error: No query has been submitted yet!"
    
    # Schedule the submit_answer_workflow with both query and answer
    workflow_run = client.schedule_workflow(
        "submit_answer_workflow",
        input={
            "query": st.session_state.last_query,
            "answer": answer
        }
    )
    
    return f"Answer submitted! Workflow ID: {workflow_run.id}"

# Create two columns for query and answer
col1, col2 = st.columns(2)

with col1:
    st.subheader("Submit Query")
    query = st.text_area(
        "Enter your query",
        placeholder="How do I deploy a Next.js application with Restack?"
    )
    if st.button("Submit Query"):
        if query:
            with st.spinner('Processing your query... Please wait.'):
                result = asyncio.run(submit_query(query))
                st.write(result)
        else:
            st.error("Please enter a query first!")

with col2:
    st.subheader("Submit Answer")
    answer = st.text_area(
        "Enter the answer",
        placeholder="Enter the answer here..."
    )
    if st.button("Submit Answer"):
        if answer:
            with st.spinner('Processing your answer... Please wait.'):
                result = submit_answer(answer)
                st.write(result)
        else:
            st.error("Please enter an answer first!")