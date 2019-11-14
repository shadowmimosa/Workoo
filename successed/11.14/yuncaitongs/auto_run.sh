#!/bin/bash

source  ~/.local/share/virtualenvs/Workoo-7ULLtGnf/bin/activate

#DIRPATH="~/git/Workoo/now/yuncaitongs/"
DIRPATH="/home/xuan/git/Workoo/now/yuncaitongs/"

cd $DIRPATH

#yuncailian
cd "${DIRPATH}/yuncailian"
nohup python spider_lian.py &

#yuncaitong
cd "${DIRPATH}/yuncaitong"
nohup python spider_tong.py &

