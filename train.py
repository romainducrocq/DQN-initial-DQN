from env import Env
from dqn.config import HYPER_PARAMS
from dqn import make_env, Agents

import os
import time
import argparse
import itertools
from functools import reduce
from datetime import timedelta


class Train:
    def __init__(self, args, env):
        os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
        os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu

        self.env = make_env(
            env=env,
            repeat=HYPER_PARAMS['repeat'],
            max_episode_steps=HYPER_PARAMS['max_episode_steps'],
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
        print(args.algo)
        print()
        print(self.agent.online_network)

        self.max_total_steps = args.max_total_steps

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
                print('---', str(timedelta(seconds=round((time.time() - self.agent.start_time), 0))), '---')

    def train_loop(self):
        print()
        print("Start Training")

        obses = self.env.reset()
        for step in itertools.count(start=self.agent.resume_step):
            self.agent.step = step

            actions = self.agent.choose_actions(obses)

            new_obses, rews, dones, infos = self.env.step(actions)

            self.agent.store_transitions(obses, actions, rews, dones, new_obses, infos)

            obses = new_obses

            self.agent.learn()

            self.agent.update_target_network()

            self.agent.log()

            self.agent.save_model()

            if bool(self.max_total_steps) and step >= self.max_total_steps:
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initial DQN - TRAIN")
    parser.add_argument('-n_env', type=int, default=HYPER_PARAMS["n_env"], help='Multi-processing environments')
    parser.add_argument('-lr', type=float, default=HYPER_PARAMS["lr"], help='Learning rate')
    parser.add_argument('-gamma', type=float, default=HYPER_PARAMS["gamma"], help='Discount factor')
    parser.add_argument('-eps_start', type=float, default=HYPER_PARAMS["eps_start"], help='Epsilon start')
    parser.add_argument('-eps_min', type=float, default=HYPER_PARAMS["eps_min"], help='Epsilon min')
    parser.add_argument('-eps_dec', type=float, default=HYPER_PARAMS["eps_dec"], help='Epsilon decay')
    parser.add_argument('-bs', type=int, default=HYPER_PARAMS["bs"], help='Batch size')
    parser.add_argument('-min_mem', type=int, default=HYPER_PARAMS["min_mem"], help='Replay memory buffer min size')
    parser.add_argument('-max_mem', type=int, default=HYPER_PARAMS["max_mem"], help='Replay memory buffer max size')
    parser.add_argument('-target_update_freq', type=int, default=HYPER_PARAMS["target_update_freq"], help='Target network update frequency')
    parser.add_argument('-save_freq', type=int, default=HYPER_PARAMS["save_freq"], help='Save frequency')
    parser.add_argument('-log_freq', type=int, default=HYPER_PARAMS["log_freq"], help='Log frequency')
    parser.add_argument('-save_dir', type=str, default=HYPER_PARAMS["save_dir"], help='Save directory')
    parser.add_argument('-log_dir', type=str, default=HYPER_PARAMS["log_dir"], help='Log directory')
    parser.add_argument('-load', type=bool, default=HYPER_PARAMS["load"], help='Load model')
    parser.add_argument('-max_total_steps', type=int, default=HYPER_PARAMS["max_total_steps"], help='Max total training steps')
    parser.add_argument('-algo', type=str, default=HYPER_PARAMS["algo"],
                        help='DQNAgent ' +
                             'DoubleDQNAgent ' +
                             'DuelingDoubleDQNAgent '
                        )
    parser.add_argument('-gpu', type=str, default=HYPER_PARAMS["gpu"], help='GPU #')

    train = Train(
        args=parser.parse_args(),
        env=Env()
    )

    train.init_replay_memory_buffer()

    train.train_loop()
