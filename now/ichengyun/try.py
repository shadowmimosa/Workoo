import os
import sys
import time
import atexit
import signal
import traceback


def term_sig_handler(signum, frame):
    print("catched singal: %d' % signum ")
    sys.exit()


@atexit.register
def atexit_fun():
    print("i am exit, stack track:")

    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_tb)


if __name__ == '__main__':
    # catch term signal
    signal.signal(signal.SIGTERM, term_sig_handler)
    signal.signal(signal.SIGINT, term_sig_handler)
    while True:
        print("hello")
        time.sleep(3)
