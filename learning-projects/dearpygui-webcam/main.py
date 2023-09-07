from __future__ import annotations

from view_dpg import DPGView
from app import Application
from webcam_opencv import OpenCVWebcam
from imageproc_scipy import ScipyImageProcessor


view = DPGView()
controller = Application(webcam=OpenCVWebcam(), image_processor=ScipyImageProcessor())

controller.set_brightness.connect(view.set_brightness)
controller.set_pause_button_label.connect(view.set_pause_button_label)
controller.update_image.connect(view.update_image)
controller.image_rotation_updated.connect(view.update_image)
view.on_brightness_slider_update.connect(controller.adjust_brightness)
view.on_frame_update.connect(controller.update_webcam_frame)
view.on_pause_button_clicked.connect(controller.toggle_pause)
view.on_rotation_slider_update.connect(controller.set_image_rotation)

with view:
    view.run()