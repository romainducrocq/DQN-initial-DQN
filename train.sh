#!/bin/bash

: '
while true; do
  python3 train.py;
done
'

echo ""

mkdir logs/train/DuelingDoubleDQNAgent_lr5e-05_train/
cp -rv logs/DuelingDoubleDQNAgent_lr5e-05/* logs/train/DuelingDoubleDQNAgent_lr5e-05_train/ && tensorboard --logdir logs/train

exit

