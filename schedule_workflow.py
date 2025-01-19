import asyncio
import time
from restack_ai import Restack


async def main():

    client = Restack()

    # input = {"query":"How do I deploy restack on the cloud"}

    input = {"query":"Write me a function in restack"}

    

    workflow_id = f"{int(time.time() * 1000)}-query_question_workflow"
    run_id = await client.schedule_workflow(
        workflow_name="query_question_workflow",
        workflow_id=workflow_id,
        input=input
    )

    await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=run_id
    )

    exit(0)

def run_schedule_workflow():
    asyncio.run(main())

if __name__ == "__main__":
    run_schedule_workflow()