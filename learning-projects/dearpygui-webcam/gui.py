from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np
from dearpygui import dearpygui as dpg

from use_case import Presenter, Webcam, ViewWebcamFrameWorkflow

@dataclass
class DPGPresenter(Presenter):
    image_view: np.ndarray = field(default_factory=lambda: np.ones((480, 640, 4), dtype=np.float32))

    def update_image(self, image) -> None:
        self.image_view[:, :, :3] = image / 255



@dataclass
class DPGController:
    presenter: DPGPresenter
    webcam: Webcam
    paused: bool = False


    def __enter__(self):
        dpg.create_context()

        with dpg.texture_registry(show=False):
            dpg.add_raw_texture(
                width=640,
                height=480,
                default_value=self.presenter.image_view,
                tag='texture-webcam',
            )

        with dpg.window(label='WebCam'):
            dpg.add_image("texture-webcam")
            dpg.add_button(tag='pause-button', label='Pause', callback=self.pause)
            

        dpg.create_viewport(title='DearPyGuiCam', width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        return self
        

    def __exit__(self, type, value, tb):
        dpg.destroy_context()

    def pause(self):
        self.paused = not self.paused
        dpg.set_item_label(item='pause-button', label='Run' if self.paused else 'Pause')

    def run(self):
        while dpg.is_dearpygui_running():
            if not self.paused:
                app = ViewWebcamFrameWorkflow(presenter=self.presenter, webcam=self.webcam)
                app.show_webcam_frame()
            dpg.render_dearpygui_frame()




