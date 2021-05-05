from .track import Track
from .car import Car
import gym
from gym import spaces
import numpy as np


class CustomEnv(gym.Env):
    def __init__(self):
        super(CustomEnv, self).__init__()

        self.track = Track()
        self.car = Car()

        self.action_space = spaces.Discrete(len(self.car.actions))
        self.observation_space = spaces.Box(low=0., high=1., shape=(self.car.n_sonars+1,), dtype=np.float32)

        """DEBUG"""
        self.steps = 0
        """"""

    def _obs(self):
        return np.array(self.car.normalize_sonar_distances() + [self.car.normalize_speed()], dtype=np.float32)

    def _rew(self):
        return float(self.car.score) + self.car.bonus

    def _done(self):
        return self.car.is_collision

    def _info(self):
        return {"r": self._rew(), "l": self.car.get_time()}

    def reset(self):
        self.track = Track()
        self.car = Car()

        (self.car.x_pos, self.car.y_pos), self.car.theta = self.track.start_line()
        self.track.create_reward_gates()
        self.car.next_reward_gate_i = self.track.start_reward_gate(self.car.vertices())
        self.car.sonar(self.track.border_vertices())

        """DEBUG"""
        self.steps = 0
        """"""

        return self._obs()

    def step(self, action):
        self.car.move(action)
        self.car.sonar(self.track.border_vertices())
        self.car.reward(self.track.next_reward_gate(self.car.next_reward_gate_i),
                        self.track.update_next_reward_gate_index(self.car.next_reward_gate_i))

        self.car.collision(self.track.border_vertices())

        """DEBUG"""
        self.steps += 1
        """"""

        return self._obs(), self._rew(), self._done(), self._info()

    def reset_render(self):
        return self.track.create_track_polygons()

    def render(self, mode='human'):
        pass

    """DEBUG"""
    def test_print(self):
        print("Sample action: ", self.action_space.sample())
        print("Sample observation: ", self.observation_space.sample())
        print("Action space n: ", self.action_space.n)
        print("Observation space n:", self.observation_space.shape[0])
        print("Obs: ", self._obs())
        print("Info: ", self._info())
        print("Steps: ", self.steps)
        print()
    """"""
