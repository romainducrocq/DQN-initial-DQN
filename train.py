from env import Env
from dqn import DeepQNetwork


import os
import argparse
import gym
from collections import deque
import itertools
import numpy as np
import random
import time



from torch.utils.tensorboard import SummaryWriter

from dqn.utils.baselines_wrappers import DummyVecEnv, SubprocVecEnv, Monitor

import msgpack
from dqn.utils import msgpack_numpy_patch

if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(description="Initial DQN - TRAIN")
    parser.add_argument('-lr', type=float, default=0.00025, help='Learning rate')
    parser.add_argument('-gamma', type=float, default=0.95, help='Discount factor')
    parser.add_argument('-eps_start', type=float, default=1., help='Epsilon start')
    parser.add_argument('-eps_min', type=float, default=0.01, help='Epsilon min')
    parser.add_argument('-eps_dec', type=float, default=1e6, help='Epsilon decay')
    parser.add_argument('-bs', type=int, default=32, help='Batch size')
    parser.add_argument('-min__mem', type=int, default=50000, help='Replay memory buffer min size')
    parser.add_argument('-max_mem', type=int, default=500000, help='Replay memory buffer max size')
    parser.add_argument('-target_update_freq', type=int, default=10000, help='Target network update frequency')
    parser.add_argument('-save_freq', type=int, default=10000, help='Save frequency')
    parser.add_argument('-log_freq', type=int, default=1000, help='Log frequency')
    parser.add_argument('-save_path', type=str, default='./save/', help='Save path')
    parser.add_argument('-log_path', type=str, default='./logs/', help='Log path')
    parser.add_argument('-gpu', type=str, default='0', help='GPU #')
    parser.add_argument('-algo', type=str, default='DQNAgent', help='DQNAgent')
    args = parser.parse_args()

    os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu

    env = Env()

    dqn = DeepQNetwork(args.lr, env.observation_space.shape[0], env.action_space.n)





