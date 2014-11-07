"""A bspline drawer."""

import random

import numpy
from scipy import interpolate


class BSpline(object):
  """Creates a basis spline."""
  def __init__(self, control_points, jitter=None):
    self.control_points = control_points
    self.control_x = [p[0] for p in self.control_points]
    self.control_y = [p[1] for p in self.control_points]
    control_range = range(len(self.control_x))

    if jitter:
      perturb_values_in_list(self.control_x, jitter)
      perturb_values_in_list(self.control_y, jitter)

    knots = [2, 3, 4]
    ipl_t = numpy.linspace(0.0, len(self.control_points) - 1, 100)

    x_tup = interpolate.splrep(control_range, self.control_x, k=3, t=knots)
    y_tup = interpolate.splrep(control_range, self.control_y, k=3, t=knots)
    self.x = interpolate.splev(ipl_t, x_tup)
    self.y = interpolate.splev(ipl_t, y_tup)


def perturb_values_in_list(array, jitter_value):
  """Adjust each element in an array in-place by some value."""
  for i in range(len(array)):
    sign = random.choice((-1, 1))
    perturbation = sign * random.random() * jitter_value
    array[i] += perturbation
