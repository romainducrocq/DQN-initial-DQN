from env import Env, View
from dqn import make_env

import argparse


class Play(View):
    def __init__(self, name, env, args):
        super(Play, self).__init__(name, make_env(env=env, max_episode_steps=args.max_s))

        self.ep = 0

        print()
        print("PLAY")
        print()
        [print(arg, "=", getattr(args, arg)) for arg in vars(args)]

        self.max_episodes = args.max_e
        self.log = (args.log, args.log_s, "./logs/test/" + args.player)

    def setup(self):
        _ = self.env.reset()

    def loop(self):
        action = self.get_play_action()

        _, _, done, info = self.env.step(action)
        Env.log_info_csv(info, done, *self.log)

        if done:
            self.setup()

            self.ep += 1

            print()
            print("Episode :", self.ep)
            [print(k, ":", info[k]) for k in info]

            if bool(self.max_episodes) and self.ep >= self.max_episodes:
                exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PLAY")
    str2bool = (lambda v: v.lower() in ("yes", "y", "true", "t", "1"))
    parser.add_argument('-max_s', type=int, default=0, help='Max steps per episode if > 0, else inf')
    parser.add_argument('-max_e', type=int, default=0, help='Max episodes if > 0, else inf')
    parser.add_argument('-log', type=str2bool, default=False, help='Log csv to ./logs/test/')
    parser.add_argument('-log_s', type=int, default=0, help='Log step if > 0, else episode')
    parser.add_argument('-player', type=str, default='player', help='Player')

    Play("PLAY", Env("play"), parser.parse_args()).run()
