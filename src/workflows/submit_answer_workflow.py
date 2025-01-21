
import asyncio
from datetime import timedelta
from typing import Any
from pydantic import BaseModel
from restack_ai.workflow import workflow, log, workflow_info, import_functions




with import_functions():
 
    from src.functions.RAG.ingestDocuments import ingest_documents_to_rag

    



# class Input(BaseModel):
#     # Add your input fields here
#     pass



@workflow.defn()
class submit_answer_workflow:
    @workflow.run
    async def run(self, input):



        # call the ingestDocuments function as a step function

        response = await workflow.step(
            ingest_documents_to_rag,
            input,
            start_to_close_timeout=timedelta(minutes=2)
        )


        # find the query and to that add this response to the backend


       



        # return final_response












		



        return {
            "result": "success"
        }