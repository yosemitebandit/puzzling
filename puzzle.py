"""Components of a puzzle."""

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


class Point(object):
  """2D point approximately on a unit grid."""
  def __init__(self, x, y, jitter=None):
    if jitter:
      sign = random.choice((-1, 1))
      self.x = x + sign * random.random() * jitter
      sign = random.choice((-1, 1))
      self.y = y + sign * random.random() * jitter
    else:
      self.x = x
      self.y = y

  def __repr__(self):
    return '%s,%s' % (self.x, self.y)


class Grid(object):
  """Manages an M row x N column grid."""
  def __init__(self, M, N):
    self.M, self.N = (M, N)
    self.mesh, self.points = [], []
    # init with empty rows
    for m in range(self.M):
      self.mesh.append([])

    # populate with points
    for m in range(self.M):
      for n in range(self.N):
        if m == 0 or n == 0 or m == self.M-1 or n == self.N-1:
          jitter_factor = 0
        else:
          jitter_factor = 0.1
        p = Point(m, n, jitter=jitter_factor)
        self.mesh[m].append(p)
        self.points.append(p)

    # setup convenience values
    self.min_x = min([p.x for p in self.points])
    self.max_x = max([p.x for p in self.points])
    self.min_y = min([p.y for p in self.points])
    self.max_y = max([p.y for p in self.points])

  def get_segments(self):
    """Returns unique edges between points."""
    segments = []
    for m in range(self.M):
      for n in range(self.N):
        start = self.mesh[m][n]
        # check point below
        if m < self.M-1:
          below = self.mesh[m+1][n]
          segments.append((start, below))
        # check point to the right
        if n < self.N-1:
          right = self.mesh[m][n+1]
          segments.append((start, right))
    return segments


def perturb_values_in_list(array, scaling):
  """Adjust each element in an array in-place by some value."""
  for i in range(len(array)):
    # start and endpoints are left untouched
    if i == 0 or i == len(array)-1:
      continue
    # other points get perturbed by some amount
    sign = random.choice((-1, 1))
    array[i] += sign * random.random() * scaling
