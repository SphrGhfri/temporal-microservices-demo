import os
from asyncio import sleep

from temporalio import activity

wait_timeout = int(os.getenv("ACTIVITY_1_WAIT_TIMEOUT", "5"))


@activity.defn(name="power_of_2")
async def power_of_2(a: int) -> int:
    await sleep(wait_timeout)
    return a**2
