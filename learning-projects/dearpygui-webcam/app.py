from __future__ import annotations
from abc import ABC, abstractmethod

from dataclasses import dataclass
import numpy as np
    
from utils import Signal

@dataclass
class Application:
    webcam: Webcam
    paused: bool = False
    brightness: int = 0
    set_brightness = Signal()
    set_pause_button_label = Signal()
    update_image = Signal()

    def update_webcam_frame(self):
        if not self.paused:
            frame = self.webcam.get_frame()
            frame += self.brightness
            self.update_image.send(image=frame)

    def toggle_pause(self):
        self.paused = not self.paused
        self.set_pause_button_label.send('Run' if self.paused else 'Pause')

    def adjust_brightness(self, value: float):
        self.brightness = value
        self.set_brightness.send(self.brightness)
        

class Webcam(ABC):
    @abstractmethod
    def get_frame(self) -> np.ndarray: ...


