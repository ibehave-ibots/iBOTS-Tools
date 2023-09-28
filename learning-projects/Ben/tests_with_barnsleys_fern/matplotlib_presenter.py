import matplotlib.pyplot as plt
from presenter import Presenter
from typing import List, Tuple


class MatplotlibPresenter(Presenter):

    def show(self, points: List[Tuple[float,float]]):
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        plt.scatter(xs,ys, s=0.1, c='g', marker='s',linewidth=0)
        plt.axis('off')
        plt.savefig('fern.png', dpi=300, bbox_inches='tight')


