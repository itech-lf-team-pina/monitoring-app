import array
import os
import math

from flask import Flask, request, redirect
from flask import render_template
from app.log.log import Log
from app.database.DatabaseConnection import DatabaseConnection


def create_app(test_config=None):
    # create and configure the app
    app: Flask = Flask(__name__, instance_relative_config=True)

    database = DatabaseConnection()

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
    def status():
        return 'up!'

    @app.route('/')
    def dashboard():

        return render_template('dashboard.html',
                               data={
                                   'title': 'Dashboard',

                               })

    @app.route('/cpu-count')
    def cpu_count_route():
        hardware_data = database.select_all_hardware()

        hardware_cpu_count = list(filter(lambda k: 'CPU count' in k[6], hardware_data))

        cpu_count_chart_data = generate_chart_data(hardware_cpu_count)

        return generate_page(filtered_data=hardware_cpu_count, in_gb=False,
                             title='CPU count')

    @app.route('/cpu-utilization')
    def cpu_utilization_route():
        hardware_data = database.select_all_hardware()

        hardware_cpu_utilization = list(filter(lambda k: 'CPU utilization' in k[6], hardware_data))

        return generate_page(filtered_data=hardware_cpu_utilization, in_gb=False,
                             title='CPU utilization')

    @app.route('/ram-available')
    def ram_available_route():
        hardware_data = database.select_all_hardware()

        hardware_ram_available = list(filter(lambda k: 'RAM available' in k[6], hardware_data))

        return generate_page(filtered_data=hardware_ram_available, in_gb=True,
                             title='RAM available')

    @app.route('/ram-used-percent')
    def ram_used_percent_route():
        hardware_data = database.select_all_hardware()
        hardware_ram_used_percent = list(filter(lambda k: 'RAM used (percent)' in k[6], hardware_data))

        return generate_page(filtered_data=hardware_ram_used_percent, in_gb=False,
                             title='RAM used (percent)')

    @app.route('/ram-used-absolute')
    def ram_used_abs_route():
        hardware_data = database.select_all_hardware()

        hardware_ram_used_absolute = list(filter(lambda k: 'RAM used (absolute)' in k[6], hardware_data))

        return generate_page(filtered_data=hardware_ram_used_absolute, in_gb=True,
                             title='RAM used (absolute)')

    @app.route('/free-disk-space')
    def free_disk_space_route():
        hardware_data = database.select_all_hardware()

        hardware_free_disk_space = list(filter(lambda k: 'Free disk space' in k[6], hardware_data))

        return generate_page(filtered_data=hardware_free_disk_space, in_gb=True,
                             title='Free disk space')

    @app.route('/used-disk-space-percent')
    def used_disk_space_percent_route():
        hardware_data = database.select_all_hardware()

        hardware_used_disk_space_percent = list(filter(lambda k: 'Used disk space (percent)' in k[6], hardware_data))

        return generate_page(filtered_data=hardware_used_disk_space_percent, in_gb=False,
                             title='Used disk space (percent)')

    @app.route('/limits')
    def limits_route():

        cpu_limits = database.select_current_threshold(threshold='cpu')
        ram_limits = database.select_current_threshold(threshold='ram')

        cpu_soft_limit_db = cpu_limits[0][1]
        cpu_hard_limit_db = cpu_limits[1][1]
        ram_soft_limit_db = ram_limits[0][1]
        ram_hard_limit_db = ram_limits[1][1]

        return render_template(
            'limits.html',
            data={
                'title': 'Limits',
                'db': {
                    'cpu': {
                        'soft': cpu_soft_limit_db,
                        'hard': cpu_hard_limit_db
                    },
                    'ram': {
                        'soft': ram_soft_limit_db,
                        'hard': ram_hard_limit_db
                    }
                }
            }
        )

    @app.route('/update-limit', methods=['POST'])
    def update_limits_route():
        print('Updating limits')
        if request.form.get('cpu_soft_limit'):
            database.update_threshold(
                threshold=request.form.get('cpu_soft_limit'),
                limit_type=1,
                hardware_type=2
            )
        if request.form.get('ram_soft_limit'):
            database.update_threshold(
                threshold=request.form.get('ram_soft_limit'),
                limit_type=1,
                hardware_type=4
            )
        if request.form.get('cpu_hard_limit'):
            database.update_threshold(
                threshold=request.form.get('cpu_hard_limit'),
                limit_type=2,
                hardware_type=2
            )
        if request.form.get('ram_hard_limit'):
            database.update_threshold(
                threshold=request.form.get('ram_hard_limit'),
                limit_type=2,
                hardware_type=4
            )

        return redirect('/limits')

    from app.log import show_log
    app.register_blueprint(show_log.bp)

    Log.write('Server started')

    return app


def generate_page(filtered_data, title, in_gb: bool = False):
    x, y = generate_chart_data(filtered_data, in_gb)

    return render_template('history.html',
                           data={
                               'title': title,
                               'labels': x,
                               'history': [
                                   {
                                       'data': y,
                                       'label': 'Used disk space (percent)',
                                       'fill': False,
                                       'borderColor': "#3e95cd",
                                   },
                               ]
                           })


def generate_chart_data(raw_data_list, in_gb: bool = False):
    kb = float(1024)
    gb = float(kb ** 3)
    x = []
    y = []

    for data in raw_data_list:
        if in_gb:
            _y = data[1] / gb
            x.append(data[4])
            y.append(_y)
        else:
            x.append(data[4])
            y.append(data[1])

    return x, y
