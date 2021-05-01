from track import *
from car import *


def init(track, car):
    track.create_polygons()
    (car.x_pos, car.y_pos), car.theta = track.start_line()
    return track, car


def event_loop(track, car, action):
    car.move(action)
    car.collision(track.border_vertices())
    car.sonar(track.border_vertices())
    return track, car
