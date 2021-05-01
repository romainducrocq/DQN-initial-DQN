from utils import *
import random


class Car:
    def __init__(self, x_pos=0, y_pos=0, width=20, ratio=2, speed=1., theta=0, color=(255, 0, 0)):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = ratio * width
        self.speed = speed
        self.theta = theta
        self.d_theta = 2
        self.d_a = 0.03
        self.d_a_friction = 0.01
        self.min_speed = 0.5

        self.color = color

    def top_left_point(self):
        return rotate_point(-self.width / 2, -self.height / 2, self.x_pos, self.y_pos, self.theta)

    def top_right_point(self):
        return rotate_point(self.width / 2, -self.height / 2, self.x_pos, self.y_pos, self.theta)

    def down_right_point(self):
        return rotate_point(self.width / 2, self.height / 2, self.x_pos, self.y_pos, self.theta)

    def down_left_point(self):
        return rotate_point(-self.width / 2, self.height / 2, self.x_pos, self.y_pos, self.theta)

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
        if action == "UP":
            self.accelerate()
        elif action == "RIGHT":
            self.rotate_right()
            self.friction()
        elif action == "DOWN":
            self.decelerate()
        elif action == "LEFT":
            self.rotate_left()
            self.friction()
        else:
            self.friction()

        self.x_pos, self.y_pos = rotate_point(0, self.speed, self.x_pos, self.y_pos, self.theta)

    def accelerate(self):
        self.speed = self.speed * (1 + self.d_a)

    def rotate_left(self):
        self.theta = (self.theta + self.d_theta) % 360

    def decelerate(self):
        self.speed = (self.speed * (1 - self.d_a) if self.speed * (1 - self.d_a) >= self.min_speed else self.min_speed)

    def rotate_right(self):
        self.theta = (self.theta - self.d_theta) % 360

    def friction(self):
        self.speed = (self.speed * (1 - self.d_a_friction) if self.speed * (1 - self.d_a_friction) >= self.min_speed else self.min_speed)

    def collision(self, lines):
        for vertex in self.vertices():
            for line in lines:
                is_intersect, x, y = get_vertices_intersection(vertex, line)
                if is_intersect:
                    self.color = [0, 0, 255]
                    return
        self.color = [255, 0, 0]
