# """FIT TO ENV"""
from env import Env, View, safe_dict, RES
from pyglet.gl import *
######


class Play(View):
    def __init__(self, *args, **kwargs):
        super(Play, self).__init__(*args, **kwargs)

        # """FIT TO ACTIONS"""
        self.action_keys = {
            pyglet.window.key.UP: self.env.car.actions['UP'],
            pyglet.window.key.RIGHT: self.env.car.actions['RIGHT'],
            pyglet.window.key.DOWN: self.env.car.actions['DOWN'],
            pyglet.window.key.LEFT: self.env.car.actions['LEFT']
        }
        ######

    def setup(self):
        _ = self.env.reset()

    def loop(self):
        # """FIT TO ACTIONS"""
        action = safe_dict(self.action_keys, self.key, self.env.car.actions['NONE'])
        ######

        _, _, done, _ = self.env.step(action)
        if done:
            self.setup()


if __name__ == "__main__":

    # """FIT TO VIEW IF NOT PYGLET"""
    play = Play(RES[0], RES[1], "PLAY", Env())
    pyglet.clock.schedule_interval(play.on_draw, 0.002)
    pyglet.app.run()
    ######
