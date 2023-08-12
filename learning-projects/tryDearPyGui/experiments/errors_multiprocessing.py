import tkinter as tk
import time
import multiprocessing as mp
from queue import Empty


def generate_layout_model():
    return {"text": "Hello, World!"}


def gui_process(layout_queue):
    def update_label():
        try:
            layout = layout_queue.get_nowait()
            label.config(text=layout["text"], fg=layout["color"])
        except Empty:
            pass

        root.after(1000, update_label)

    root = tk.Tk()
    root.title("GUI Framework")
    label = tk.Label(root, text="", font=("Arial", 14))
    label.pack(padx=20, pady=20)
    update_label()
    root.mainloop()


def layout_generator_process(layout_queue):
    while True:
        layout = generate_layout_model()
        layout_queue.put(layout)
        time.sleep(1)


if __name__ == "__main__":
    layout_queue = mp.Queue()

    gui = mp.Process(target=gui_process, args=(layout_queue,))
    layout_generator = mp.Process(target=layout_generator_process, args=(layout_queue,))

    gui.start()
    layout_generator.start()

    gui.join()
    layout_generator.join()