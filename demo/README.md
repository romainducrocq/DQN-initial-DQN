### How To Build a Custom Environment

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
    - 2.3: `action_space` -> _gym.spaces.Discrete<int>_: set the action space.  
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

**3. 1 View with pyglet**  

Wrap the environment view in pyglet.  

**file `env/view.py`**, **class `View`**   
1. `import`: import the environment utils global constants.  
2. `__init__()`:  
    - 2.1: `(width, height)`, `background_color` -> <int>: initialize the pyglet parameters.  
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
1. `HYPER_PARAMS` -> _dict_: Set the hyperparameters.  
2. `network_config(input_dim)` -> _(torch.nn.Sequential, function, function, int)_:  
    - 2.1 `net` -> _torch.nn.Sequential_: define the neural network.  
    - 2.2 `optim_func` -> _function_: define the optimizer function.  
    - 2.3 `loss_func` -> _function_: define the loss function.  
    - 2.4 `fc_out_dim` -> _int_: set the output dimension passed to the dueling layer.  

