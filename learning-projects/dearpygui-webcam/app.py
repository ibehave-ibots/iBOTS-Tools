from __future__ import annotations
from abc import ABC, abstractmethod

from dataclasses import dataclass
import numpy as np
    
from utils import Signal


@dataclass
class Application:
    webcam: Webcam
    image_processor: ImageProcessor
    paused: bool = False
    rotation_deg: float = 0.
    brightness: int = 0
    set_brightness = Signal()
    set_pause_button_label = Signal()
    update_image = Signal()
    image_rotation_updated = Signal()

    def update_webcam_frame(self):
        if not self.paused:
            frame = self.webcam.get_frame()
            frame = self.image_processor.adjust_brightness(image=frame, brightness=self.brightness)
            frame = self.image_processor.rotate(image=frame, degrees=self.rotation_deg)
            assert isinstance(frame, np.ndarray)
            self.update_image.send(image=frame)

    def toggle_pause(self):
        self.paused = not self.paused
        self.set_pause_button_label.send('Run' if self.paused else 'Pause')

    def adjust_brightness(self, value: float):
        self.brightness = value
        self.set_brightness.send(self.brightness)

    def set_image_rotation(self, value: float):
        self.rotation_deg = value
        self.image_rotation_updated.send(self.rotation_deg)
        

class Webcam(ABC):

    @abstractmethod
    def get_frame(self) -> np.ndarray: ...


class ImageProcessor(ABC):
    
    @abstractmethod
    def rotate(self, image: np.ndarray, degrees: float) -> np.ndarray: ...

    @abstractmethod
    def adjust_brightness(self, image: np.ndarray, brightness: int) -> np.ndarray: ...