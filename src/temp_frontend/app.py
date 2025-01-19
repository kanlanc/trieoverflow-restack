import gradio as gr
from restack_ai import Restack
from typing import Optional
import asyncio
import time

# temp frontend

# Initialize Restack client
client = Restack()

state={"last_query":""}

async def submit_query(query: str, state: Optional[dict] = None) -> tuple[str, dict]:
    """Submit a query to the query_question_workflow"""
    # Schedule the workflow
    workflow_id = f"{int(time.time() * 1000)}-query_question_workflow"

    input = {"query":query}

    print(input)

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
   
    # Store the query in state for later use
    state = {"last_query": query}
    
    return f"Query result: {result}", state

def submit_answer(answer: str, state: Optional[dict] = None) -> str:
    """Submit an answer using the submit_answer_workflow"""
    if not state or "last_query" not in state:
        return "Error: No query has been submitted yet!"
    
    # Schedule the submit_answer_workflow with both query and answer
    workflow_run = client.schedule_workflow(
        "submit_answer_workflow",
        input={
            "query": state["last_query"],
            "answer": answer
        }
    )
    
    return f"Answer submitted! Workflow ID: {workflow_run.id}"

# Create the Gradio interface
with gr.Blocks() as app:
    # Initialize state
    state = gr.State({})
    
    with gr.Row():
        with gr.Column():
            # Query input
            query_input = gr.Textbox(
                label="Enter your query",
                placeholder="How do I deploy a Next.js application with Restack?"
            )
            query_button = gr.Button("Submit Query")
            query_output = gr.Textbox(label="Query Status")
            
        with gr.Column():
            # Answer input
            answer_input = gr.Textbox(
                label="Submit Answer",
                placeholder="Enter the answer here..."
            )
            answer_button = gr.Button("Submit Answer")
            answer_output = gr.Textbox(label="Answer Status")
    
    # Set up event handlers
    query_button.click(
        submit_query,
        inputs=[query_input, state],
        outputs=[query_output, state],
        show_progress="full"
    )
    
    answer_button.click(
        submit_answer,
        inputs=[answer_input, state],
        outputs=answer_output
    )

if __name__ == "__main__":
    app.launch()