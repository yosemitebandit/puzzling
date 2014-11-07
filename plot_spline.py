"""Plotting a single spline."""

import matplotlib.pyplot as pyplot

import puzzle

if __name__ == '__main__':

  # setup a plotter
  figure = pyplot.figure()
  axes = figure.add_subplot(111)

  for _ in range(5):
    # setup a bspline
    control_points = [[0, 0], [7, 1],
                      [9, 0],
                      [8, -2], [10, -3], [12, -2],
                      [11, 0],
                      [13, 1], [20, 0]]
    spline = puzzle.BSpline(control_points, jitter=0.75)
    # plot
    axes.plot(spline.x, spline.y)

  # format and save
  axes.set_xlim([min(spline.x) - 1.0, max(spline.x) + 1.0])
  axes.set_ylim([min(spline.y) - 1.0, max(spline.y) + 1.0])
  axes.set_aspect('equal')
  figure.set_size_inches(18, 10)
  figure.savefig('/tmp/test.png', dpi=100)
