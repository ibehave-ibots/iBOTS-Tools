from __future__ import annotations
from abc import ABC, abstractmethod

from dataclasses import dataclass
import numpy as np

from use_case import Webcam
from webcam_opencv import OpenCVWebcam


        
class Observer(ABC):

    @abstractmethod
    def notify(self, event: str) -> None: ...
    

@dataclass
class Application(Observer):
    webcam: Webcam
    view: View
    paused: bool = False

    def __post_init__(self):
        self.view.register(self)

    def notify(self, event: str):
        match event:
            case 'pause-button-clicked': self.toggle_pause()
            case 'frame-updating': self.update_webcam_frame()

    def update_webcam_frame(self):
        if not self.paused:
            frame = self.webcam.get_frame()
            self.view.update_image(image=frame)

    def toggle_pause(self):
        self.paused = not self.paused
        self.view.set_pause_button_label('Run' if self.paused else 'Pause')

        

class View(ABC):

    @abstractmethod
    def register(self, observer: Observer) -> None: ...

    @abstractmethod
    def update_image(self, image: np.ndarray): ...

    @abstractmethod
    def set_pause_button_label(self, label: str) -> None: ...

    def on_frame_update(self):
        for observer in self.observers:
            observer.notify('frame-updating')

    def on_pause_button_clicked(self):
        for observer in self.observers:
            observer.notify('pause-button-clicked')



class Webcam(ABC):
    @abstractmethod
    def get_frame(self) -> np.ndarray: ...


