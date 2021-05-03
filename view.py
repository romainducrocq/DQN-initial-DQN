from pyglet.gl import *
import math
import random
import time
from utils import *
from env import *


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


def draw_label_top_left(text, x, y, y_offset=0, margin=50, font_size=40, color=(0, 0, 0, 255)):
    pyglet.text.Label(text, x=x+margin, y=y-y_offset*(font_size+margin)-margin, font_size=font_size, color=color).draw()


class View(pyglet.window.Window):

    def __init__(self, width, height, name, env, mode):
        super(View, self).__init__(width, height, name, resizable=True)
        glClearColor(193/255, 225/255, 193/255, 1)
        self.width = width
        self.height = height
        self.name = name
        self.zoom = 1
        self.key = None

        self.env = env
        self.mode = mode

        self.action_keys = {
            pyglet.window.key.UP: self.env.car.actions['UP'],
            pyglet.window.key.RIGHT: self.env.car.actions['RIGHT'],
            pyglet.window.key.DOWN: self.env.car.actions['DOWN'],
            pyglet.window.key.LEFT: self.env.car.actions['LEFT']
        }

        self.car_imgs, self.car_sprites = [], []
        for i, sprite in enumerate(self.env.car.sprites):
            self.car_imgs.append(pyglet.image.load(sprite))
            self.car_imgs[i].anchor_x = self.car_imgs[i].width // 2
            self.car_imgs[i].anchor_y = self.car_imgs[i].height // 2
            self.car_sprites.append({
                "sprite": pyglet.sprite.Sprite(self.car_imgs[i], 0, 0),
                "scale_x": (self.env.car.height + 5) / (self.car_imgs[i].height * 2),
                "scale_y": 2 * (self.env.car.width + 5) / self.car_imgs[i].width
            })

        self.debug_view = False
        self.debug_timer = time.time()

        _ = self.env.reset()

    def on_draw(self, dt=0.002):
        self.clear()

        if self.mode == "PLAY":
            action = self.env.car.actions['NONE'] if self.key not in self.action_keys else self.action_keys[self.key]
            _, _, done, _ = self.env.step(action)
            if done:
                _ = self.env.reset()

        draw_polygons(self.env.track.polygons_track, self.env.track.colors["polygons_track"])
        if self.key == pyglet.window.key.SPACE and (time.time() - self.debug_timer) > 0.2:
            self.debug_view = not self.debug_view
            self.debug_timer = time.time()
        if self.debug_view:
            draw_vertices(self.env.track.reward_gates, self.env.track.colors["vertex_reward_gates"])
            draw_vertices([self.env.track.next_reward_gate(self.env.car.next_reward_gate_i)], self.env.track.colors["vertex_next_reward_gate"])
            draw_vertices(self.env.car.sonars, self.env.car.color[int(self.env.car.is_collision)])
        draw_vertices(self.env.track.out_border_vertices, self.env.track.colors["vertex_borders"])
        draw_vertices(self.env.track.in_border_vertices, self.env.track.colors["vertex_borders"])
        # draw_polygons([self.env.car.points()], self.env.car.color[int(self.env.car.is_collision)])

        self.car_sprites[int(self.env.car.is_collision)]["sprite"].update(
            x=self.env.car.x_pos,
            y=self.env.car.y_pos,
            scale_x=self.car_sprites[int(self.env.car.is_collision)]["scale_x"],
            scale_y=self.car_sprites[int(self.env.car.is_collision)]["scale_y"],
            rotation=270-self.env.car.theta
        )
        self.car_sprites[int(self.env.car.is_collision)]["sprite"].draw()

        draw_label_top_left("Debug view: SPACE", -RES[0], RES[1], y_offset=1)
        draw_label_top_left("Time: " + str(self.env.car.get_time()), -RES[0], RES[1], y_offset=2)
        draw_label_top_left("Score: " + str(self.env.car.score), -RES[0], RES[1], y_offset=3)

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
