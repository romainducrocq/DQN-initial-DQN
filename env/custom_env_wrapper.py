# """CHANGE CUSTOM ENV IMPORT HERE""" ##################################################################################
from .custom_env import Track, Car, RES
########################################################################################################################

import gym
from gym import spaces
import numpy as np


class CustomEnvWrapper(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, train=False):
        super(CustomEnvWrapper, self).__init__()

        self.train = train

        self.steps = 0
        self.total_reward = 0.

        # """CHANGE ENV CONSTRUCT HERE""" ##############################################################################
        self.track = Track()
        self.car = Car()
        ################################################################################################################

        # """CHANGE FEATURE SCALING HERE""" ############################################################################
        self.lim_features = {
            "speed": (0., 50. if self.train else 35.),
            "sonar_distance": (0., RES[0])
        }
        ################################################################################################################

        # """CHANGE ACTION AND OBSERVATION SPACE SIZES HERE""" #########################################################
        action_space_n = len(self.car.actions)
        observation_space_n = self.car.n_sonars + 1
        ################################################################################################################

        if "reward" not in self.lim_features:
            self.lim_features["reward"] = (0., 1.)

        self.action_space = spaces.Discrete(action_space_n)
        self.observation_space = spaces.Box(low=0., high=1., shape=(observation_space_n,), dtype=np.float32)

    def scale(self, x, feature):
        return (x - self.lim_features[feature][0]) / (self.lim_features[feature][1] - self.lim_features[feature][0])

    def _obs(self):
        obs = []

        # """CHANGE OBSERVATION HERE""" ################################################################################
        self.car.sonar(self.track.border_vertices())

        obs += [self.scale(sonar_distance, "sonar_distance") for sonar_distance in self.car.sonar_distances]
        obs += [self.scale(self.car.speed, "speed")]
        ################################################################################################################

        return np.array(obs, dtype=np.float32)

    def _rew(self):
        rew = 0.

        # """CHANGE REWARD HERE""" #####################################################################################
        if self.car.reward(self.track.next_reward_gate(self.car.next_reward_gate_i),
                           self.track.update_next_reward_gate_index(self.car.next_reward_gate_i)):
            rew += 1
        ################################################################################################################

        rew = self.scale(rew, "reward")
        self.total_reward += rew
        return rew

    def _done(self):
        done = False

        # """CHANGE DONE HERE""" #######################################################################################
        self.car.collision(self.track.border_vertices())
        if self.car.is_collision:
            done = True
        ################################################################################################################

        return done

    def _info(self):
        info = {
            "l": self.steps,
            "r": self.total_reward,
            # """CHANGE INFO HERE""" ###################################################################################
            "time": round(self.car.get_time(), 2),
            "score": self.car.score,
            ############################################################################################################
        }
        return info

    def reset(self):
        self.steps = 0
        self.total_reward = 0.

        # """CHANGE RESET HERE""" ######################################################################################
        self.track = Track()
        self.car = Car(lim_features=self.lim_features)

        (self.car.x_pos, self.car.y_pos), self.car.theta = self.track.start_line()
        self.track.create_reward_gates()
        self.car.next_reward_gate_i = self.track.start_reward_gate(self.car.vertices())
        ################################################################################################################

        if not self.train:
            self.reset_render()

        return self._obs()

    def step(self, action):
        # """CHANGE STEP HERE""" #######################################################################################
        self.car.move(action)
        ################################################################################################################

        if not self.train:
            self.step_render()

        self.steps += 1

        return self._obs(), self._rew(), self._done(), self._info()

    def reset_render(self):
        # """CHANGE RESET RENDER HERE""" ###############################################################################
        self.track.create_track_polygons()
        ################################################################################################################

    def step_render(self):
        # """CHANGE STEP RENDER HERE""" ################################################################################
        pass
        ################################################################################################################

    def render(self, mode='human'):
        pass
