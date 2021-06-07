from env import Env, View
from dqn.config import HYPER_PARAMS
from dqn import make_env, Networks

import os
import argparse
import numpy as np
from functools import reduce

from torch import device, cuda


class Observe(View):
    def __init__(self, name, env, args):
        os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
        os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu

        # TODO
        # super(Observe, self).__init__(name, make_env(env=env, max_episode_steps=args.max_steps))
        super(Observe, self).__init__(name, make_env(env=env, repeat=HYPER_PARAMS['repeat'], max_episode_steps=args.max_steps))

        self.model_pack = args.d.split('/')[-1].split('_model.pack')[0]

        self.network = getattr(Networks, {
            "DQNAgent": "DeepQNetwork",
            "DoubleDQNAgent": "DeepQNetwork",
            "DuelingDoubleDQNAgent": "DuelingDeepQNetwork",
            "PerDuelingDoubleDQNAgent": "DuelingDeepQNetwork"
        }[self.model_pack.split('_lr')[0]])(
            device(("cuda:" + args.gpu) if cuda.is_available() else "cpu"),
            float(self.model_pack.split('_lr')[1].split('_')[0]),
            reduce(lambda x, y: x * y, list(self.env.observation_space.shape)),
            self.env.action_space.n
        )

        self.network.load(args.d)

        self.obs = np.zeros(reduce(lambda x, y: x * y, list(self.env.observation_space.shape)), dtype=np.float32)

        self.repeat = 0
        self.action = 0

    def setup(self):
        self.obs = self.env.reset()

        self.repeat = 0

    def loop(self):
        # TODO
        # if self.repeat % (HYPER_PARAMS['repeat'] or 1) == 0:
        if self.repeat % (0 or 1) == 0:
            self.action = self.network.actions([self.obs.tolist()])[0]

        self.repeat += 1

        self.obs, _, done, info = self.env.step(self.action)
        if done:
            self.setup()

            print()
            [print(k, ":", info[k]) for k in info]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OBSERVE")
    parser.add_argument('-d', type=str, default='', help='Directory', required=True)
    parser.add_argument('-max_steps', type=int, default=HYPER_PARAMS['max_episode_steps'], help='Max episode steps')
    parser.add_argument('-gpu', type=str, default='0', help='GPU #')

    Observe("OBSERVE", Env("observe"), parser.parse_args()).run()
