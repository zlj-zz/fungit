from random import choice, randint
from string import ascii_letters
from time import time


def create_str(n):
    r_lst = []
    for i in range(n):
        temp = ""
        for j in range(randint(5, 11)):
            temp += choice(ascii_letters)
        r_lst.append(temp)
    return r_lst


test_list = create_str(10000)

s1 = time()
print(*test_list, sep="")
t1 = time() - s1

fstr = ""
s2 = time()
for i in test_list:
    fstr = f"{fstr}{i}"
# print(fstr)
t2 = time() - s2

a = []
s3 = time()
for i in test_list:
    a.append(i)
print(*a, sep="")
# print(fstr)
t3 = time() - s3

print(t1, t2, t3)

"""
Time speed:

f'' < %s

append to a list < join string

print(f'') > print(*[])
"""
