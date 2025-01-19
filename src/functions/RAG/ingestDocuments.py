from restack_ai.function import function, FunctionFailure, log
from llama_index.llms.anthropic import Anthropic
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from llama_index.core import get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine
from typing import Dict, List
import os


async def create_questions_from_processed_discord_messages(input: dict) -> dict:
    # Validate input and API keys
    if not input:
        raise FunctionFailure("Invalid input: input dictionary cannot be empty", non_retryable=True)
    
    required_keys = {
        "LLAMA_CLOUD_API_KEY": os.getenv("LLAMA_CLOUD_API_KEY"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
    }
    
    missing_keys = [k for k, v in required_keys.items() if not v]
    if missing_keys:
        raise FunctionFailure(f"Missing required API keys: {', '.join(missing_keys)}", non_retryable=True)

    try:
        # Initialize LlamaCloud Index
        

        index = LlamaCloudIndex(
            name="Trieoverflow General Index for All Frameworks", 
            project_name="Trieoverflow",
            organization_id="37ad34df-e1d9-481e-9007-9b194cf46e13",
            api_key=required_keys["LLAMA_CLOUD_API_KEY"]
        )

        # Initialize LLMs
        llm_anthropic = Anthropic(
            model="claude-3-5-sonnet-20240620",
            api_key=required_keys["ANTHROPIC_API_KEY"],
            timeout=60
        )

       

        # Setup retriever and query engine
        response_synthesizer = get_response_synthesizer(llm=llm_anthropic)
        retriever = index.as_retriever(
            dense_similarity_top_k=5,
            sparse_similarity_top_k=5,
            alpha=0.5,
            enable_reranking=True,
            rerank_top_n=5
        )

        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer
        )

        # Extract input parameters
        query = input.get("query")
        user_preferences = input.get("user_preferences")
        context = input.get("context", "")

        # Construct the query prompt
        query_prompt = f"""
        Based on the following information:
        
        Query: {query}
        User Preferences: {user_preferences}
        Additional Context: {context}
        
        Please provide relevant information and insights while considering:
        1. The specific query requirements
        2. User's stated preferences
        3. Any contextual information provided
        
        Format the response to be clear and structured.
        """

        # Execute query
        response = query_engine.query(query_prompt)
        
        return {
            "response": response.response,
            "sources": [node.text for node in response.source_nodes],
            "metadata": {
                "query_timestamp": response.metadata.get("timestamp"),
                "total_sources": len(response.source_nodes)
            }
        }

    except Exception as e:
        log.error(f"Error in llama_cloud_rag: {str(e)}")
        raise FunctionFailure(f"Failed to process RAG query: {str(e)}", non_retryable=True) from e