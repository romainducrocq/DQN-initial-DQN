import random
from collections import deque


class ReplayMemory:
    def __init__(self, buffer_size, batch_size):
        self.batch_size = batch_size
        self.replay_buffer = deque(maxlen=buffer_size)

    def store_transitions(self, obses, actions, rews, dones, new_obses):
        raise NotImplementedError

    def sample_transitions(self):
        raise NotImplementedError


class ReplayMemoryNaive(ReplayMemory):
    def __init__(self, *args, **kwargs):
        super(ReplayMemoryNaive, self).__init__(*args, **kwargs)

    def store_transitions(self, obses, actions, rews, dones, new_obses):
        for e, (obs, action, rew, done, new_obs) in enumerate(zip(obses, actions, rews, dones, new_obses)):
            transition = (obs, action, rew, done, new_obs)
            self.replay_buffer.append(transition)

            if done:
                yield e

    def sample_transitions(self):
        return random.sample(self.replay_buffer, self.batch_size)
