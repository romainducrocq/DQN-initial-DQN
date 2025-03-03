#!/usr/bin/bash

cd ../

source venv/bin/activate
if [ -z "${1}" ]; then
    python3 train.py -algo PerDuelingDoubleDQNAgent -max_total_steps 18000000
else
    python3 train.py "${@}"
fi
deactivate

exit
