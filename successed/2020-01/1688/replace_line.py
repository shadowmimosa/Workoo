import csv

with open('./data/final.csv', 'r') as fin:  #读有空行的csv文件，舍弃空行
    lines = ''
    for line in fin:
        if line != '\n':
            lines += line
            
with open('E:\\test.csv', 'wt') as fout:  #再次文本方式写入，不含空行
    fout.write(lines)
