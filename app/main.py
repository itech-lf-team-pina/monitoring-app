from webserver.server import create_app


class Main:
    create_app().run('0.0.0.0', 5000)


if __name__ == "__main__":
    Main()
