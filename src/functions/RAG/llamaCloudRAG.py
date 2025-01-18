from restack_ai.function import function, log
import aiohttp  # Using aiohttp instead of requests for async operations

@function.defn()
async def llama_cloud_rag(query: str = "This is a placeholder query just in case"):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://localhost:8080/getRag",
                json={"query": query}  # Fixed input.query to query
            ) as response:
                response.raise_for_status()
                return await response.json()
                
    except aiohttp.ClientError as e:
        raise e
