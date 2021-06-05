# """CHANGE IS PYGLET VIEW HERE""" #####################################################################################
PYGLET = True
########################################################################################################################

# """CHANGE PYGLET VIEW HERE""" ########################################################################################

if PYGLET:
    # """CHANGE CUSTOM ENV UTILS IMPORT HERE""" ########################################################################
    from .custom_env import RES
    ####################################################################################################################

    from pyglet.gl import *

    import time


class PygletView(pyglet.window.Window if PYGLET else object):

    @staticmethod
    def points_to_pyglet_vertex(points, color):
        return pyglet.graphics.vertex_list(len(points),
                                           ('v3f/stream', [item for sublist in
                                                           map(lambda p: [p[0], p[1], 0], points)
                                                           for item in sublist]),
                                           ('c3B', PygletView.color_polygon(len(points), color))
                                           )

    @staticmethod
    def color_polygon(n, color):
        colors = []
        for i in range(n):
            colors.extend(color)
        return colors

    @staticmethod
    def draw_polygons(polygons, color):
        [PygletView.points_to_pyglet_vertex(polygon, color).draw(gl.GL_TRIANGLE_FAN) for polygon in polygons]

    @staticmethod
    def draw_vertices(vertices, color):
        [PygletView.points_to_pyglet_vertex(vertex, color).draw(gl.GL_LINES) for vertex in vertices]

    @staticmethod
    def draw_label_top_left(text, x, y, y_offset=0, margin=50, font_size=40, color=(0, 0, 0, 255)):
        pyglet.text.Label(text, x=x + margin, y=y - y_offset * (font_size + margin) - margin, font_size=font_size,
                          color=color).draw()

    @staticmethod
    def load_sprite(path, anchor_x=0.5, anchor_y=0.5):
        img = pyglet.image.load(path)
        img.anchor_x = int(img.width * anchor_x)
        img.anchor_y = int(img.height * anchor_y)
        return pyglet.sprite.Sprite(img, 0, 0)

    def __init__(self, name, env):
        # """CHANGE VIEW INIT HERE""" ##################################################################################
        (width, height) = RES
        background_color = [193, 225, 193]
        ################################################################################################################

        super(PygletView, self).__init__(width, height, name, resizable=True)
        glClearColor(background_color[0] / 255, background_color[1] / 255, background_color[2] / 255, 1)
        self.zoom = 1
        self.key = None

        self.env = env

        self.setup()

        # """CHANGE VIEW SETUP HERE""" #################################################################################
        self.ai_view = False
        self.ai_view_timer = time.time()

        self.colors = {
            "car": [[255, 0, 0], [0, 0, 255]],
            "polygons_track": [51, 51, 51],
            "vertex_borders": [255, 0, 100],
            "vertex_reward_gates": [0, 100, 255],
            "vertex_next_reward_gate": [255, 0, 100]
        }

        img_path = "./env/custom_env/img/"
        self.car_imgs, self.car_sprites = [], []
        for i, sprite in enumerate(["car_blue.png", "car_red.png"]):
            self.car_imgs.append(pyglet.image.load(img_path + sprite))
            self.car_imgs[i].anchor_x = self.car_imgs[i].width // 2
            self.car_imgs[i].anchor_y = self.car_imgs[i].height // 2
            self.car_sprites.append({
                "sprite": pyglet.sprite.Sprite(self.car_imgs[i], 0, 0),
                "scale_x": (self.env.car.height + 5) / (self.car_imgs[i].height * 2),
                "scale_y": 2 * (self.env.car.width + 5) / self.car_imgs[i].width
            })
        ################################################################################################################

    @staticmethod
    def await_frame_skip():
        # """CHANGE AWAIT FRAME SKIP HERE""" ###########################################################################
        time.sleep(0.)
        ################################################################################################################

    def get_play_action(self):
        # """CHANGE GET PLAY ACTION HERE""" ############################################################################
        noop = self.env.car.actions['NOOP']
        action_keys = {
            pyglet.window.key.UP: self.env.car.actions['UP'],
            pyglet.window.key.RIGHT: self.env.car.actions['RIGHT'],
            pyglet.window.key.DOWN: self.env.car.actions['DOWN'],
            pyglet.window.key.LEFT: self.env.car.actions['LEFT']
        }

        return noop if self.key not in action_keys else action_keys[self.key]
        ################################################################################################################

    def on_draw(self, dt=0.002):
        self.clear()

        self.loop()

        # """CHANGE VIEW LOOP HERE""" ##################################################################################
        PygletView.draw_polygons(self.env.track.polygons_track, self.colors["polygons_track"])
        if self.key == pyglet.window.key.SPACE and (time.time() - self.ai_view_timer) > 0.2:
            self.ai_view = not self.ai_view
            self.ai_view_timer = time.time()
        if self.ai_view:
            PygletView.draw_vertices(self.env.track.reward_gates, self.colors["vertex_reward_gates"])
            PygletView.draw_vertices([self.env.track.next_reward_gate(self.env.car.next_reward_gate_i)], self.colors["vertex_next_reward_gate"])
            PygletView.draw_vertices(self.env.car.sonars, self.colors["car"][int(self.env.car.is_collision)])
        PygletView.draw_vertices(self.env.track.out_border_vertices, self.colors["vertex_borders"])
        PygletView.draw_vertices(self.env.track.in_border_vertices, self.colors["vertex_borders"])
        # draw_polygons([self.env.car.points()], self.colors["car"][int(self.env.car.is_collision)])

        self.car_sprites[int(self.env.car.is_collision)]["sprite"].update(
            x=self.env.car.x_pos,
            y=self.env.car.y_pos,
            scale_x=self.car_sprites[int(self.env.car.is_collision)]["scale_x"],
            scale_y=self.car_sprites[int(self.env.car.is_collision)]["scale_y"],
            rotation=270-self.env.car.theta
        )
        self.car_sprites[int(self.env.car.is_collision)]["sprite"].draw()

        PygletView.draw_label_top_left("AI view: SPACE", -RES[0], RES[1], y_offset=1)
        PygletView.draw_label_top_left("Time: " + str(round(self.env.car.get_time(), 2)), -RES[0], RES[1], y_offset=2)
        PygletView.draw_label_top_left("Score: " + str(self.env.car.score), -RES[0], RES[1], y_offset=3)
        ################################################################################################################

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

    def setup(self):
        raise NotImplementedError

    def loop(self):
        raise NotImplementedError

    def run(self):
        pyglet.clock.schedule_interval(self.on_draw, 0.002)
        pyglet.app.run()


########################################################################################################################

# """CHANGE CUSTOM VIEW HERE""" ########################################################################################

if not PYGLET:
    import time


class CustomView:
    def __init__(self, name, env):
        self.name = name
        self.env = env

        self.setup()

        # """CHANGE VIEW SETUP HERE""" #################################################################################
        ################################################################################################################

    @staticmethod
    def await_frame_skip():
        # """CHANGE AWAIT FRAME SKIP HERE""" ###########################################################################
        time.sleep(0.)
        ################################################################################################################

    def get_play_action(self):
        # """CHANGE GET PLAY ACTION HERE""" ############################################################################
        return 0
        ################################################################################################################

    def on_draw(self, dt=0.002):
        time.sleep(dt)
        self.clear()
        
        self.loop()
    
        # """CHANGE VIEW LOOP HERE""" ##################################################################################
        ################################################################################################################

    def clear(self):
        # """CHANGE CLEAR VIEW HERE""" #################################################################################
        pass
        ################################################################################################################

    def setup(self):
        raise NotImplementedError

    def loop(self):
        raise NotImplementedError

    def run(self):
        while True:
            self.on_draw()

########################################################################################################################
