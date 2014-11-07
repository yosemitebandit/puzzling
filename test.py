""" b-spline test
via: http://stackoverflow.com/questions/24612626/b-spline-interpolation-with-python
"""

import numpy
import matplotlib.pyplot as pyplot
from scipy import interpolate

points = numpy.array([[-4, 4.5], [3, 5],
                      [5, 4],
                      [4, 2], [6, 1], [8, 2],
                      [7, 4],
                      [9, 5], [16, 4.5]])
x = points[:, 0]
y = points[:, 1]

t = range(len(x))
knots = [2, 3, 4]
ipl_t = numpy.linspace(0.0, len(points) - 1, 100)

x_tup = interpolate.splrep(t, x, k=3, t=knots)
y_tup = interpolate.splrep(t, y, k=3, t=knots)
x_i = interpolate.splev(ipl_t, x_tup)
y_i = interpolate.splev(ipl_t, y_tup)

print 'knots:', x_tup

figure = pyplot.figure()
axes = figure.add_subplot(111)
axes.plot(x, y, label='original')
axes.plot(x_i, y_i, label='spline')
axes.set_xlim([min(x) - 1.0, max(x) + 1.0])
axes.set_ylim([min(y) - 1.0, max(y) + 1.0])
#axes.legend()

axes.set_aspect('equal')

figure.savefig('/tmp/test.png')
