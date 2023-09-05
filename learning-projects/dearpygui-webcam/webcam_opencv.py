from __future__ import annotations

from dataclasses import dataclass, field
import cv2
import numpy as np

from use_case import Webcam


@dataclass
class OpenCVWebcam(Webcam):
    cap: cv2.VideoCapture = field(default_factory=lambda: cv2.VideoCapture(0))

    def get_frame(self) -> np.ndarray:
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            return frame
   