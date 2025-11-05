import asyncio
import os
import random

import uvicorn
from fastapi import FastAPI
from temporalio import worker
from temporalio.client import Client

from producers.workflows import CalculateWorkflow

app = FastAPI()

temporal_address = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")


async def get_client() -> Client:
    return await Client.connect(temporal_address)


@app.post("/")
async def create_workflow(number: int):
    client = await get_client()
    handle = await client.start_workflow(
        CalculateWorkflow.run,  # Use the workflow class method
        number,
        id=f"calculate-{number}-{random.randint(0, 10000)}",
        task_queue="calculation-task-queue",
    )

    return {"message": "workflow started", "workflow_id": handle.id}


@app.get("/result/{workflow_id}")
async def get_workflow_result(workflow_id: str):
    try:
        client = await get_client()
        handle = client.get_workflow_handle(workflow_id)
        result = await handle.result()
        return {"message": "completed", "result": result}
    except Exception as e:
        return {"message": "workflow not completed or failed", "error": str(e)}


async def run_worker():
    """Run the Temporal worker"""
    client = await get_client()
    worker_instance = worker.Worker(
        client,
        task_queue="calculation-task-queue",
        workflows=[CalculateWorkflow],
    )
    await worker_instance.run()


async def run_server():
    """Run the FastAPI server"""
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    """Run both the FastAPI server and Temporal worker concurrently"""
    await asyncio.gather(
        run_server(),
        run_worker(),
    )


if __name__ == "__main__":
    asyncio.run(main())
