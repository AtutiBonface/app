import asyncio

async def example_queue_usage():
    queue = asyncio.Queue()

    # Add some items to the queue
    await queue.put('item1')
    await queue.put('item2')
    await queue.put('item3')
    await queue.put('item2')
    await queue.put('item3')
    await queue.put('item2')
    await queue.put('item3')
    await queue.put('item2')
    await queue.put('item3')
    await queue.put('item2')
    await queue.put('item3')
    await queue.put('item2')
    await queue.put('item3')

    # Check the size of the queue
    size = queue.qsize()
    while not queue.empty():
        item = await queue.get()
        print(item)
        queue.task_done()

    print(size)

# Run the example coroutine
asyncio.run(example_queue_usage())