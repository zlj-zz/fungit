import random
import time


l = [str(random.randint(0, 10000000000000)) for _ in range(100000)]

str_ = "12123213213232131231"
l_ = []


def test_str():
    start = time.time()
    str_ = ""
    for item in l:
        str_ += item
    print(str_)
    return time.time() - start


def test_list():
    start = time.time()
    l_.clear()
    for item in l:
        l_.append(item)
    print(*l_)
    return time.time() - start


if __name__ == "__main__":
    t1 = test_str()
    t2 = test_list()
    print(t1, t2)
