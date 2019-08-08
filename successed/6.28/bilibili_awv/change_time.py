import time
import datetime
import os
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

for value in os.listdir("./data/"):
    if "201" in value:
        # with open("./data/{}".format(value),"r",encoding="utf-8") as fn:
        info_ = pd.read_csv("./data/{}".format(value))
        print(info_)
        info_ = info_.drop(columns=["id"])
        info_["time"] = info_["time"].astype(int)
        print(info_)
        info_["time"] = info_["time"].apply(lambda x: time.strftime(
            "%Y-%m-%d", time.localtime(x)))
        print(info_)
        info_.to_csv(
            "./data/final/{}_final.csv".format(value.replace(".csv", "")),
            index=None)
