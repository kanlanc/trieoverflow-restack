
import asyncio
from datetime import timedelta
from typing import Any
from pydantic import BaseModel
from restack_ai.workflow import workflow, log, workflow_info, import_functions




with import_functions():
    # from src.functions.<your_function_filename> import <your_function_name>
    from src.functions.discordAgent import discordAgent
    from src.functions.githubIssuesAgent import githubIssuesAgent
    from src.functions.perplexity.perplexityAgent import perplexityAgent
    from src.functions.RAG.llamaCloudRAG import llama_cloud_rag
    from src.functions.RAG.validateRAGResponse import validate_RAG_response
    # from src.functions.gen_code.restack_code_generator import restack_code_gen

    



# class Input(BaseModel):
#     # Add your input fields here
#     pass



@workflow.defn()
class query_question_workflow:
    @workflow.run
    async def run(self, input):


        # find the query and to that add this response to the backend


       



        # return final_response












		



        return {
            "result": "success"
        }