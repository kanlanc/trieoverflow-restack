from restack_ai.function import function, log
from pydantic import BaseModel
import os

from llama_index.core.llms import ChatMessage
from llama_index.llms.perplexity import Perplexity


@function.defn()
async def perplexityAgent(input) -> str:
    try:
        log.info("perplexityAgent function started")

        query = input.get("query")


        pplx_api_key = os.getenv("PERPLEXITY_API_KEY")
        perplixty_llm = Perplexity(
            api_key=pplx_api_key,
            model="mixtral-8x7b-instruct",
            temperature=0.5
        )

        # perplexityMessage = perplixty_llm.complete(query).text

        perplexityMessage = """The search results don't contain specific information about deploying a Next.js application with Restack. However, I can provide you with the general steps to deploy a Next.js application:
        First, ensure your Next.js application is properly set up with the required scripts in your package.json1:
        json
        "scripts": {
          "dev": "next dev",
          "build": "next build",
          "start": "next start",
          "lint": "next lint"
        }
        To deploy your application, follow these steps:
        Build your application for production by running12:
        bash
        npm run build
        Start the production server12:
        bash
        npm start
        Your Next.js application will be optimized for production, with compiled and minified JavaScript for optimal performance2.
        For specific instructions about deploying with Restack, you would need to consult Restack's official documentation, as the provided search results don't contain this information.



        """


        # Create chat messages
        # messages = [
        #     ChatMessage(role="system", content="Be precise and concise."),
        #     ChatMessage(role="user", content=query)
        # ]

        try:
            # Call the Perplexity LLM with the messages
            # perplexityMessage = perplixty_llm.chat(messages).message.content
            return perplexityMessage
        except Exception as e:
            log.error("Perplexity API call failed", error=str(e))
            raise Exception(f"Perplexity API error: {str(e)}")

    except Exception as e:
        log.error("perplexityAgent function failed", error=e)
        raise e
