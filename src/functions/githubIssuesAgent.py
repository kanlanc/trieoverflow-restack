from restack_ai.function import function, log
from pydantic import BaseModel


@function.defn()
async def githubIssuesAgent() -> str:
    try:
        log.info("githubIssuesAgent function started")

        perplexityMessage = """

Unable to load github agent 
        
"""
        return perplexityMessage

    except Exception as e:
        log.error("githubIssuesAgent function failed", error=e)
        raise e
