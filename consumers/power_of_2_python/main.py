import logging
import os

from temporalio import worker
from temporalio.client import Client

from consumers.power_of_2_python.activities import power_of_2

temporal_address = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")

logger = logging.getLogger(__name__)


async def get_client() -> Client:
    return await Client.connect(temporal_address)


async def main():
    # Create a worker that hosts the activity
    client = await get_client()
    worker_instance = worker.Worker(
        client,
        task_queue="power-of-2-service-queue",
        activities=[power_of_2],
        max_concurrent_activities=5,  # Limit heavy computation activities
    )
    await worker_instance.run()


if __name__ == "__main__":
    import asyncio

    logging.basicConfig(level=logging.INFO)
    logger.info("Starting Power of 2 Worker...")
    asyncio.run(main())
