Implemented from my DQN framework: https://github.com/romainducrocq/frameworQ

****

### initial-DQN

Déjà vu, I've just been in this place before?  
https://www.youtube.com/watch?v=dv13gl0a-FA  

1. Train: `python3 train.py -algo PerDuelingDoubleDQNAgent -max_total_steps 18000000`
2. Observe: `python3 observe.py -d save/PerDuelingDoubleDQNAgent_lr5e-05_model.pack -max_s 500`
3. Visualize: `tensorboard --logdir ./logs/train/`
4. Play: `python3 play.py`

****

### Build dependencies

make: `cd bin/ && bash make.sh`


1. Apt packages:  
> apt-get update && apt-get install build-essential libpq-dev libssl-dev openssl libffi-dev sqlite3 libsqlite3-dev libbz2-dev zlib1g-dev cmake  

2. Python 3.7.m:  
> m=0 && while wget -q --method=HEAD https<area>://www<area>.python.org/ftp/python/3.7.$(( $m + 1 ))/Python-3.7.$(( $m + 1 )).tar.xz; do m=$(( $m + 1 )); done && wget https<area>://www<area>.python.org/ftp/python/3.7.$m/Python-3.7.$m.tar.xz && tar xvf Python-3.7.$m.tar.xz && cd Python-3.7.$m && ./configure && make && make altinstall && cd .. && rm -rv Python-3.7.$m.tar.xz Python-3.7.$m  

3. Venv (venv):  
> mkdir venv && python3.7 -m venv venv/  
> source venv/bin/activate  
> (venv) ... *Pip3 packages*  
> deactivate  

4. Pip3 packages:  
> (venv) export TMPDIR='/var/tmp'  
> (venv) pip3 install 'pyglet==1.5.0' gym torch tensorboard 'msgpack==1.0.2' wheel --no-cache-dir  

****

### Demo

![Demo gif](demo/demo.gif)

![Demo tensorboard png](demo/demo_tensorboard.png)

