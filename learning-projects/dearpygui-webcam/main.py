from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np
from dearpygui import dearpygui as dpg

from gui import DPGController, DPGPresenter
from webcam_opencv import OpenCVWebcam




## Main

controller = DPGController(
    webcam=OpenCVWebcam(),
    presenter=DPGPresenter()
)
   
with controller:
    controller.run()


    