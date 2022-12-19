import os
import threading

import app.alarm.start_alarm
from hardware.monitor import HardwareMonitor
from log.log import Log
from webserver.server import create_app
from database.DatabaseConnection import DatabaseConnection


class Main:
    Log.write('Monitoring started')
    os.environ.setdefault('PORT', '5000')
    webserver_thread = threading.Thread(
        target=lambda: create_app().run(debug=False, host='0.0.0.0', port=os.environ.get('PORT')),
        name='Webserver').start()

    hardware_database_log_thread = threading.Thread(
        target=lambda: HardwareMonitor().write_periodic_logs_in_db(DatabaseConnection()),
        name='HardwareDatabaseLogWriter').start()

    alarm_thread = threading.Thread(
        target=lambda: app.alarm.start_alarm.start_alarm(),
        name='TestAlarm'
    ).start()

    hardware_log_thread = threading.Thread(
        target=lambda: HardwareMonitor().write_periodic_logs(),
        name='HardwareLogWriter'
    ).start()


if __name__ == "__main__":
    Main()
