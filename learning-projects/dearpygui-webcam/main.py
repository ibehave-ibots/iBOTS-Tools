from __future__ import annotations

from dataclasses import dataclass, field
import cv2
import numpy as np
from dearpygui import dearpygui as dpg



@dataclass
class DearPyGuiView:
    webcam: OpenCVWebcam
    image_view: np.ndarray = field(default_factory=lambda: np.ones((480, 640, 4), dtype=np.float32))

    def __enter__(self):
        dpg.create_context()

        with dpg.texture_registry(show=False):
            dpg.add_raw_texture(
                width=640,
                height=480,
                default_value=self.image_view,
                tag='texture-webcam',
            )

        with dpg.window(label='WebCam'):
            dpg.add_image("texture-webcam")

        dpg.create_viewport(title='DearPyGuiCam', width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        return self
        

    def __exit__(self, type, value, tb):
        dpg.destroy_context()

    def update_image(self, image) -> None:
        view.image_view[:, :, :3] = image / 255

    def run(self):
        while dpg.is_dearpygui_running():
            frame = self.webcam.get_frame()
            view.update_image(image=frame)
            dpg.render_dearpygui_frame()



@dataclass
class OpenCVWebcam:
    cap: cv2.VideoCapture = field(default_factory=lambda: cv2.VideoCapture(0))

    def get_frame(self) -> np.ndarray:
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            return frame
   
   
with DearPyGuiView(webcam=OpenCVWebcam()) as view:
    view.run()


    