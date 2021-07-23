# """CHANGE CUSTOM ENV IMPORT HERE""" ##################################################################################
from .custom_env import Track, Car, RES
########################################################################################################################


class DqnEnv:

    def min_max_scale(self, x, feature):
        return (x - self.min_max[feature][0]) / (self.min_max[feature][1] - self.min_max[feature][0])

    def __init__(self, m, p=None):
        self.mode = {"train": False, "observe": False, "play": False, m: True}
        self.player = p if self.mode["play"] else None

        # """CHANGE ENV CONSTRUCT HERE""" ##############################################################################
        self.track = Track()
        self.car = Car()
        ################################################################################################################

        # """CHANGE FEATURE SCALING HERE""" ############################################################################
        self.min_max = {
            "speed": (0., 50. if self.mode["train"] else 35.),
            "sonar_distance": (0., RES[0]),
            "rew": (0., 1.)
        }
        ################################################################################################################

        # """CHANGE ACTION AND OBSERVATION SPACE SIZES HERE""" #########################################################
        self.action_space_n = len(self.car.actions)
        self.observation_space_n = self.car.n_sonars + 1
        ################################################################################################################

    def obs(self):
        # """CHANGE OBSERVATION HERE""" ################################################################################
        self.car.sonar(self.track.border_vertices())

        obs = [self.min_max_scale(sonar_distance, "sonar_distance") for sonar_distance in self.car.sonar_distances] + \
              [self.min_max_scale(self.car.speed, "speed")]
        ################################################################################################################
        return obs

    def rew(self):
        # """CHANGE REWARD HERE""" #####################################################################################
        rew = 0.
        if self.car.reward(self.track.next_reward_gate(self.car.next_reward_gate_i),
                           self.track.update_next_reward_gate_index(self.car.next_reward_gate_i)):
            rew = 1.
        ################################################################################################################
        return rew

    def done(self):
        # """CHANGE DONE HERE""" #######################################################################################
        self.car.collision(self.track.border_vertices())
        done = self.car.is_collision
        ################################################################################################################
        return done

    def info(self):
        # """CHANGE INFO HERE""" #######################################################################################
        info = {
            "time": round(self.car.get_time(), 2),
            "score": self.car.score
        }
        ################################################################################################################
        return info

    def reset(self):
        # """CHANGE RESET HERE""" ######################################################################################
        self.track = Track()
        self.car = Car(lim_features=self.min_max)

        (self.car.x_pos, self.car.y_pos), self.car.theta = self.track.start_line()
        self.track.create_reward_gates()
        self.car.next_reward_gate_i = self.track.start_reward_gate(self.car.vertices())
        ################################################################################################################

    def step(self, action):
        # """CHANGE STEP HERE""" #######################################################################################
        self.car.move(action)
        ################################################################################################################

    def reset_render(self):
        # """CHANGE RESET RENDER HERE""" ###############################################################################
        self.track.create_track_polygons()
        ################################################################################################################

    def step_render(self):
        # """CHANGE STEP RENDER HERE""" ################################################################################
        pass
        ################################################################################################################
