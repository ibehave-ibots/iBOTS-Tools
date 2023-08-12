from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import dearpygui.dearpygui as dpg

from gui import dpg_utils
from gui.gui import setup_gui, update_gui
from utils import repeat

if TYPE_CHECKING:
    from main import AppData

def run(proc_data: AppData = None):

    if proc_data is None:
        proc_data = {'x': [2, 3, 4], 'y': [4, 4.5, 6]}
    with dpg_utils.create_context(vsync=False):
        setup_gui()
        asyncio.ensure_future(repeat(dpg.render_dearpygui_frame, dt=.015, run_cond=dpg.is_dearpygui_running))
        asyncio.ensure_future(repeat(update_gui, data=(proc_data,), dt=.002, run_cond=dpg.is_dearpygui_running))
        asyncio.get_event_loop().run_forever()