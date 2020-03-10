import os
import sys
import ftplib
import socket
from ftplib import FTP


def ftpconnect(host, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp


def uploadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


# # ftp = ftpconnect("47.100.41.79", "xuan", "CXD@gggg")
# ftp = ftpconnect("cs.nzzbw.com", "nzzbw", "nzzbw789")

# uploadfile(ftp, './try.txt', './try.txt')

CONST_HOST = "cs.nzzbw.com"
CONST_USERNAME = "nzzbw"
CONST_PWD = "nzzbw789"
CONST_BUFFER_SIZE = 1024

COLOR_NONE = "\033[m"
COLOR_GREEN = "\033[01;32m"
COLOR_RED = "\033[01;31m"
COLOR_YELLOW = "\033[01;33m"


def connect():
    try:
        ftp = ftplib.FTP(CONST_HOST)
        ftp.login(CONST_USERNAME, CONST_PWD)
        return ftp
    except (socket.error, socket.gaierror):
        print(
            "FTP is unavailable,please check the host,username and password!")
        sys.exit(0)


def disconnect(ftp):
    ftp.quit()


def upload(ftp, filepath):
    with open(filepath, "rb") as fn:
        file_name = os.path.split(filepath)[-1]
        try:
            ftp.storbinary('STOR %s' % file_name, fn, CONST_BUFFER_SIZE)
        except ftplib.error_perm:
            return False
        return True


def download(ftp, filename):
    with open(filename, "wb") as fn:
        try:
            ftp.retrbinary("RETR %s" % filename, fn.write, CONST_BUFFER_SIZE)
        except ftplib.error_perm:
            return False
        return True


def list(ftp):
    ftp.dir()


def find(ftp, filename):
    ftp_f_list = ftp.nlst()
    if filename in ftp_f_list:
        return True
    else:
        return False


def help():
    print("help info:")
    print("[./ftp.py l]\t show the file list of the ftp site ")
    print(
        "[./ftp.py f filenamA filenameB]\t check if the file is in the ftp site"
    )
    print("[./ftp.py p filenameA filenameB]\t upload file into ftp site")
    print("[./ftp.py g filenameA filenameB]\t get file from ftp site")
    print("[./ftp.py h]\t show help info")
    print("other params are invalid")


def main():
    args = sys.argv[1:]
    if len(args) == 0:
        print("Params needed!")
        sys.exit(0)

    ftp = connect()

    if args[0] == "p":
        f_list = args[1:]
        for up_file in f_list:
            if not os.path.exists(up_file):
                print(("UPLOAD: %s " + COLOR_RED + "FAILED" + COLOR_NONE +
                       "  :file not exist") % up_file)
                continue
            elif not os.path.isfile(up_file):
                print(("UPLOAD: %s " + COLOR_RED + "FAILED" + COLOR_NONE +
                       "  :%s is not a file") % (up_file, up_file))
                continue

            if upload(ftp, up_file):
                print(("UPLOAD: %s " + COLOR_GREEN + "SUCCESS" + COLOR_NONE) %
                      up_file)
            else:
                print(("UPLOAD: %s " + COLOR_RED + "FAILED" + COLOR_NONE) %
                      up_file)
    elif args[0] == "g":
        f_list = args[1:]
        for down_file in f_list:
            if not find(ftp, down_file):
                print(
                    ("DOWNLOAD: %s " + COLOR_RED + "FAILED" + COLOR_NONE +
                     "  :%s is not in the ftp site") % (down_file, down_file))
                continue

            if download(ftp, down_file):
                print(
                    ("DOWNLOAD: %s " + COLOR_GREEN + "SUCCESS" + COLOR_NONE) %
                    down_file)
            else:
                print(("DOWNLOAD: %s " + COLOR_RED + "FAILED" + COLOR_NONE) %
                      down_file)

    elif args[0] == "l":
        list(ftp)
    elif args[0] == "f":
        f_list = args[1:]
        for f_file in f_list:
            if find(ftp, f_file):
                print(("SEARCH: %s " + COLOR_GREEN + "EXIST" + COLOR_NONE) %
                      f_file)
            else:
                print(("SEARCH: %s " + COLOR_RED + "NOT EXIST" + COLOR_NONE) %
                      f_file)

    elif args[0] == "h":
        help()
    else:
        print("args are invalid!")
        help()

    disconnect(ftp)


if __name__ == "__main__":
    main()
