import asyncio
import os
from src.functions.function import welcome
from src.client import client



# Functions
from src.functions.discordAgent import discordAgent
from src.functions.githubIssuesAgent import githubIssuesAgent
from src.functions.perplexity.perplexityAgent import perplexityAgent
from src.functions.RAG.llamaCloudRAG import llama_cloud_rag
from src.functions.RAG.validateRAGResponse import validate_RAG_response
from src.functions.gen_code.restack_code_generator import restack_code_gen


# Workflows

from src.workflows.query_question_workflow import query_question_workflow



from watchfiles import run_process






async def main():

    await client.start_service(
        workflows=[query_question_workflow],
        functions=[discordAgent, githubIssuesAgent, perplexityAgent, llama_cloud_rag, validate_RAG_response,restack_code_gen]
    )

def run_services():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Service interrupted by user. Exiting gracefully.")

def watch_services():
    watch_path = os.getcwd()
    print(f"Watching {watch_path} and its subdirectories for changes...")
    run_process(watch_path, recursive=True, target=run_services)

if __name__ == "__main__":
       run_services()
