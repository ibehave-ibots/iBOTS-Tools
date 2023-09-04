
import dearpygui.dearpygui as dpg


def display_values(): 
    print(dpg.get_value(height),dpg.get_value(width))

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=300)

with dpg.window(label="The Game of Life"):
    height = dpg.add_input_int(label="height")
    width = dpg.add_input_int(label="width")
    dpg.add_button(label="print size", callback=display_values)



dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()