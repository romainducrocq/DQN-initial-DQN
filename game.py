from track import *
from car import *


def init():
    track = Track()
    car = Car()

    track.create_track_polygons()
    (car.x_pos, car.y_pos), car.theta = track.start_line()
    track.create_reward_gates()
    car.next_reward_gate_i = track.start_reward_gate(car.vertices())
    return track, car


def event_loop(track, car, action):
    car.move(action)
    car.sonar(track.border_vertices())
    car.reward(track.next_reward_gate(car.next_reward_gate_i),
               track.update_next_reward_gate_index(car.next_reward_gate_i))

    car.collision(track.border_vertices())
    if car.is_collision:
        track, car = init()
    return track, car
