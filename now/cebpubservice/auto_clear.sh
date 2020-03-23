#!/bin/bash
DIRPATH="/root/spider/"

#cebpubservice
source /root/.local/share/virtualenvs/cebpubservice-fFFyqeAB/bin/activate
cd "${DIRPATH}/cebpubservice"
nohup python clear_folder.py &
