from fern import Fern
from transformation_values import trans_list
from matplotlib_presenter import MatplotlibPresenter


number_of_points = 1e6
fern = Fern(trans_list)
fern.calc_points(int(number_of_points))
#fern.save_points('fern.dat')

presenter = MatplotlibPresenter()
presenter.show(fern.points)
