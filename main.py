from utils import *
from car import *
from track import *
from view import *


if __name__ == "__main__":

    track = Track(10, 0.75, 0.25)
    car = Car()

    view = View(RES[0], RES[1], "Initial DQN", track, car)
    pyglet.clock.schedule_interval(view.on_draw, 0.002)
    pyglet.app.run()
