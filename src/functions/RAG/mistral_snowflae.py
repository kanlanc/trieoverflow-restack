# from restack_ai.function import function, FunctionFailure, log
# from llama_index.llms.anthropic import Anthropic
# from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
# from llama_index.core import get_response_synthesizer
# from llama_index.core.query_engine import RetrieverQueryEngine
# from typing import Dict, List
# import os

# # from snowflake.snowpark import Session
# # from snowflake.cortex import Complete, ExtractAnswer, Sentiment, Summarize, Translate

# # Create Snowflake session
# # session = Session.builder.configs({
# #     "user": os.getenv('SNOWFLAKE_USER'),
# #     "password": os.getenv('SNOWFLAKE_PASSWORD'),
# #     "account": os.getenv('SNOWFLAKE_ACCOUNT'),
# #     "warehouse": os.getenv('SNOWFLAKE_WAREHOUSE'),
# #     "database": os.getenv('SNOWFLAKE_DATABASE'),
# #     "schema": os.getenv('SNOWFLAKE_SCHEMA')
# # }).create()[3]



# # @function.defn()
# # async def mistral_snowflae(input: dict) -> dict:
# #     # Validate input and API keys
# #     if not input:
# #         raise FunctionFailure("Invalid input: input dictionary cannot be empty", non_retryable=True)
    
   
# #     response = Complete(
# #         "mistral-large",
# #         input["query"],
# #         session=session,
# #         stream=True
# #     )

# #     # Print streaming response
# #     for update in response:
# #         print(update)[6]
