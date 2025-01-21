
from restack_ai.function import function, log
from typing import Any
from pydantic import BaseModel

# Add your imports here


class write_restack_functionInput(BaseModel):
    # Add your input fields here
    pass

@function.defn()
async def write_restack_function(input: write_restack_functionInput):
    try:
        # Your function logic here
        pass
    except Exception as error:
        log.error("%!s(MISSING) function failed", error=error)
        raise error


# ------------------------------------------------------------------------------------------------

# Add this function in services.py file when your function is ready
# to the respective service and workflow config

# Example:

# client.start_service(
#            workflows=[<ThisWorkflowName>],
#            functions=[<this_function_name>],
#            options=ServiceOptions(
#                endpoints= True,
#                max_concurrent_function_runs=1
#            )
#        ),



-------  or  -------

# client.start_service(
#     functions=[<this_function_name>],
#     task_queue="<task_queue_name>", # could be whatever you prefer
#     options=ServiceOptions(
#         rate_limit=1,
#         max_concurrent_function_runs=1
#     )
		# ),


# ------------------------------------------------------------------------------------------------
