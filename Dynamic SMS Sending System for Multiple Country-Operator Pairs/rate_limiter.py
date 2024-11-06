import asyncio

async def rate_limit(tasks, limit=10):
    """
    Limits the execution of tasks to a specified rate.

    Parameters:
    - tasks: List of coroutine tasks to be executed.
    - limit: The maximum number of tasks to execute within the rate period.

    Example usage:
        tasks = [asyncio.create_task(your_function(...)) for _ in range(10)]
        await rate_limit(tasks)
    """
    for i in range(0, len(tasks), limit):
        # Get a chunk of tasks based on the limit
        chunk = tasks[i:i + limit]
        
        # Run these tasks concurrently
        await asyncio.gather(*chunk)
        
        # Wait 6 seconds to comply with "10 tasks per minute" (60 sec / 10)
        await asyncio.sleep(6)
