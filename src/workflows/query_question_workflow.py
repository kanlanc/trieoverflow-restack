
import asyncio
from datetime import timedelta
from typing import Any
from pydantic import BaseModel
from restack_ai.workflow import workflow, log, workflow_info, import_functions




with import_functions():
    # from src.functions.<your_function_filename> import <your_function_name>
    from src.functions.discordAgent import discordAgent
    from src.functions.githubIssuesAgent import githubIssuesAgent
    from src.functions.perplexityAgent import perplexityAgent
    from src.functions.RAG.llamaCloudRAG import llama_cloud_rag
    



# class Input(BaseModel):
#     # Add your input fields here
#     pass



@workflow.defn()
class query_question_workflow:
    @workflow.run
    async def run(self, input):



		


		# results = await workflow.step(
        #     <function_name>,
        #     input,
        #     start_to_close_timeout=timedelta(minutes=2)
        # )

        return {
            "result": "success"
        }