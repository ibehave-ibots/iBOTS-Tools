
import asyncio
from typing import List, TypedDict
import multiprocessing as mp

import gui
import sensor


class AppData(TypedDict):
    x: List[int|float]
    y: List[int|float]


if __name__ == '__main__':
    manager = mp.Manager()
    data: AppData = manager.dict({'x': [1, 2, 5], 'y': [6, 8, 8.2]})

    gui_proc = mp.Process(target=gui.run, args=(data,))
    daq_proc = mp.Process(target=lambda: asyncio.run(sensor.simulate_data_update(data)), daemon=True)
    gui_proc.start()
    daq_proc.start()
    gui_proc.join()
    daq_proc.join()