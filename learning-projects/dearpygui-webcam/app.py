from __future__ import annotations
from abc import ABC, abstractmethod

from dataclasses import dataclass
import numpy as np

from use_case import Webcam
    

@dataclass
class Application:
    webcam: Webcam
    view: View
    paused: bool = False
    brightness: int = 0

    def update_webcam_frame(self):
        if not self.paused:
            frame = self.webcam.get_frame()
            frame += self.brightness
            self.view.update_image(image=frame)

    def toggle_pause(self):
        self.paused = not self.paused
        self.view.set_pause_button_label('Run' if self.paused else 'Pause')

    def adjust_brightness(self, value: float):
        self.brightness = value
        self.view.set_brightness(self.brightness)
        

class View(ABC):

    @abstractmethod
    def update_image(self, image: np.ndarray): ...

    @abstractmethod
    def set_pause_button_label(self, label: str) -> None: ...

    @abstractmethod
    def set_brightness(self, value: float) -> None: ...



class Webcam(ABC):
    @abstractmethod
    def get_frame(self) -> np.ndarray: ...


