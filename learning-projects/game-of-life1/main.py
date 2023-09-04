
import dearpygui.dearpygui as dpg
import numpy as np


def display_values(): 
    print(dpg.get_value(height),dpg.get_value(width))


def update_matrix_size():
    width_value =  dpg.get_value(width)
    height_value =  dpg.get_value(height)
    print("update", width_value, height_value)
    texture_data = []
    for i in range(0, width_value * height_value):
        col = np.random.random()
        print(col)
        texture_data.extend([0, col, 0 ,1])

    texture_data= np.random(0,1, size=())

    print('Length : ', len(texture_data))
    with dpg.texture_registry(show=True):
        dpg.add_static_texture(width=width_value,
                                height=height_value,
                                default_value=texture_data, 
                                tag="texture_tag")

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=300)

with dpg.window(label="The Game of Life"):
    height = dpg.add_input_int(label="height")
    width = dpg.add_input_int(label="width")
    dpg.add_button(label="print size", callback=display_values)
    dpg.add_button(label="update", callback=update_matrix_size)



dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()