#!/bin/bash

DIRPATH="/root/workoo/gd/"

cd $DIRPATH

#gdggzy
cd "${DIRPATH}"
nohup python3 gdggzy.py &

#gdedulscg.cn
cd "${DIRPATH}"
nohup python3 gdedulscg.cn.py &
