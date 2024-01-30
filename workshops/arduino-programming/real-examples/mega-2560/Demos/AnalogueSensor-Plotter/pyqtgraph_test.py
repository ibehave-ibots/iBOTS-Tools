import sys
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets
from collections import deque
import time

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, maxlen=100):
        super().__init__()
        
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.y_data = deque([], maxlen=maxlen)
        self.curve = self.plot_graph.plot( self.y_data)


    def add_new_data(self, y):
        self.y_data.append(y)
        
        # Update the plot with the new data
        self.curve.setData( self.y_data)
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    while True:
        main.add_new_data( np.random.randint(500, 1000))
        app.processEvents()
        time.sleep(0.01)
    
    sys.exit(app.exec_())