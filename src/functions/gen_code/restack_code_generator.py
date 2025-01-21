from restack_ai.function import function, log
from pydantic import BaseModel
from google import genai
from google.genai import types
import subprocess


import os

@function.defn()
def use_cli(command: str) -> str:
    """Generates workflow or function based on the 

    Args:
        command from the list of commands
    """
    

    try:
        # Split the command into workflow or function
        cmd_parts = command.split()
        if len(cmd_parts) != 2:
            raise ValueError("Command must be in format: 'workflow name' or 'function name'")

        cmd_type, name = cmd_parts

        # Validate command type
        if cmd_type not in ['workflow', 'function']:
            raise ValueError("Command type must be either 'workflow' or 'function'")

        # Construct and execute the restack CLI command
        restack_cmd = ['./restack_cli', cmd_type, name]
        result = subprocess.run(restack_cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Command failed with error: {result.stderr}")

        return result.stdout

    except Exception as e:
        log.error(f"Error executing restack CLI command: {str(e)}")
        raise e




@function.defn()
async def restack_code_gen(input):
    try:
        log.info("gemini_multi_function_call function started", input=input)
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

        user_query = input["query"]
        
        prompt = f"""Based on the following user request, determine if they need a workflow or a function. 
        A workflow is needed when the request involves multiple steps, automation, or coordination between different services.
        A function is needed for single, specific tasks or operations.

        User request: {user_query}

        Analyze the request and respond with either 'workflow' or 'function' or False followed by a suggested name (in snake_case).
        Format your response exactly as: "<type> <name>"
        Example: "workflow data_pipeline" or "function process_image"
        """
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt,
            config=types.GenerateContentConfig(tools=[use_cli])
        )
        
        # Use the model's response to call use_cli
        command = response.text.strip()
        result={}
        if command!=False:
            result = use_cli(command)
        
        log.info("gemini_multi_function_call function completed", response=result)
        return {"command": command, "result": result}
    except Exception as e:
        log.error("gemini_multi_function_call function failed", error=e)
        raise e