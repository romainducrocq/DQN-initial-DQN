### initial-DQN

My own DQN library for custom environments. Supports:  
- Custom environments in OpenAI gym framework.  
- Dynamic save and load with msgpack.
- Multi-processing learning.  
- Tensorboard visualization.  

How to use:  
1. Create a custom environment in env/ with a pyglet view and a gym wrapper.  
2. Configure the hyperparameters and neural net architecture in dqn/config/dqn_config.py.  
3. Train the model with `python3 train.py -algo PerDuelingDoubleDQNAgent -max_total_steps 18000000`.  
4. Observe the AI with `python3 observe.py -dir save/PerDuelingDoubleDQNAgent_lr5e-05_model.pack -max_steps 500`.  
5. Visualize the learning curves in tensorboard with `tensorboard --logdir ./logs/`.  
6. And beat the AI with `python3 play.py` to assert dominance on the machines.  
 
The following algorithms are implemented:  
- DQN: vanilla DQN.  
- DDQN: Double DQN.  
- 3DQN: Dueling Double DQN.  
- Per3DQN: Dueling Double DQN with Priority Experience Replay.  

### Software Requirements

- Python 3.7  
> sudo apt-get update && sudo apt-get install build-essential libpq-dev libssl-dev openssl libffi-dev sqlite3 libsqlite3-dev libbz2-dev zlib1g-dev cmake python3.7 python3-pip python3.7-dev python3.7-venv  

- venv  
> mkdir venv && python3.7 -m venv venv/  
> source venv/bin/activate  
> deactivate  

- pyglet, gym, torch, tensorboard, msgpack, wheel  
> (venv) pip3 install 'pyglet==1.5.0' gym torch tensorboard 'msgpack==1.0.2' wheel --no-cache-dir  

### Demo

![Demo gif](demo/demo.gif)

![Demo tensorboard png](demo/demo_tensorboard.png)

### How To Build a Custom Environment

This library provides a framework designed to wrap and support any custom environment for applying DQN algorithms. All sections to be modified are indicated by comments.
No uncommented section should require any modification, especially no code related to the DQN algorithms. Are to be modified only:
- The environment model folder `env/custom_env/`,
- The environment view file `env/view.py`,
- The environment controller wrapper filer `env/custom_env_wrapper.py`,
- The entry programs interacting with the view `play.py` and `observe.py`,
- The DQN hyperparameter configuration file `dqn/config/dqn_config.py`.

1. **Model:**
1.1. In the `env/custom_env/` folder, create the environment model. Do so in an object-oriented fashion, as the transition dynamic is wrapped in an external controller. E.g: car.py, track.py, utils.py.
2. **Controller:**
2. In the `env/custom_env_wrapper.py` file, wrap the environment controller in the `CustomEnvWrapper` class:  
	- Import the environment model,  
	- In `__init__`: construct the environment, define the feature scaling, and the action/observation spaces,  
	- Define the observation in `_obs`, the reward in `_rew`, the end condition in `_done`, and add infos in `_info`,  
	- Define the initial state in `reset`, and the transition dynamics in `step`,  
	- (Optional) Define additional rendering instructions in `reset_render` and `step_render`, for the view only.  

3. **With Pyglet**  
The framework uses Pyglet for the view by default.  
3. In the `env/view.py` file, wrap the environment view in the `View` class:  
	- Import the environment utils,  
	- In `__init__`: initilialize the Pyglet parameters and define the view setup,  
	- Defin the view loop in `on_draw`.   




****

https://www.youtube.com/watch?v=dv13gl0a-FA  
