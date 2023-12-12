import dearpygui.dearpygui as dpg
from multiprocessing import Process, Manager
import time



def setup(data):
    # Setup
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()
    dpg.show_viewport()


    with dpg.window(label='win'):
        dpg.add_button(label='Hi!', tag='button')

    # Update and Render Loop
    while dpg.is_dearpygui_running():
        dpg.set_item_label('button', data['time'])
        dpg.render_dearpygui_frame()

    # Cleanup
    dpg.destroy_context()


def log_time(data):
    while True:
        time.sleep(.001)
        current = time.time()
        data['time'] = current
        print(current)


def manage_app(timer_model, render_model):
    while True:
        time.sleep(0)
        render_model['time'] = str(round(timer_model['time'], 2))


manager = Manager()
timer_model = manager.dict(time=3.14)
render_model = manager.dict(time='3.123424242324324')


gui_proc = Process(target=setup, kwargs=dict(data=render_model))
timer_proc = Process(target=log_time, kwargs=dict(data=timer_model), daemon=True)
main_proc = Process(target=manage_app, kwargs=dict(timer_model=timer_model, render_model=render_model), daemon=True)

gui_proc.start()
timer_proc.start()
main_proc.start()
gui_proc.join()
gui_proc.close()
timer_proc.terminate()
main_proc.terminate()
while timer_proc.is_alive() or main_proc.is_alive():  # There's a bit of delay before the terminate() call actually takes effect.
    pass
timer_proc.close()
main_proc.close()
print('done!')
