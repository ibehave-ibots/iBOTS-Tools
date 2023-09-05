from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np


class Presenter(ABC):
    @abstractmethod
    def update_image(self, image: np.ndarray):...


class Webcam(ABC):
    @abstractmethod
    def get_frame(self) -> np.ndarray: ...


@dataclass
class ViewWebcamFrameWorkflow:
    presenter: Presenter
    webcam: Webcam

    def show_webcam_frame(self):
        frame = self.webcam.get_frame()
        self.presenter.update_image(image=frame)

