from __future__ import annotations
import asyncio
from collections import deque
from pathlib import Path
import struct
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import AppData

        
async def simulate_data_update(proc_data: AppData):
    n = 50000
    t_queue = deque(maxlen=n)   
    y_queue = deque(maxlen=n)
    dt = None
    async for readings in connect_to_sensor():
        t, y = list(zip(*list(readings)))
        t_queue.extend(t)
        y_queue.extend(y)
        if len(t_queue) > 2:
            if dt is None:
                dt = t_queue[-1] - t_queue[-2]
                print(1 / dt)
            s = int(4 / dt)
            proc_data.update({'x': list(t_queue)[-s:], 'y': list(y_queue)[-s:]})
        
        
async def connect_to_sensor():
    program_path = str(Path(__file__).parent / 'run_sensor.py')
    proc = await asyncio.create_subprocess_exec('python', program_path, stdout=asyncio.subprocess.PIPE)
    while True:
        out = await proc.stdout.read(16*3000, )
        readings = struct.iter_unpack('dd', out)
        yield readings
    

if __name__ == '__main__':
    asyncio.run(connect_to_sensor())
        


    



