import cv2
import numpy as np
from dearpygui import dearpygui as dpg

image_view = np.ones((480, 640, 4), dtype=np.float32)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Callback function to update the image texture
def update_image():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (640, 480))
        frame = np.ascontiguousarray(frame)
        image_view[:, :, :3] = frame / 255



dpg.create_context()

with dpg.texture_registry(show=False):
    dpg.add_raw_texture(
        width=640,
        height=480,
        default_value=image_view,
        tag='texture-webcam',
    )

with dpg.window(label='WebCam'):
    dpg.add_image("texture-webcam")

dpg.create_viewport(title='DearPyGuiCam', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
while dpg.is_dearpygui_running():
    update_image()
    dpg.render_dearpygui_frame()

dpg.destroy_context()
    