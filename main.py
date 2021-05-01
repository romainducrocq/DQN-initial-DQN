from utils import *
from car import *
from track import *
from view import *


if __name__ == "__main__":

    view = View(RES[0], RES[1], "Initial DQN")
    pyglet.clock.schedule_interval(view.on_draw, 0.002)
    pyglet.app.run()
