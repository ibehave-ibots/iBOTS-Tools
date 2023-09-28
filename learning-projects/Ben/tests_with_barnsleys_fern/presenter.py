from abc import ABC, abstractmethod
from typing import List, Tuple

    
class Presenter(ABC):

    @abstractmethod
    def show(self, points: List[Tuple[float,float]]):
        ...
        
    def load_points(self, filename: str) -> List[Tuple[float,float]]:
        points = []
        with open(filename, 'r') as f:
            first_line = f.readline()
            for line in f:
                x_val, y_val = line.split(',')
                x_val = float(x_val)
                y_val = float(y_val)
                points.append((x_val, y_val)) 

        return points
