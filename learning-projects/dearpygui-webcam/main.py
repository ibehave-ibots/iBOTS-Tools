from __future__ import annotations

from gui import DPGController, DPGPresenter
from webcam_opencv import OpenCVWebcam


controller = DPGController(
    webcam=OpenCVWebcam(),
    presenter=DPGPresenter()
)
   
with controller:
    controller.run()


    