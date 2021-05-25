from .utils import \
    euclidean_distance, \
    get_vertices_intersection, \
    point_on_circle, \
    rotate_point, \
    safe_dict, \
    RES
import math
import time


class Car:
    def __init__(self, max_features=None):
        self.x_pos = 0
        self.y_pos = 0
        self.width = 20
        self.height = 2 * self.width
        self.theta = 0
        self.speed = 0.
        self.d_theta = 2
        self.d_a = 0.03
        self.d_da = 0.06
        self.d_a_friction = 0.01
        self.min_speed = 0.3
        self.max_speed = safe_dict(max_features, "speed", 20.)
        self.max_sonar_distance = safe_dict(max_features, "sonar_distance", RES[0])

        self.is_collision = False

        self.n_sonars = 36
        self.sonars = [[]]*self.n_sonars
        self.sonar_distances = [0.]*self.n_sonars

        self.next_reward_gate_i = 0
        self.score = 0

        self.start_time = time.time()

        self.actions = {'UP': 0, 'RIGHT': 1, 'DOWN': 2, 'LEFT': 3, 'NONE': 4}

        self.color = [[255, 0, 0], [0, 0, 255]]
        self.sprites = ["./env/img/car_blue.png", "./env/img/car_red.png"]

    def top_left_point(self):
        return rotate_point(-self.width / 2, -self.height / 2, self.x_pos, self.y_pos, math.radians(self.theta))

    def top_right_point(self):
        return rotate_point(self.width / 2, -self.height / 2, self.x_pos, self.y_pos, math.radians(self.theta))

    def down_right_point(self):
        return rotate_point(self.width / 2, self.height / 2, self.x_pos, self.y_pos, math.radians(self.theta))

    def down_left_point(self):
        return rotate_point(-self.width / 2, self.height / 2, self.x_pos, self.y_pos, math.radians(self.theta))

    def points(self):
        return [
            self.top_left_point(),
            self.top_right_point(),
            self.down_right_point(),
            self.down_left_point()
        ]

    def top_vertex(self):
        return self.top_left_point(), self.top_right_point()

    def right_vertex(self):
        return self.top_right_point(), self.down_right_point()

    def down_vertex(self):
        return self.down_right_point(), self.down_left_point()

    def left_vertex(self):
        return self.down_left_point(), self.top_right_point()

    def vertices(self):
        return [
            self.top_vertex(),
            self.right_vertex(),
            self.down_vertex(),
            self.left_vertex()
        ]

    def move(self, action):
        if action == self.actions['UP']:
            self.accelerate()
        elif action == self.actions['RIGHT']:
            self.rotate_right()
            self.friction()
        elif action == self.actions['DOWN']:
            self.decelerate()
        elif action == self.actions['LEFT']:
            self.rotate_left()
            self.friction()
        elif action == self.actions['NONE']:
            self.friction()
        else:
            self.friction()

        self.x_pos, self.y_pos = rotate_point(0, self.speed, self.x_pos, self.y_pos, math.radians(self.theta))

    def accelerate(self):
        self.speed = min([(self.speed * (1 + self.d_a) if self.speed > 0 else self.min_speed), self.max_speed])

    def rotate_left(self):
        self.theta = (self.theta + self.d_theta) % 360 if self.speed > 0 else self.theta

    def decelerate(self):
        self.speed = (self.speed * (1 - self.d_da) if self.speed * (1 - self.d_da) >= self.min_speed else 0.)

    def rotate_right(self):
        self.theta = (self.theta - self.d_theta) % 360 if self.speed > 0 else self.theta

    def friction(self):
        self.speed = (self.speed * (1 - self.d_a_friction) if self.speed * (1 - self.d_a_friction) >= self.min_speed else 0.)

    def collision(self, border_vertices):
        for vertex in self.vertices():
            for border_vertex in border_vertices:
                is_intersect, x, y = get_vertices_intersection(vertex, border_vertex)
                if is_intersect:
                    self.is_collision = True
                    return
        self.is_collision = False

    def sonar(self, border_vertices):
        a, b, c = 4, 6, 10
        for i in range(self.n_sonars):
            theta = 0
            if i < a:
                theta += (i * 2 * math.pi) / a
            elif a <= i < a + 2 * b:
                theta += ((((i - a) // b) + 1) * 2 - 1) * math.pi / 2 + \
                         (2 * (i % 2) - 1) * math.pi / pow(2, (i - (i % 2) - a - b * ((i - a) // b)) / 2 + 3)
            else:
                theta += ((i - (a + 2 * b)) // c) * math.pi + \
                         (2 * (i % 2) - 1) * ((i - (i % 2) - a - b * 2 - c * ((i - (a + 2 * b)) // c)) / 2 + 1) * math.pi / 16

            self.sonars[i] = [
                (self.x_pos, self.y_pos),
                point_on_circle(math.radians(self.theta) + theta, self.max_sonar_distance, self.x_pos, self.y_pos)
            ]

            for border_vertex in border_vertices:
                is_intersect, x, y = get_vertices_intersection(self.sonars[i], border_vertex)
                if is_intersect:
                    self.sonars[i][1] = (x, y)
                    self.sonar_distances[i] = euclidean_distance(self.sonars[i][0], self.sonars[i][1])

    def reward(self, reward_gate_vertex, update_next_reward_gate_i):
        for vertex in self.vertices():
            if get_vertices_intersection(vertex, reward_gate_vertex)[0]:
                self.next_reward_gate_i = update_next_reward_gate_i
                self.score += 1
                return True
        return False

    def get_time(self):
        return time.time() - self.start_time

