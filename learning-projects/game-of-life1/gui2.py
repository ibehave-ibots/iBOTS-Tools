import dearpygui.dearpygui as dpg
import numpy as np
from app import create_random_board, update_board_state

board = create_random_board(500, 500)

dpg.create_context()

def update_board():
    board[:] = update_board_state(board)
    update_texture(board)

def update_texture(board):
    texture_data = []
    for cell_state in board.flatten():
        if cell_state:
            texture_data.extend([0, 0, 0, 1])
        else:
            texture_data.extend([1, 1, 1, 1])
    dpg.set_value("texture_tag", texture_data)
    print(np.mean(texture_data), texture_data[:6])

with dpg.texture_registry(show=True):
    dpg.add_dynamic_texture(width=500, height=500, default_value=[1]*500*500*4, tag="texture_tag")


with dpg.window(label="Tutorial"):
    dpg.add_image("texture_tag")
    dpg.add_button(label="print size", callback=update_board)

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
# dpg.start_dearpygui()
while dpg.is_dearpygui_running():
    update_board()
    dpg.render_dearpygui_frame()

dpg.destroy_context()