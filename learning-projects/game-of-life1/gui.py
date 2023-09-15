import dearpygui.dearpygui as dpg
import numpy as np
from app import create_random_board, update_board_state

board = create_random_board(500, 500)
board_view = np.ones((board.shape[0], board.shape[1], 4), dtype=np.float32)

dpg.create_context()

def update_board():
    board[:] = update_board_state(board)
    board_view[:, :, 0] = board
    board_view[:, :, 1] = board
    board_view[:, :, 2] = board
    
with dpg.texture_registry(show=True):
    dpg.add_raw_texture(
        width=board_view.shape[1], 
        height=board_view.shape[0], 
        default_value=board_view,#.flatten(order='A'), 
        format=dpg.mvFormat_Float_rgba,
        tag="texture_tag"
    )


with dpg.window(label="Tutorial"):
    dpg.add_image("texture_tag")

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
while dpg.is_dearpygui_running():
    update_board()
    dpg.render_dearpygui_frame()

dpg.destroy_context()