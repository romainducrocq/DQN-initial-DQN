from track import *
from car import *


def init():
    track = Track()
    car = Car()

    track.create_polygons()
    (car.x_pos, car.y_pos), car.theta = track.start_line()
    return track, car


def event_loop(track, car, action):
    car.move(action)
    car.sonar(track.border_vertices())
    car.collision(track.border_vertices())
    if car.is_collision:
        track, car = init()
    return track, car
