from track import *
from car import *


def init(track, car):
    return track, car


def event_loop(track, car, action):
    car.move(action)
    car.collision(track.vertices)
    return track, car
