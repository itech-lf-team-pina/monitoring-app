import os
import threading

from hardware.monitor import HardwareMonitor
from log.log import Log
from webserver.server import create_app


class Main:
    os.environ.setdefault('PORT', '5000')

    test = threading.Thread(target=lambda: create_app().run(debug=False, host='0.0.0.0', port=os.environ.get('PORT')),
                            name='Webserver').start()
    Log.write('Monitoring started')
    hardware = HardwareMonitor()

    hardware_log = threading.Thread(target=lambda: HardwareMonitor().write_periodic_logs(),
                                    name='HardwareLogWriter').start()


if __name__ == "__main__":
    Main()
