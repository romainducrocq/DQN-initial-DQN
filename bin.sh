#!/usr/bin/bash

LIGHT_GREEN='\033[1;32m'
LIGHT_CYAN='\033[1;36m'
NC='\033[0m' 

function help () {
  echo -e "${LIGHT_CYAN}SYNOPSIS${NC}"
  echo -e "\t./bin ${LIGHT_GREEN}-p${NC} | ${LIGHT_GREEN}-v${NC} | ${LIGHT_GREEN}-o${NC} | ${LIGHT_GREEN}-t${NC} | ${LIGHT_GREEN}-h${NC}\n"
  echo -e "${LIGHT_CYAN}DESCRIPTION${NC}"
  echo -e "\tRun:\n"
  echo -e "\t\t${LIGHT_GREEN}-p${NC} - play\n"
  echo -e "\t\t${LIGHT_GREEN}-v${NC} - visualize\n"
  echo -e "\t\t${LIGHT_GREEN}-o${NC} - observe\n"
  echo -e "\t\t${LIGHT_GREEN}-t${NC} - train\n"
  echo -e "\t\t${LIGHT_GREEN}-h${NC} - help\n"
}

source venv/bin/activate

if [ "$1" = "-p" ]; then
  python3 play.py
elif [ "$1" = "-v" ]; then
  tensorboard --logdir ./logs/
elif [ "$1" = "-o" ]; then
  python3 observe.py -dir save/PerDuelingDoubleDQNAgent_lr5e-05_model.pack -max_steps 500
elif [ "$1" = "-t" ]; then
  python3 train.py -algo PerDuelingDoubleDQNAgent -max_total_steps 18000000
else
  help
fi

deactivate

exit
