### Software Requirements

- Python 3.7  
> wget https://www.python.org/ftp/python/3.7.10/Python-3.7.10.tar.xz  
> tar -xvf Python-3.7.10.tar.xz && rm -v Python-3.7.10.tar.xz && cd Python-3.7.10  
> apt-get install build-essential sqlite3 libsqlite3-dev libbz2-dev zlib1g-dev cmake  
> ./configure && make && make altinstall  

- venv  
> mkdir venv && python3.7 -m venv venv/  
> source venv/bin/activate  
> deactivate  

- pyglet, gym, torch, tensorboard, msgpack, wheel  
> (venv) pip3 install pyglet gym torch tensorboard 'msgpack==1.0.2' wheel

- tensorboard:
> tensorboard --logdir ./logs/
> rm -rv logs/*

****

State space (n=9): 8 sonar distances, speed  
Action space (n=5): up, right, down, left, none  
Reward: score  
