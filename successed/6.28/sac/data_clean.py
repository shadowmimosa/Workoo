import os
import pandas as pd
import json


def main():
    raw_data = pd.read_excel("./new.xlsx")
    # raw_data = pd.read_excel("./new_0.xls")

    # raw_data = raw_data.rename(
    #     columns={
    #         "RPI_NAME": "姓名",
    #         "SCO_NAME": "性别",
    #         "AOI_NAME": "执业机构",
    #         "CER_NUM": "证书编号",
    #         "PTI_NAME": "执业岗位",
    #         "ECO_NAME": "学历",
    #         "OBTAIN_DATE": "证书取得日期",
    #     },
    #     inplace=True)
    # a.columns = ['a', 'b', 'c']
    # certificate = raw_data["certificate"]
    for index in range(len(raw_data) - 1, -1, -1):
        cer_ = json.loads(raw_data.iloc[index]["certificate"])
        for i, j in enumerate(cer_):
            column = "certificate_{}".format(i)
            if column not in raw_data.columns.values:
                raw_data[column] = ""
            value = json.dumps({
                "证书编号": j["CER_NUM"],
                "取得日期": j["OBTAIN_DATE"],
                "执业机构": j["AOI_NAME"],
                "执业岗位": j["PTI_NAME"],
                "证书状态": j["CERTC_NAME"],
                "离职备案日期": j["OPER_DATE"]
            },
                               ensure_ascii=False)
            # raw_data.iloc[index][column] = value
            raw_data.at[index, column] = value
    raw_data = raw_data.drop(columns=["certificate"])
    raw_data.to_excel("./data_0.xlsx", index=None)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()