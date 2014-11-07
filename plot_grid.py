"""Plotting a single spline."""

import matplotlib.pyplot as pyplot

import puzzle

if __name__ == '__main__':

  # setup a plotter
  figure = pyplot.figure()
  axes = figure.add_subplot(111)

  # setup a grid
  grid = puzzle.Grid(4, 5)
  segments = grid.get_segments()
  print 'number of segments:', len(segments)

  # plot
  axes.plot([p.x for p in grid.points], [p.y for p in grid.points], 'b.')

  # format and save
  axes.set_xlim([grid.min_x - 1.0, grid.max_x + 1.0])
  axes.set_ylim([grid.min_y - 1.0, grid.max_y + 1.0])
  axes.set_aspect('equal')
  figure.set_size_inches(18, 10)
  figure.savefig('/tmp/grid.png', dpi=100)
