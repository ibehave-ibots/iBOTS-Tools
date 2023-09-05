from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import dearpygui.dearpygui as dpg

from app import View, Observer


@dataclass
class DPGView(View):
    image_view: np.ndarray = field(default_factory=lambda: np.ones((480, 640, 4), dtype=np.float32))
    observers: list = field(default_factory=list)

    def register(self, observer: Observer) -> None:
        self.observers.append(observer)

    def __enter__(self):
        dpg.create_context()

        with dpg.texture_registry(show=False):
            dpg.add_raw_texture(
                width=self.image_view.shape[1],
                height=self.image_view.shape[0],
                default_value=self.image_view,
                tag='texture-webcam',
            )

        with dpg.window(label='WebCam'):
            dpg.add_image("texture-webcam")
            dpg.add_button(tag='pause-button', label='Pause', callback=self.on_pause_button_clicked)

        dpg.create_viewport(title='DearPyGuiCam', width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        return self
        
    def __exit__(self, type, value, tb):
        dpg.destroy_context()

    def update_image(self, image) -> None:
        self.image_view[:, :, :3] = image / 255

    def set_pause_button_label(self, label):
        dpg.set_item_label(item='pause-button', label=label)

    def run(self):
        while dpg.is_dearpygui_running():
            self.on_frame_update()
            dpg.render_dearpygui_frame()
