#!/bin/bash

: '
while true; do
  python3 train.py;
done
'

echo "train lr"
echo ""

python3 train.py -lr 0.01 -max_total_steps 2000000
python3 train.py -lr 0.001 -max_total_steps 2000000
python3 train.py -lr 0.0001 -max_total_steps 2000000
python3 train.py -lr 0.00001 -max_total_steps 2000000

exit

