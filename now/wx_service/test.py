# def try_werobot():
#     import werobot
#     pass

# try:
#     b = 1
#     a = b
#     print(a)
# except SyntaxError:
#     print("SyntaxError")
# except NameError:
#     print("NameError")
# else:
#     print("Ok")
# finally:
#     print("Finally")

# print(round(2 - 1.59, 3))

from decimal import Decimal
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        f = func(*args, **kwargs)
        end_time = time.time()
        print("执行函数{}使用了{}秒".format(
            getattr(func, "__name__"), end_time - start_time))
        return f

    return wrapper


@timer
def test_decimal():
    for _ in range(1000000):
        num = '{:.2f}'.format(Decimal('2') - Decimal('1.59'))


@timer
def test_round():
    for _ in range(1000000):
        number = round(2 - 1.59, 2)


@timer
def test_decimal_1():
    for _ in range(1000000):
        num = '{:.2f}'.format(2 - Decimal('1.59'))


@timer
def test_format():
    a = "string"
    for _ in range(1000000):
        string = "string %s" % a


@timer
def test_format_1():
    a = "string"
    for _ in range(1000000):
        string = ""
        string += a


@timer
def test_format_2():
    a = "string"
    for _ in range(1000000):
        string = "string {}".format(a)


@timer
def test_int():
    for _ in range(1000000):
        int("66")


if __name__ == "__main__":
    test_int()
    # test_format()
    # test_format_1()
    # test_format_2()
    # test_round()
    # test_decimal()
    # test_decimal_1()