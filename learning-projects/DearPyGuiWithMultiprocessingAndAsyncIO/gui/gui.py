from typing import List, TypedDict
import dearpygui.dearpygui as dpg


class Model(TypedDict):
    x_data: List[int]
    y_data: List[int]


def build_model(app_data) -> Model:
    model: Model = {'x_data': app_data['x'], 'y_data': app_data['y']}
    return model


def update_gui(app_data):
    model: Model = build_model(app_data=app_data)
    dpg.set_value('line_series', [model['x_data'], model['y_data']])
    dpg.set_axis_limits('x_axis', ymin=min(model['x_data']), ymax=max(model['x_data']))
    # dpg.set_axis_limits('y_axis', ymin=min(model['y_data']), ymax=max(model['y_data']))


def setup_gui():
    with dpg.window(label='Plot'):
        with dpg.plot(label='Sine Wave', width=1200, height=600):
            x_axis = dpg.add_plot_axis(dpg.mvXAxis, label='X Axis', tag='x_axis')
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label='Y Axis', tag='y_axis')

            dpg.add_line_series(
                    [2, 3, 4, 5],
                    [-1, 0, 1, 0],
                    label='The Data',
                    parent=y_axis,
                    tag='line_series',
                )