import os
import threading

from hardware.monitor import HardwareMonitor
from log.log import Log
from webserver.server import create_app
from database.DatabaseConnection import DatabaseConnection


class Main:
    os.environ.setdefault('PORT', '5000')

    test = threading.Thread(target=lambda: create_app().run(debug=False, host='0.0.0.0', port=os.environ.get('PORT')),
                            name='Webserver').start()
    Log.write('Monitoring started')
    database = DatabaseConnection()

    hardware_log = threading.Thread(target=lambda: HardwareMonitor().write_periodic_logs(),
                                    name='HardwareLogWriter').start()
    hardware_database_log = threading.Thread(
        target=lambda: HardwareMonitor().write_periodic_logs_in_db(DatabaseConnection()),
        name='HardwareDatabaseLogWriter').start()


if __name__ == "__main__":
    Main()
