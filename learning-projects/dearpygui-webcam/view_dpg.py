from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import dearpygui.dearpygui as dpg

from utils import Signal


@dataclass
class DPGView:
    image_view: np.ndarray = field(default_factory=lambda: np.ones((480, 640, 4), dtype=np.float32))
    observers: list = field(default_factory=list)
    on_frame_update = Signal()
    on_pause_button_clicked = Signal()
    brightness_slider_updated = Signal()
    rotation_slider_updated = Signal()
    

    def __enter__(self):
        dpg.create_context()

        with dpg.texture_registry(show=False):
            dpg.add_raw_texture(
                width=self.image_view.shape[1],
                height=self.image_view.shape[0],
                default_value=self.image_view,
                tag='texture-webcam',
            )

        with dpg.window(label='WebCam', height=800):
            dpg.add_image("texture-webcam")
            dpg.add_button(tag='pause-button', label='Pause', callback=self.on_pause_button_clicked.send)
            dpg.add_slider_int(min_value=0, max_value=50, default_value=0, callback=self._on_brightness_slider_update)
            dpg.add_slider_float(min_value=-90, max_value=90, default_value=0, callback=self._on_rotation_slider_update)

        dpg.create_viewport(title='DearPyGuiCam', width=800, height=800)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        return self

    def _on_rotation_slider_update(self, sender, app_data):
        return self.rotation_slider_updated.send(app_data)

    def _on_brightness_slider_update(self, sender, app_data):
        return self.brightness_slider_updated.send(app_data)
    

        
    def __exit__(self, type, value, tb):
        dpg.destroy_context()

    def update_image(self, image) -> None:
        self.image_view[:, :, :3] = image / 255

    def set_pause_button_label(self, label):
        dpg.set_item_label(item='pause-button', label=label)

    def run(self):
        while dpg.is_dearpygui_running():
            self.on_frame_update.send()
            dpg.render_dearpygui_frame()
