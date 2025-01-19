from restack_ai.function import function, FunctionFailure, log
from llama_index.llms.anthropic import Anthropic
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from llama_index.core import get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine
from typing import Dict, List
import os

@function.defn()
async def validate_RAG_response(input: dict) -> dict:
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
        rag_response = input.get("response")
       

        # Construct the query prompt
        query_prompt = f"""
        You are a helpful coding assistant. I have a question from a user that needs to be answered using relevant documentation and discussions.

        Below there is a response that I intend to give to the user, I want you to evaluate and tell me if the resposne answers the users query

        User Question: {query}

        Response: {rag_response}

        Please provide a detailed and accurate response that:
        1. Directly addresses the user's coding question
        2. Includes relevant code examples when appropriate
        3. Explains the reasoning behind the solution
        4. References any best practices or important considerations
        5. Cites specific documentation or discussions that support the answer

        Format your response in a clear, structured way with:
        - A direct answer to the question
        - Code examples (if applicable)
        - Explanation of key concepts
        - Any important caveats or considerations
        - References to supporting documentation

        Base your response only on the most relevant information from the knowledge base.
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