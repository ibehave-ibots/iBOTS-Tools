from __future__ import annotations

from view_dpg import DPGView
from app import Application
from webcam_opencv import OpenCVWebcam


view = DPGView()
controller = Application(webcam=OpenCVWebcam(), view=view)
with view:
    view.run()