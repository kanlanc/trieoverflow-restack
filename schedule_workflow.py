import asyncio
import time
from restack_ai import Restack
from src.workflows.workflow import GreetingWorkflowInput
async def main():

    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-query_question_workflow"
    run_id = await client.schedule_workflow(
        workflow_name="query_question_workflow",
        workflow_id=workflow_id,
        input="How can I fix the os.stat error that I keep getting"
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