import time

from webserver.server import create_app
from log.log import Log


class Main:
    log = Log()

    print('Test')

    # log.write('Test')
    # print(log.read())

    create_app().run('0.0.0.0', 5000)


def main():
    """ Main program """
    main_class = Main()


if __name__ == "__main__":
    main()
