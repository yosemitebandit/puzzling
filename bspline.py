"""A bspline drawer."""
import numpy
from scipy import interpolate


class BSpline(object):
  """Creates a basis spline."""
  def __init__(self, control_points):
    self.control_points = control_points

    self.control_x, self.control_y = zip(*self.control_points)
    control_range = range(len(self.control_x))

    knots = [2, 3, 4]
    ipl_t = numpy.linspace(0.0, len(self.control_points) - 1, 100)

    x_tup = interpolate.splrep(control_range, self.control_x, k=3, t=knots)
    y_tup = interpolate.splrep(control_range, self.control_y, k=3, t=knots)
    self.x = interpolate.splev(ipl_t, x_tup)
    self.y = interpolate.splev(ipl_t, y_tup)
