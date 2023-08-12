import asyncio



async def log(dt: float = .05):
    inc = 0
    while True:
        await asyncio.sleep(dt)
        inc += 1
        print('Message', inc)


async def repeat(fun, dt, run_cond = lambda: True, data = (), loop = None):
    """
    Runs a synchronous function repeatedly with the given data, sleeping for dt time. Stops loop if run_cond is falsy.
    """
    while run_cond():
        fun(*data)
        await asyncio.sleep(dt)

    current_loop = asyncio.get_event_loop() if loop is None else loop
    current_loop.stop()