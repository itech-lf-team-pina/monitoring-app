import os

from flask import Flask
from app.log.log import Log


def create_app(test_config=None):
    # create and configure the app
    app: Flask = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/status')
    def hello():
        return 'up!'

    from app.log.show_log import show_log
    app.register_blueprint(show_log.bp)

    Log.write('Server started')

    return app
