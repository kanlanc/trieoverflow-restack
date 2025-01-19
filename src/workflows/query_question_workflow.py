
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
    from src.functions.gen_code.restack_code_generator import restack_code_gen

    



# class Input(BaseModel):
#     # Add your input fields here
#     pass



@workflow.defn()
class query_question_workflow:
    @workflow.run
    async def run(self, input):


        # First go through RAG and if you cant find similar questions anywhere,
        #  than go through the other agents

        # For the discord message, formatting, you should definetely process the discord messages before you
        # something with them esspecially using the "reference_message" field in the json to connect the dots

        # You also need to look into how to extract the threads in the messages!



        # ANOTHER APPRIOACH

        # DO THE RAG else

        # Use different agents and go through:
        #  - Docs
        #  - Perplexity
        #  - Discord
        #  - Github Issues



        log.info("AND IT STARTS!")

        user_query = input.get("query")

        RAG_QUERY_INPUT= {
            "query":user_query
        }


        final_response = {}


        # Call llama_cloud_rag with a sample query
        rag_results = await workflow.step(
            llama_cloud_rag,
            RAG_QUERY_INPUT,
            start_to_close_timeout=timedelta(minutes=2)
        )

        log.info(f"RAG Response: {rag_results['response']}")

        final_response["rag_results"]=rag_results['response']

        # Testing

        # return {"rag_output" : rag_results['response']}
        # log.info(f"Number of sources found: {rag_results['metadata']['total_sources']}")



        # VALIDATE THE RAG RESPONSE

        # FIXME: MOST LIKELY EXCEED THE TOKEN LIMIT FOR THE INPUT 

        # validate_RAG_response_input={
        #     "query": RAG_QUERY_INPUT["query"],
        #     "response": rag_results["response"]
        # }

        # validated_response = await workflow.step(
        #     validate_RAG_response,
        #     validate_RAG_response_input,
        #     start_to_close_timeout=timedelta(minutes=2)
        # )





        # TODO: make the return from validated_response be True or False later


        if(True):

            # Call perplexity agent and the other agents
            perplexity_input = {
                "query": RAG_QUERY_INPUT["query"]
            }

            perplexity_response = await workflow.step(
                perplexityAgent,
                perplexity_input,
                start_to_close_timeout=timedelta(minutes=2)
            )

            log.info(f"Perplexity Response: {perplexity_response}")

            final_response["perplexity_response"] = perplexity_response



        # TODO: MAKE THE TOOL OF RESTACK CLI BE USED


        if(True):

        # Call code generation function
            code_gen_input = {
                "query": RAG_QUERY_INPUT["query"]
            }

            code_gen_response = await workflow.step(
                restack_code_gen,
                code_gen_input, 
                start_to_close_timeout=timedelta(minutes=2),
                # retry_policy=RetryPolicy(maximum_attempts=2)
            )

            log.info(f"Code Generation Response: {code_gen_response}")

            final_response["code_gen_response"] = code_gen_response




        return final_response











            # DONT FORGET TO GET THE ANSWER FROM THE USER AND ADD THAT TO THE BACKEND

		



        return {
            "result": "success"
        }