from webserver.server import create_app


class Main:
    webserver = create_app().run()


def main():
    """ Main program """
    start = Main()


if __name__ == "__main__":
    main()