import math
import random

RES = (1920, 1080)


# https://stackoverflow.com/questions/39879924/rotate-a-rectangle-consisting-of-4-tuples-to-left-or-right
def rotate_point(x_rot, y_rot, x_trans, y_trans, theta):
    return math.cos(math.radians(theta)) * x_rot - math.sin(math.radians(theta)) * y_rot + x_trans, \
           math.sin(math.radians(theta)) * x_rot + math.cos(math.radians(theta)) * y_rot + y_trans


# https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect?rq=1
def get_vertices_intersection(vertex1, vertex2):
    p0_x, p0_y, p1_x, p1_y = vertex1[0][0], vertex1[0][1], vertex1[1][0], vertex1[1][1]
    p2_x, p2_y, p3_x, p3_y = vertex2[0][0], vertex2[0][1], vertex2[1][0], vertex2[1][1]

    s1_x, s1_y = p1_x - p0_x, p1_y - p0_y
    s2_x, s2_y = p3_x - p2_x, p3_y - p2_y

    s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-s2_x * s1_y + s1_x * s2_y)
    t = (s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-s2_x * s1_y + s1_x * s2_y)

    if 0 <= s <= 1 and 0 <= t <= 1:  # Collision detected
        i_x = p0_x + (t * s1_x)
        i_y = p0_y + (t * s1_y)
        return True, i_x, i_y

    return False, None, None         # No collision


# https://stackoverflow.com/questions/8997099/algorithm-to-generate-random-2d-polygon
def generate_polygon(x_orig, y_orig, avg_radius, irregularity, spikeyness, n_vertices):

    irregularity = max(0, min([1, irregularity])) * 2*math.pi / n_vertices
    spikeyness = max(0, min([1, spikeyness])) * avg_radius

    angle_steps = []             # Generate n angle steps
    lower = (2*math.pi / n_vertices) - irregularity
    upper = (2*math.pi / n_vertices) + irregularity
    sum_steps = 0
    for i in range(n_vertices):
        step = random.uniform(lower, upper)
        angle_steps.append(step)
        sum_steps = sum_steps + step

    k = sum_steps / (2*math.pi)  # Normalize the steps so that point 0 and point n+1 are the same
    for i in range(n_vertices):
        angle_steps[i] = angle_steps[i] / k

    points = []                  # Now generate the points
    angle = random.uniform(0, 2*math.pi)
    offset = 100
    for i in range(n_vertices):
        res = int(-math.cos(math.atan(RES[1]/RES[0])) <= math.cos(angle) <= math.cos(math.atan(RES[1]/RES[0])))

        r_i = max(-RES[res] + offset, min([RES[res] - offset, random.gauss(avg_radius, spikeyness)]))
        x = x_orig + r_i*math.cos(angle)
        y = y_orig + r_i*math.sin(angle)
        points.append((int(x), int(y)))

        angle = angle + angle_steps[i]

    vertices = []
    for i in range(len(points)):
        vertices.append((points[i - 1], points[i]))

    return vertices
