from abc import ABC, abstractmethod
from typing import List, Tuple
from numpy.random import choice


class Transformation:
    def __init__(self, matrix, offset, probability: float): # as long as matrix and offset are indexable with shapes (2,2) and (1,2), I don't care what type they are. List, array, np.matrix etc...
        self.zero_zero : float = matrix[0][0]
        self.zero_one : float = matrix[0][1]
        self.one_zero : float = matrix[1][0]
        self.one_one : float = matrix[1][1]

        self.x_offset : float = offset[0]
        self.y_offset : float = offset[1]

        self.probability = probability



class Fern:

    def __init__(self, transformations: List[Transformation]):
        self.points: List[(float,float)] = [(0,0)]
        self.transformations = transformations
        self.probabilities: List[float] = [t.probability for t in transformations]
        
    def get_next_transform(self) -> Transformation:
        transformation_index = choice(range(0, len(self.transformations)), 
                            p=self.probabilities)
        return self.transformations[transformation_index]

    def apply_transformation(self,
                                transformation: Transformation,
                                start_point:Tuple[float,float]
                            )-> Tuple[float,float]:
        x_next = transformation.zero_zero * start_point[0] +\
                transformation.zero_one * start_point[1] + \
                transformation.x_offset
        y_next =  transformation.one_zero * start_point[0] + \
                transformation.one_one * start_point[1] + \
                transformation.y_offset
    
        return (x_next, y_next)
         
    def calc_next_point(self) -> None:
        transformation_to_apply = self.get_next_transform()
        new_point =self.apply_transformation(transformation_to_apply, self.points[-1])
        self.points.append(new_point)
              
    def calc_points(self, n: int) -> None:
        for i in range(1, n):
            self.calc_next_point()
            if 100*(i/n)%1 ==0: 
                perc_complete =int(100*(i/n))
                print(f"calculating: {perc_complete} %", end = '\r')


    def save_points(self, filename:str) -> None:
        with open(filename, 'w') as f:
            f.write('x,y\n')
            for p in self.points:
                f.write('%.5f, %.5f\n' %(p[0], p[1]))

   
