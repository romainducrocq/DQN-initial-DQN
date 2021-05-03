import math
import random

RES = (1920, 1080)


def sign(n):
    return int(n/abs(n))


def arg_max(_list):
    return max(range(len(_list)), key=lambda i: _list[i])


def arg_min(_list):
    return min(range(len(_list)), key=lambda i: _list[i])


def clip(min_clip, max_clip, x):
    return max(min_clip, min([max_clip, x])) if min_clip < max_clip else x


def euclidean_distance(point1, point2):
    return math.sqrt(pow(point2[0] - point1[0], 2) + pow(point2[1] - point1[1], 2))


def point_on_circle(theta, radius, x_orig, y_orig):
    return x_orig + math.cos(theta)*radius, y_orig + math.sin(theta)*radius


def theta_right_triangle(o=None, a=None, h=None, f=None):
    if f == "sin":
        return math.asin(o/h)
    if f == "cos":
        return math.acos(a/h)
    if f == "tan":
        return math.atan(o/a)


def midpoint_vertex(vertex):
    return [(vertex[0][0] + vertex[1][0]) / 2, (vertex[0][1] + vertex[1][1]) / 2]


def slope_vertex(vertex):
    return 0 if (vertex[1][0] - vertex[0][0]) == 0 else \
        math.atan((vertex[1][1] - vertex[0][1])/(vertex[1][0] - vertex[0][0]))


def slope_vertex_2pi(vertex):
    slope = slope_vertex(vertex)
    if (((vertex[1][1] - vertex[0][1]) >= 0 and (vertex[1][0] - vertex[0][0]) < 0)
            or ((vertex[1][1] - vertex[0][1]) < 0 and (vertex[1][0] - vertex[0][0]) < 0)):
        slope += math.pi
    elif (vertex[1][1] - vertex[0][1]) < 0 and (vertex[1][0] - vertex[0][0]) >= 0:
        slope += 2*math.pi
    return slope


# https://stackoverflow.com/questions/39879924/rotate-a-rectangle-consisting-of-4-tuples-to-left-or-right
def rotate_point(x_rot, y_rot, x_trans, y_trans, theta):
    return math.cos(theta) * x_rot - math.sin(theta) * y_rot + x_trans, \
           math.sin(theta) * x_rot + math.cos(theta) * y_rot + y_trans


# https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect?rq=1
def get_vertices_intersection(vertex1, vertex2):
    p0_x, p0_y, p1_x, p1_y = vertex1[0][0], vertex1[0][1], vertex1[1][0], vertex1[1][1]
    p2_x, p2_y, p3_x, p3_y = vertex2[0][0], vertex2[0][1], vertex2[1][0], vertex2[1][1]

    s1_x, s1_y = p1_x - p0_x, p1_y - p0_y
    s2_x, s2_y = p3_x - p2_x, p3_y - p2_y

    if (-s2_x * s1_y + s1_x * s2_y) == 0:
        return False, None, None

    s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-s2_x * s1_y + s1_x * s2_y)
    t = (s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-s2_x * s1_y + s1_x * s2_y)

    if 0 <= s <= 1 and 0 <= t <= 1:  # Collision detected
        i_x = p0_x + (t * s1_x)
        i_y = p0_y + (t * s1_y)
        return True, i_x, i_y

    return False, None, None         # No collision


# https://stackoverflow.com/questions/8997099/algorithm-to-generate-random-2d-polygon
def generate_polygon(x_orig=0, y_orig=0, avg_radius=(RES[0]+RES[1])/2, irregularity=0.75, spikeyness=0.25, n_vertices=10, res=RES, offset=100):

    irregularity = clip(0, 1, irregularity) * 2*math.pi / n_vertices
    spikeyness = clip(0, 1, spikeyness) * avg_radius

    theta_steps = []             # Generate n angle steps
    lower = (2*math.pi / n_vertices) - irregularity
    upper = (2*math.pi / n_vertices) + irregularity
    sum_steps = 0
    for i in range(n_vertices):
        step = random.uniform(lower, upper)
        theta_steps.append(step)
        sum_steps = sum_steps + step

    k = sum_steps / (2*math.pi)  # Normalize the steps so that point 0 and point n+1 are the same
    for i in range(n_vertices):
        theta_steps[i] = theta_steps[i] / k

    points = []                  # Now generate the points
    theta = random.uniform(0, 2*math.pi)
    diagonal_theta = theta_right_triangle(o=res[1], a=res[0], f="tan")
    for i in range(n_vertices):
        w_h = int(-math.cos(diagonal_theta) <= math.cos(theta) <= math.cos(diagonal_theta))

        r_i = clip(-res[w_h] + offset, res[w_h] - offset, random.gauss(avg_radius, spikeyness))
        x = x_orig + r_i*math.cos(theta)
        y = y_orig + r_i*math.sin(theta)
        points.append((int(x), int(y)))

        theta = theta + theta_steps[i]

    vertices = []
    for i in range(len(points)):
        vertices.append([points[i - 1], points[i]])

    return vertices


def zoom_vertices(vertices, zoom=150, x_orig=0, y_orig=0):
    new_vertices = []
    for vertex in vertices:
        new_vertex = []
        for point in vertex:
            h = euclidean_distance((x_orig, y_orig), point)
            theta = 0
            if (point[0] - x_orig) >= 0 and (point[1] - y_orig) >= 0:
                a = euclidean_distance((x_orig, y_orig), (point[0], y_orig))
                theta += theta_right_triangle(a=a, h=h, f="cos")
            elif (point[0] - x_orig) < 0 and (point[1] - y_orig) >= 0:
                a = euclidean_distance((x_orig, y_orig), (x_orig, point[1]))
                theta += theta_right_triangle(a=a, h=h, f="cos") + math.pi/2
            elif (point[0] - x_orig) < 0 and (point[1] - y_orig) < 0:
                a = euclidean_distance((x_orig, y_orig), (point[0], y_orig))
                theta += theta_right_triangle(a=a, h=h, f="cos") + math.pi
            elif (point[0] - x_orig) >= 0 and (point[1] - y_orig) < 0:
                a = euclidean_distance((x_orig, y_orig), (x_orig, point[1]))
                theta += theta_right_triangle(a=a, h=h, f="cos") + 3*math.pi/2
            new_vertex.append(point_on_circle(theta, h + zoom, x_orig, y_orig))
        new_vertices.append(new_vertex)
    return new_vertices
