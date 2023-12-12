import dearpygui.dearpygui as dpg
import time
import matplotlib.pyplot as plt

dpg.create_context()

dpg.create_viewport()
dpg.set_viewport_vsync(False)  # if vsync is off, it's nonblocking
dpg.setup_dearpygui()
dpg.show_viewport()

dts = []

last_time = time.perf_counter()
for _ in range(200):
    dpg.render_dearpygui_frame()
    current_time = time.perf_counter()
    # time.sleep(.01)
    dt = current_time - last_time
    last_time = current_time
    dts.append(dt)

dpg.destroy_context()


plt.hist(dts, bins=15)
plt.show()