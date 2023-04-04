import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

def surfboard_outline(width, thickness, num_points=1000):
    """
    Generate a smooth closed curve representing the outline of a surfboard cross-section using a cubic spline.

    Parameters:
    width (float): Width of the surfboard.
    thickness (float): Thickness of the surfboard.
    bottom_curve (float): Curvature of the bottom half of the surfboard outline.
    num_points (int): Number of points to generate on the curve. Defaults to 100.

    Returns:
    x (numpy.ndarray): x-coordinates of the surfboard outline.
    y (numpy.ndarray): y-coordinates of the surfboard outline.
    """
    # Define control points for Bezier curve
    p0 = [0, thickness/2]
    p2 = [0, -thickness/2]
    p1 = [width/2, (p0[1]+p2[1])/2]
    p3 = [-width/2, (p0[1]+p2[1])/2]
    print(f'Effective thickness is {p0[1]+abs(p2[1])}')
    # Create array of control points
    control_points = np.array([p2, p3, p0, p1, p2])
    # plt.scatter(p0[0],p0[1],color='black')
    # plt.scatter(p1[0],p1[1],color='blue')
    # plt.scatter(p2[0],p2[1],color='orange')
    # plt.scatter(p3[0],p3[1],color='green')

    # Generate evenly spaced parameter values for the spline
    t = np.linspace(0, 1, 5)

    # Generate cubic spline interpolation function
    spline_func = interp1d(t, control_points, kind='cubic', axis=0)

    # Generate parameter values for the smooth curve
    t_smooth = np.linspace(0, 1, num_points+1)

    # Evaluate the cubic spline at the parameter values to generate the smooth curve
    curve = spline_func(t_smooth)

    # Extract x and y coordinates of the smooth curve
    x = curve[:, 0]
    y = curve[:, 1]

    # Return x and y coordinates of the closed curve
    return x, y

def offset(x,y,offset):

    # calculate unit tangent vector at each point
    dx = np.gradient(x)
    dy = np.gradient(y)
    ds = np.sqrt(dx**2 + dy**2)
    tx = dx/ds
    ty = dy/ds

    # rotate unit tangent vector by 90 degrees to obtain unit normal vector
    nx = -ty
    ny = tx

    # scale unit normal vector by offset distance to obtain offset vector
    ox = nx * offset
    oy = ny * offset

    # translate each point along original curve by corresponding offset vector
    x_offset = x + ox
    y_offset = y + oy
    
    return x_offset, y_offset

