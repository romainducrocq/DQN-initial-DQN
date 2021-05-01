from pyglet.gl import *
import math
import random
from utils import *
from track import *
from car import *
from game import *


def points_to_pyglet_vertex(points, color):
    return pyglet.graphics.vertex_list(len(points),
                                       ('v3f/stream', [item for sublist in
                                                       map(lambda p: [p[0], p[1], 0], points)
                                                       for item in sublist]),
                                       ('c3B', color_polygon(len(points), color))
                                       )


def color_polygon(n, color):
    colors = []
    for i in range(n):
        colors.extend(color)
    return colors


def draw_polygons(polygons, color):
    [points_to_pyglet_vertex(polygon, color).draw(gl.GL_TRIANGLE_FAN) for polygon in polygons]


def draw_vertices(vertices, color):
    [points_to_pyglet_vertex(vertex, color).draw(gl.GL_LINES) for vertex in vertices]


class View(pyglet.window.Window):

    def __init__(self, width, height, name):
        super(View, self).__init__(width, height, name, resizable=True)
        glClearColor(193/255, 225/255, 193/255, 1)
        self.width = width
        self.height = height
        self.name = name
        self.zoom = 1
        self.key = None
        self.actions = {
            pyglet.window.key.UP: "UP",
            pyglet.window.key.RIGHT: "RIGHT",
            pyglet.window.key.DOWN: "DOWN",
            pyglet.window.key.LEFT: "LEFT"
        }

        self.track, self.car = init()

        self.car_imgs, self.car_sprites = [], []
        for i, sprite in enumerate(self.car.sprites):
            self.car_imgs.append(pyglet.image.load(sprite))
            self.car_imgs[i].anchor_x = self.car_imgs[i].width // 2
            self.car_imgs[i].anchor_y = self.car_imgs[i].height // 2
            self.car_sprites.append({
                "sprite": pyglet.sprite.Sprite(self.car_imgs[i], 0, 0),
                "scale_x": (self.car.height + 5) / (self.car_imgs[i].height * 2),
                "scale_y": 2 * (self.car.width + 5) / self.car_imgs[i].width
            })

    def on_draw(self, dt=0.002):
        self.clear()
        action = None if self.key not in self.actions else self.actions[self.key]
        self.track, self.car = event_loop(self.track, self.car, action)
        draw_polygons(self.track.polygons, self.track.polygons_color)
        draw_vertices(self.track.out_border_vertices, self.track.vertex_color)
        draw_vertices(self.track.in_border_vertices, self.track.vertex_color)
        draw_vertices(self.car.sonars, self.car.color)
        # draw_polygons([self.car.points()], self.car.color)

        self.car_sprites[int(self.car.is_collision)]["sprite"].update(
            x=self.car.x_pos,
            y=self.car.y_pos,
            scale_x=self.car_sprites[int(self.car.is_collision)]["scale_x"],
            scale_y=self.car_sprites[int(self.car.is_collision)]["scale_y"],
            rotation=270-self.car.theta
        )
        self.car_sprites[int(self.car.is_collision)]["sprite"].draw()

    def on_resize(self, width, height):
        glMatrixMode(gl.GL_MODELVIEW)
        glLoadIdentity()
        glOrtho(-width, width, -height, height, -1, 1)
        glViewport(0, 0, width, height)
        glOrtho(-self.zoom, self.zoom, -self.zoom, self.zoom, -1, 1)

    def on_key_press(self, symbol, modifiers):
        self.key = symbol

    def on_key_release(self, symbol, modifiers):
        if self.key == symbol:
            self.key = None
