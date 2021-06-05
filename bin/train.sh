#!/usr/bin/bash

function run () {

python3 train.py -algo PerDuelingDoubleDQNAgent -max_total_steps 18000000

}

cd ..

source venv/bin/activate

run

deactivate

exit
