import numpy as np


def intersection(line0, line1):
    """Find the point where two lines intersect

    Parameters
    ----------
    line0 : numpy.ndarray
        two points that define a line -- ``[[x0, y0, x1, y1]]``
    line1 : numpy.ndarray
        two points that define a line (same as ``line0``)

    Returns
    -------
    numpy.ndarray
        the point where ``line0`` and ``line1`` intersect -- ``[x, y]``

    """
    # \Delta x and \Delta y
    dx0 = line0[0][2] - line0[0][0]
    dy0 = line0[0][3] - line0[0][1]
    dx1 = line1[0][2] - line1[0][0]
    dy1 = line1[0][3] - line1[0][1]

    # A [x, y]^T = b
    A = np.array([[dy0, -dx0], [dy1, -dx1]])
    b = np.array([line0[0][0] * dy0 - line0[0][1] * dx0, line1[0][0] * dy1 - line1[0][1] * dx1])

    return np.round(np.linalg.solve(A, b))  # .astype(np.uint16)


def find_x_given_y(line, y):
    """Given a line, solve for x when y is specified

    Parameters
    ----------
    line : numpy.ndarray
        two points that define a line -- ``[[x0, y0, x1, y1]]``
    y : float
        we want to find x such that (x, y) is on the line

    Returns
    -------
    numpy.ndarray
        ``[x, y]``, where x is such that (x, y) is on the line

    """
    dx = line[0][2] - line[0][0]
    dy = line[0][3] - line[0][1]

    return np.round(np.array([line[0][0] + (y - line[0][1]) * dx / dy, y]))  # .astype(np.uint16)


def intersection_or_ymax(line0, line1, y_const):
    """Given two lines, return whichever points are lower: their intersection with each other
    or their intersection with the line y=y_const

    Parameters
    ----------
    line0 : numpy.ndarray
        two points that define a line -- ``[[x0, y0, x1, y1]]``
    line1 : numpy.ndarray
        two points that define a line (same as ``line0``)
    y_const : float
        we will find the intersections of ``line0`` and ``line1`` with the line y=y_const

    Returns
    -------
    numpy.ndarray
        the point ``[x, y]`` where ``line0`` intersects ``line1`` OR where ``line0`` intersects y=y_const
    numpy.ndarray
        same as xy0, except for ``line1``

    """
    # point where the lines intersect each other
    xy = intersection(line0, line1)

    if xy[1] > y_const:
        return xy, xy
    else:
        return find_x_given_y(line0, y_const), find_x_given_y(line1, y_const)


def extend_to_bottom_top(line, y_bottom, y_top):
    """Extend ``line`` to the bottom and top of the masked image

    Parameters
    ----------
    line : numpy.ndarray
        two points that define a line -- ``[[x0, y0, x1, y1]]``
    y_bottom : float
        we will find the intersection of ``line`` with the line y=y_bottom
    y_top : float
        we will find the intersection of ``line`` with the line y=y_top

    Returns
    -------
    numpy.ndarray
        two points that define a line -- ``[[x0, y0, x1, y1]]``, where ``y0 = y_bottom``
        and ``y1 = y_top``

    """
    # find the points on the bottom and top
    xy_bottom = find_x_given_y(line, y_bottom)
    xy_top = find_x_given_y(line, y_top)

    return np.array([[xy_bottom[0], xy_bottom[1], xy_top[0], xy_top[1]]])


def extend_to_bottom(line, y_bottom):
    """Extend ``line`` to the bottom of the masked image

    Parameters
    ----------
    line : numpy.ndarray
        two points that define a line -- ``[[x0, y0, x1, y1]]``
    y_bottom : float
        we will find the intersection of ``line`` with the line y=y_bottom

    Returns
    -------
    numpy.ndarray
        two points that define a line -- ``[[x0, y0, x1, y1]]``, where ``y0 = y_bottom``

    """
    # find the points on the bottom and top
    xy_bottom = find_x_given_y(line, y_bottom)

    if line[0][1] > line[0][3]:
        return np.array([[xy_bottom[0], xy_bottom[1], line[0][2], line[0][3]]])
    else:
        return np.array([[xy_bottom[0], xy_bottom[1], line[0][0], line[0][1]]])


def get_slope(line):
    """Get the slope of the line

    Parameters
    ----------
    line : numpy.ndarray
        two points that define a line -- ``[[x0, y0, x1, y1]]``

    Returns
    -------
    float
        the slope of the line

    """
    if np.abs(float(line[0][2]) - float(line[0][0])) < 1e-6:
        return 1e6
    else:
        return (float(line[0][3]) - float(line[0][1])) / (float(line[0][2]) - float(line[0][0]))