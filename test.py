import subprocess


def a():
    print('djfal')


if __name__ == "__main__":
    port = subprocess.check_output(['git status'], shell=True).decode()
    port = port.split('\n')
    for i in port:
        print(i)

    a = {
        'a': a
    }
    a['a']()
