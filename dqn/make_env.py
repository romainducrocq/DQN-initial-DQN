from .utils.baselines_wrappers import DummyVecEnv, SubprocVecEnv, Monitor


def make_vec_env(env, n_env):
    if n_env > 1:
        return SubprocVecEnv([lambda: Monitor(env, allow_early_resets=True) for _ in range(n_env)])
    else:
        return DummyVecEnv([lambda: Monitor(env, allow_early_resets=True) for _ in range(n_env)])
