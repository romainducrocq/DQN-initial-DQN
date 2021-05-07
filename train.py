from env import Env
from dqn import make_env, Agents

import os
import time
import argparse
import itertools
from functools import reduce

REPEAT = 2
MAX_EPISODE_STEPS = 5000

class Train:
    def __init__(self, args, env):
        os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
        os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu

        self.env = make_env(
            env=env,
            repeat=REPEAT,
            max_episode_steps=MAX_EPISODE_STEPS,
            n_env=args.n_env
        )

        self.agent = getattr(Agents, args.algo)(
            n_env=args.n_env,
            lr=args.lr,
            gamma=args.gamma,
            epsilon_start=args.eps_start,
            epsilon_min=args.eps_min,
            epsilon_decay=args.eps_dec,
            input_dim=reduce(lambda x, y: x*y, list(env.observation_space.shape)),
            output_dim=env.action_space.n,
            batch_size=args.bs,
            min_buffer_size=args.min_mem,
            buffer_size=args.max_mem,
            update_target_frequency=(args.target_update_freq // args.n_env),
            save_frequency=args.save_freq,
            log_frequency=args.log_freq,
            save_dir=args.save_dir,
            log_dir=args.log_dir,
            load=args.load,
            algo=args.algo,
            gpu=args.gpu
        )

        self.agent.load_model()

        print()
        print(self.agent.online_network)

    def init_replay_memory_buffer(self):
        print()
        print("Initialize Replay Memory Buffer")

        obses = self.env.reset()
        for t in range(self.agent.min_buffer_size):
            if t >= self.agent.min_buffer_size - self.agent.resume_step:
                actions = self.agent.choose_actions(0, obses)
            else:
                actions = [self.env.action_space.sample() for _ in range(self.agent.n_env)]

            new_obses, rews, dones, _ = self.env.step(actions)
            self.agent.store_transitions(obses, actions, rews, dones, new_obses, None)

            obses = new_obses

            if (t+1) % 10000 == 0:
                print(str(t+1) + ' / ' + str(self.agent.min_buffer_size))
                print('---', round((time.time() - self.agent.start_time), 2), '---')

    def train_loop(self):
        print()
        print("Start Training")

        obses = self.env.reset()
        for step in itertools.count(start=self.agent.resume_step):
            actions = self.agent.choose_actions(step, obses)

            new_obses, rews, dones, infos = self.env.step(actions)

            self.agent.store_transitions(obses, actions, rews, dones, new_obses, infos)

            obses = new_obses

            self.agent.learn()

            self.agent.update_target_network(step)

            self.agent.log(step)

            self.agent.save_model(step)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initial DQN - TRAIN")
    parser.add_argument('-n_env', type=int, default=4, help='Multi-processing environments')
    parser.add_argument('-lr', type=float, default=0.00025, help='Learning rate')
    parser.add_argument('-gamma', type=float, default=0.99, help='Discount factor')
    parser.add_argument('-eps_start', type=float, default=1., help='Epsilon start')
    parser.add_argument('-eps_min', type=float, default=0.1, help='Epsilon min')
    parser.add_argument('-eps_dec', type=float, default=1e6, help='Epsilon decay')
    parser.add_argument('-bs', type=int, default=32, help='Batch size')
    parser.add_argument('-min_mem', type=int, default=500000, help='Replay memory buffer min size')
    parser.add_argument('-max_mem', type=int, default=1000000, help='Replay memory buffer max size')
    parser.add_argument('-target_update_freq', type=int, default=50000, help='Target network update frequency')
    parser.add_argument('-save_freq', type=int, default=10000, help='Save frequency')
    parser.add_argument('-log_freq', type=int, default=1000, help='Log frequency')
    parser.add_argument('-save_dir', type=str, default='./save/', help='Save directory')
    parser.add_argument('-log_dir', type=str, default='./logs/', help='Log directory')
    parser.add_argument('-load', type=bool, default=True, help='Load model')
    parser.add_argument('-algo', type=str, default='DoubleDQNAgent', help='DQNAgent/DoubleDQNAgent')
    parser.add_argument('-gpu', type=str, default='0', help='GPU #')

    train = Train(
        args=parser.parse_args(),
        env=Env()
    )

    train.init_replay_memory_buffer()

    train.train_loop()
