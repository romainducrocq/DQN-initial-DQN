from .track import Track
from .car import Car
from .utils import RES
import gym
from gym import spaces
import numpy as np


class CustomEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, train=False):
        super(CustomEnv, self).__init__()

        self.MAX_FEATURES = {
            "speed": 50. if train else 35.,
            "sonar_distance": RES[0]
        }

        self.track = Track()
        self.car = Car(max_features=self.MAX_FEATURES)

        self.steps = 0
        self.total_reward = 0.
        self.action_space = spaces.Discrete(len(self.car.actions))
        self.observation_space = spaces.Box(low=0., high=1., shape=(self.car.n_sonars+1,), dtype=np.float32)

    def _obs(self):
        self.car.sonar(self.track.border_vertices())

        obs = np.array(
            [
                sonar_distance / self.MAX_FEATURES["sonar_distance"]
                for sonar_distance in self.car.sonar_distances
            ] + [
                self.car.speed / self.MAX_FEATURES["speed"]
            ], dtype=np.float32)
        return obs

    def _rew(self):
        rew = 0.
        if self.car.reward(self.track.next_reward_gate(self.car.next_reward_gate_i),
                           self.track.update_next_reward_gate_index(self.car.next_reward_gate_i)):
            rew += 1
        self.total_reward += rew
        return rew

    def _done(self):
        self.car.collision(self.track.border_vertices())
        done = self.car.is_collision
        return done

    def _info(self):
        info = {
            "l": self.steps,
            "r": self.total_reward
        }
        return info

    def reset(self):
        self.steps = 0
        self.total_reward = 0.

        self.track = Track()
        self.car = Car(max_features=self.MAX_FEATURES)

        (self.car.x_pos, self.car.y_pos), self.car.theta = self.track.start_line()
        self.track.create_reward_gates()
        self.car.next_reward_gate_i = self.track.start_reward_gate(self.car.vertices())

        return self._obs()

    def step(self, action):
        self.car.move(action)

        self.steps += 1

        return self._obs(), self._rew(), self._done(), self._info()

    def reset_render(self):
        return self.track.create_track_polygons()

    def render(self, mode='human'):
        pass
