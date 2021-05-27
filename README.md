### initial-DQN

My own DQN library for custom environments. Supports:  
- Custom environments in OpenAI gym framework.  
- Dynamic save and load with msgpack.
- Multi-processing learning.  
- Tensorboard visualization.  

How to use:  
1. Create a custom environment in env/ with pyglet and wrap it in gym in env/custom_env.py.  
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

****

https://www.youtube.com/watch?v=dv13gl0a-FA  
