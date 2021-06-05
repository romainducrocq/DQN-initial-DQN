#!/usr/bin/bash

function run () {

python3 observe.py -dir save/PerDuelingDoubleDQNAgent_lr5e-05_model.pack -max_steps 500	

}

cd ..

source venv/bin/activate

run

deactivate

exit
