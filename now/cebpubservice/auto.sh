#!/bin/bash
DIRPATH="/root/spider/"

#cebpubservice
source /root/.local/share/virtualenvs/cebpubservice-fFFyqeAB/bin/activate
cd "${DIRPATH}/cebpubservice"
nohup python run.py &
nohup python sync.py &
