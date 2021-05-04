from env.track import Track
from env.car import Car


class Env:
    def __init__(self):
        self.track = Track()
        self.car = Car()
        self.action_space_n = self.car.action_n()
        self.observation_space_n = self.car.observation_n()

    def action_space_sample(self):
        return self.car.action_sample()

    def reset_render(self):
        return self.track.create_track_polygons()

    def reset(self):
        self.track = Track()
        self.car = Car()

        (self.car.x_pos, self.car.y_pos), self.car.theta = self.track.start_line()
        self.track.create_reward_gates()
        self.car.next_reward_gate_i = self.track.start_reward_gate(self.car.vertices())
        self.car.sonar(self.track.border_vertices())

        self.test_print()

        return self.car.obs()

    def step(self, action):
        self.car.move(action)
        self.car.sonar(self.track.border_vertices())
        self.car.reward(self.track.next_reward_gate(self.car.next_reward_gate_i),
                        self.track.update_next_reward_gate_index(self.car.next_reward_gate_i))

        self.car.collision(self.track.border_vertices())

        return self.car.step()

    def test_print(self):
        print("Sample: ", self.action_space_sample())
        print("Action space n: ", self.action_space_n)
        print("Observation space n:", self.observation_space_n)
        print()
