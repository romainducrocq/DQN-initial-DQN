### Build a custom environment

This library provides a framework designed to wrap custom environments for applying DQN algorithms.  
All sections to be modified are indicated by comments. Are to be modified only:  
- The environment model package: `env/custom_env/`.  
- The environment view file: `env/view.py`.  
- The environment controller wrapper file: `env/custom_env_wrapper.py`.  
- The entry program files interacting with the view: `play.py` and `observe.py`.  
- The DQN hyperparameter configuration file: `dqn/config/dqn_config.py`.  

### 1. Model

Create the custom environment model.  

**package `env/custom_env/`**  
1. create the environment model classes. E.g: car.py, track.py.  
2. create additional resources. E.g: utils.py, img/.  

**file `env/custom_env/utils.py`**  
1. `RES` -> _(int, int)_: set the window resolution.  
2. define the global constants and functions.  

### 2. Controller

Wrap the environment controller in gym.  

**file `env/custom_env_wrapper.py`**, **class `CustomEnvWrapper`**   
1. `import`: import the environment model.  
2. `__init__()`:  
    - 2.1: construct the environment objects.  
    - 2.2: `MAX_FEATURES` -> _dict_: set the feature scaling.  
    - 2.3: `action_space` -> _gym.spaces.Discrete\<int>_: set the action space.  
    - 2.4: `observation_space`: -> _gym.spaces.Box<np.float32>_: set the observation space.  
3. `_obs()` -> _np.ndarray<np.float32>_: define the observation function, scaled in [0, 1].  
4. `_rew()` -> _float_: define the step reward function, scaled in [0, 1].  
5. `_done()` -> _bool_: define the end function.  
6. `_info()` -> _dict_: (optional) add log infos.  
7. `reset()` -> _np.ndarray_: define the initial state.  
8. `step(action)` -> _(np.ndarray, float, bool, dict)_: define the transition dynamic for one timestep.  
9. `reset_render()`: (optional) add reset instructions for the view only.  
10. `step_render()`: (optional) add step instructions for the view only.  

### 3. View

**3.1 View with pyglet**  

Wrap the environment view in pyglet.  

**file `env/view.py`**, **class `View`**   
1. `import`: import the environment utils global constants.  
2. `__init__()`:  
    - 2.1: `(width, height)`, `background_color` -> \<int>: initialize the pyglet parameters.  
    - 2.2: define the view setup.  
3. `on_draw()`: define the view loop.  

**file `play.py`**, **class `Play`**   
1. `__init__()`:   
    - 1.1: `noop` -> _int_: set the noop action.  
    - 1.2: `action_keys` -> _dict_: set the action keys.  

**file `observe.py`**, **class `Observe`**   
1. `loop()`: (optional) synchronize the frame rate in case of frame skipping.  

**3.2 View without pyglet**  

Create the environment view without pyglet.  

**file `env/view.py`**, **class `View`**   
1. create the environment view.  
2. `setup()`, `loop()`: keep.  
3. `run()`: create an infinite event loop running loop() and the view loop.  

**file `play.py`**  
1. `import`: fit to view.  
2. `class Play`: fit to view.  
3. `__main__`: construct the view object and run run().  

**file `observe.py`**  
1. `import`: fit to view.  
2. `__main__`: construct the view object and run run().  

### 4. Hyperparameter tuning

Tune the hyperparameters and the network configuration.  

**file `dqn/config/dqn_config.py`**   
1. `HYPER_PARAMS` -> _dict_: set the hyperparameters.  
2. `network_config(input_dim)` -> _(torch.nn.Sequential, function, function, int)_:  
    - 2.1 `net` -> _torch.nn.Sequential_: define the neural network.  
    - 2.2 `optim_func` -> _function_: define the optimizer function.  
    - 2.3 `loss_func` -> _function_: define the loss function.  
    - 2.4 `fc_out_dim` -> _int_: set the output dimension passed to the dueling layer.  

****

### Run `play.py`, `observe.py`, `train.py`

- play.py
```
python3 play.py

PLAY
```

- observe.py
```
python3 observe.py [-h] -dir DIR [-max_steps MAX_STEPS] [-gpu GPU]

OBSERVE

optional arguments:
  -h, --help            show this help message and exit
  -dir DIR              Directory
  -max_steps MAX_STEPS  Max episode steps
  -gpu GPU              GPU #

```

- train.py
```
python3 train.py [-h] [-gpu GPU] [-n_env N_ENV] [-lr LR] [-gamma GAMMA]
                 [-eps_start EPS_START] [-eps_min EPS_MIN] [-eps_dec EPS_DEC]
                 [-eps_dec_exp EPS_DEC_EXP] [-bs BS] [-min_mem MIN_MEM]
                 [-max_mem MAX_MEM] [-target_update_freq TARGET_UPDATE_FREQ]
                 [-target_soft_update TARGET_SOFT_UPDATE]
                 [-target_soft_update_tau TARGET_SOFT_UPDATE_TAU]
                 [-save_freq SAVE_FREQ] [-log_freq LOG_FREQ]
                 [-save_dir SAVE_DIR] [-log_dir LOG_DIR] [-load LOAD]
                 [-repeat REPEAT] [-max_episode_steps MAX_EPISODE_STEPS]
                 [-max_total_steps MAX_TOTAL_STEPS] [-algo ALGO]

TRAIN

optional arguments:
  -h, --help            show this help message and exit
  -gpu GPU              GPU #
  -n_env N_ENV          Multi-processing environments
  -lr LR                Learning rate
  -gamma GAMMA          Discount factor
  -eps_start EPS_START  Epsilon start
  -eps_min EPS_MIN      Epsilon min
  -eps_dec EPS_DEC      Epsilon decay
  -eps_dec_exp EPS_DEC_EXP
                        Epsilon exponential decay
  -bs BS                Batch size
  -min_mem MIN_MEM      Replay memory buffer min size
  -max_mem MAX_MEM      Replay memory buffer max size
  -target_update_freq TARGET_UPDATE_FREQ
                        Target network update frequency
  -target_soft_update TARGET_SOFT_UPDATE
                        Target network soft update
  -target_soft_update_tau TARGET_SOFT_UPDATE_TAU
                        Target network soft update tau rate
  -save_freq SAVE_FREQ  Save frequency
  -log_freq LOG_FREQ    Log frequency
  -save_dir SAVE_DIR    Save directory
  -log_dir LOG_DIR      Log directory
  -load LOAD            Load model
  -repeat REPEAT        Steps repeat action
  -max_episode_steps MAX_EPISODE_STEPS
                        Episode step limit
  -max_total_steps MAX_TOTAL_STEPS
                        Max total training steps
  -algo ALGO            DQNAgent DoubleDQNAgent DuelingDoubleDQNAgent
                        PerDuelingDoubleDQNAgent
```

