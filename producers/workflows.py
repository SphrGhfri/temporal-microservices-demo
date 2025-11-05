from datetime import timedelta

from temporalio import workflow


@workflow.defn
class CalculateWorkflow:
    @workflow.run
    async def run(self, number: int) -> int:
        result = await workflow.execute_activity(
            "power_of_2",
            number,
            start_to_close_timeout=timedelta(seconds=100),
            task_queue="power-of-2-service-queue",
        )
        result = await workflow.execute_activity(
            "power_of_4",
            result,
            start_to_close_timeout=timedelta(seconds=100),
            task_queue="power-of-4-service-queue",
        )
        result = await workflow.execute_activity(
            "power_of_6",
            result,
            start_to_close_timeout=timedelta(seconds=100),
            task_queue="power-of-6-service-queue",
        )
        return result
