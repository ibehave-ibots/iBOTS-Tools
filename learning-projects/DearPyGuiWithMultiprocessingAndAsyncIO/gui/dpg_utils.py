from __future__ import annotations

import asyncio
from contextlib import contextmanager
from typing import NamedTuple

import dearpygui.dearpygui as dpg


@contextmanager
def create_context(vsync: bool = True):
    dpg.create_context()
    dpg.create_viewport()
    dpg.set_viewport_vsync(vsync)  # if vsync is off, it's nonblocking
    dpg.setup_dearpygui()
    dpg.show_viewport()
    # dpg.render_dearpygui_frame()
    yield
    dpg.destroy_context()



class FrameData(NamedTuple):
    num: int
    dt: float = 0

    def __repr__(self) -> str:
        return f"FrameData(num={self.num}, dt={round(self.dt, 4)})"
        



async def handle_shutdown(loop):
    while dpg.is_dearpygui_running():
        await asyncio.sleep(0.01)
    loop.stop()


   