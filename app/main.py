import os
import threading
import time

from hardware.monitor import HardwareMonitor
from log.log import Log
from webserver.server import create_app
from database.DatabaseConnection import DatabaseConnection
from alarm import Alarm
from mail.WarningMail import WarningMail


def start_alarm():
    database = DatabaseConnection()
    mail = WarningMail()
    hardware = HardwareMonitor()

    alarm = Alarm(db=database, hardware=hardware, mail=mail)

    while True:
        alarm.check_thresholds()
        time.sleep(5)


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
        target=start_alarm(),
        name='AlarmThread'
    )

    hardware_log_thread = threading.Thread(
        target=lambda: HardwareMonitor().write_periodic_logs(),
        name='HardwareLogWriter'
    ).start()


if __name__ == "__main__":
    Main()
