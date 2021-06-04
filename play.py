from env import Env, View


class Play(View):
    def __init__(self, *args, **kwargs):
        super(Play, self).__init__(*args, **kwargs)

    def setup(self):
        _ = self.env.reset()

    def loop(self):
        action = self.get_play_action

        _, _, done, _ = self.env.step(action)
        if done:
            self.setup()


if __name__ == "__main__":

    Play("PLAY", Env()).run()
