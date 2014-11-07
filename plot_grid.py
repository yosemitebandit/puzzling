"""Plotting a single spline."""

import matplotlib.pyplot as pyplot

import puzzle

# good starting point for a puzzle piece edge
control_points = [[0, 0], [7, 1],
                  [9, 0],
                  [8, -2], [10, -3], [12, -2],
                  [11, 0],
                  [13, 1], [20, 0]]

if __name__ == '__main__':
  # setup a plotter
  figure = pyplot.figure()
  axes = figure.add_subplot(111)

  # setup a grid
  grid = puzzle.Grid((7, 9), control_points)
  segments = grid.get_segments()
  print 'number of segments:', len(segments)

  # plot
  axes.plot([p.x for p in grid.points], [p.y for p in grid.points], 'b.')
  for segment in segments:
    x, y = segment
    axes.plot(x, y, 'g-')

  # format and save
  axes.set_xlim([grid.min_x - 1.0, grid.max_x + 1.0])
  axes.set_ylim([grid.min_y - 1.0, grid.max_y + 1.0])
  axes.set_aspect('equal')
  figure.set_size_inches(28, 16)
  figure.savefig('/tmp/grid.png', dpi=100)
