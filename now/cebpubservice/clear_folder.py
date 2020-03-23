import os
import shutil
import datetime


def out_time(path):
    for folder in os.listdir(path):
        folder_time = datetime.datetime.strptime(folder, '%Y-%m-%d')
        if folder_time + datetime.timedelta(3) < datetime.datetime.now():
            fullpath = os.path.join(path, folder)
            shutil.rmtree(fullpath)
            print(f'已删除 - {fullpath}')


def main():
    for folder in ['pic', 'pic_raw', 'pdf']:
        out_time(f'./static/{folder}')


if __name__ == "__main__":
    main()