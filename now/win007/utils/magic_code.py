from chardet import detect

def judge_code(path):
    with open(path, 'rb') as fn:
        data = fn.read()
        charinfo = detect(data)

    gb_encode = ["gb2312", "GB2312", "gb18030", "GB18030", "GBK", "gbk"]

    return 'GBK' if charinfo['encoding'] in gb_encode else charinfo['encoding']