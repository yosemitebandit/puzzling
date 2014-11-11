"""plot_puzzle.py

Plotting a random puzzle board with basis splines.

Usage:
  plot_puzzle.py <width> <height> [--method=<m>] [--out=<o>]
      [--grid-jitter=<g>] [--control-point-jitter=<c>]

Args:
  <width>   number of pieces in the x-direction
  <height>  number of pieces in the y-direction

Options:
  --method=<m>                spline type [default: bspline]
  --out=<o>                   save path [default: /tmp/out.png]
  --grid-jitter=<g>           jitter randomness [default: 0.1]
  --control-point-jitter=<c>  control point randomness [default: 0.03]
"""

from docopt import docopt
import matplotlib.pyplot as pyplot

import puzzle


# empirically-determined spline control points for a puzzle piece edge
control_points = [[0, 0], [7, 1],
                  [9, 0],
                  [8, -2], [10, -3], [12, -2],
                  [11, 0],
                  [13, 1], [20, 0]]


if __name__ == '__main__':
  # get input args
  args = docopt(__doc__)

  # setup the grid
  grid = puzzle.Grid((int(args['<width>']), int(args['<height>'])),
      control_points, args['--method'],
      grid_jitter=float(args['--grid-jitter']),
      control_point_jitter=float(args['--control-point-jitter']))
  segments = grid.get_segments()

  # plot
  figure = pyplot.figure()
  axes = figure.add_subplot(111)
  axes.plot([p.x for p in grid.points], [p.y for p in grid.points], 'b.')
  for segment in segments:
    x, y = segment
    axes.plot(x, y, 'g-')

  # format and save
  axes.set_xlim([grid.min_x - 1.0, grid.max_x + 1.0])
  axes.set_ylim([grid.min_y - 1.0, grid.max_y + 1.0])
  axes.set_aspect('equal')
  figure.set_size_inches(28, 16)
  figure.savefig(args['--out'], dpi=100)
