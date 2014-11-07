"""Plotting a single spline."""

import matplotlib.pyplot as pyplot

import bspline

if __name__ == '__main__':
  # setup a single bspline
  control_points = [[0, 0], [7, 1],
                    [9, 0],
                    [8, -2], [10, -3], [12, -2],
                    [11, 0],
                    [13, 1], [20, 0]]
  spline = bspline.BSpline(control_points)

  # plot
  figure = pyplot.figure()
  axes = figure.add_subplot(111)
  axes.plot(spline.control_x, spline.control_y, 'b.', label='control')
  axes.plot(spline.x, spline.y, 'g-', label='spline')

  # format and save
  axes.set_xlim([min(spline.x) - 1.0, max(spline.x) + 1.0])
  axes.set_ylim([min(spline.y) - 1.0, max(spline.y) + 1.0])
  axes.set_aspect('equal')
  figure.set_size_inches(18, 10)
  figure.savefig('/tmp/test.png', dpi=100)