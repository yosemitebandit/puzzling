"""Components of a puzzle."""

import math
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

  def scale(self, distance):
    """Scale x and y by some factor."""
    start = Point(self.x[0], self.y[0])
    end = Point(self.x[-1], self.y[-1])
    original_distance = calculate_distance(start, end)
    scale_factor = original_distance / distance
    self.x = [x / scale_factor for x in self.x]
    self.y = [y / scale_factor for y in self.y]

  def rotate(self, angle):
    """Rotate x and y by some angle."""
    rotation_matrix = numpy.matrix([[math.cos(angle), math.sin(angle)],
                                    [-1 * math.sin(angle), math.cos(angle)]])
    rotated_x, rotated_y = [], []
    for i in range(len(self.x)):
      vector = numpy.matrix(numpy.array([self.x[i], self.y[i]]))
      rotated_vector = rotation_matrix * vector.T
      # :|
      rotated_vector = rotated_vector.ravel().tolist()[0]
      rotated_x.append(rotated_vector[0])
      rotated_y.append(rotated_vector[1])
    self.x = rotated_x
    self.y = rotated_y

  def translate(self, anchor_point):
    """Translate all points such that the spline starts at some anchor."""
    self.x = [x + anchor_point.x for x in self.x]
    self.y = [y + anchor_point.y for y in self.y]


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
  def __init__(self, (M, N), golden_control_points):
    self.M, self.N = (M, N)
    self.golden_control_points = golden_control_points
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
        # setup the start point for comparison
        start = self.mesh[m][n]

        # check the point below the start
        if m < self.M-1:
          below = self.mesh[m+1][n]

          # if it's directly below, this is an edge, so just create a line
          if abs(start.x - below.x) == 1:
            segments.append(([start.x, below.x], [start.y, below.y]))

          # if there's an offset, this is an interior segment: draw a bspline
          else:
            spline = BSpline(self.golden_control_points, jitter=0.75)
            # transform it via scaling, rotation and translation
            # such that the spline's endpoints match 'start' and 'below'
            spline.scale(calculate_distance(start, below))
            spline.rotate(calculate_angle(start, below))
            spline.translate(start)
            segments.append((spline.x, spline.y))

        # now check the point to the right of the start
        if n < self.N-1:
          right = self.mesh[m][n+1]

          # if it's directly right, this is an edge, so just create a line
          if abs(start.y - right.y) == 1:
            segments.append(([start.x, right.x], [start.y, right.y]))

          # if there's an offset, this is an interior segment: draw a bspline
          else:
            spline = BSpline(self.golden_control_points, jitter=0.75)
            # transform it via scaling, rotation and translation
            # such that the spline's endpoints match 'start' and 'right'
            spline.scale(calculate_distance(start, right))
            spline.rotate(calculate_angle(start, right))
            spline.translate(start)
            segments.append((spline.x, spline.y))

    return segments


def calculate_angle(p1, p2):
  """Returns angle between two points in radians."""
  '''
  x_dist = p2.x - p1.x
  hypotenuse = calculate_distance(p1, p2)
  return math.acos(x_dist / hypotenuse)
  '''
  x_dist = p2.x - p1.x
  y_dist = p2.y - p1.y
  return math.atan2(y_dist, x_dist)


def calculate_distance(p1, p2):
  return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def perturb_values_in_list(array, scaling):
  """Adjust each element in an array in-place by some value."""
  for i in range(len(array)):
    # start and endpoints are left untouched
    if i == 0 or i == len(array)-1:
      continue
    # other points get perturbed by some amount
    sign = random.choice((-1, 1))
    array[i] += sign * random.random() * scaling
