#!/usr/bin/bash

cd ../

source venv/bin/activate
if [ -z "${1}" ]; then
    python3 observe.py -d save/PerDuelingDoubleDQNAgent_lr5e-05_model.pack -max_s 500
else
    python3 observe.py "${@}"
fi
deactivate

exit
