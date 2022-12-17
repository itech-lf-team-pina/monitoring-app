import configparser
import time

from app.log.log import Log
from app.mail.WarningMail import WarningMail
from app.hardware.monitor import HardwareMonitor
from app.database.DatabaseConnection import DatabaseConnection


class Alarm:
    _db: DatabaseConnection = None
    _hardware: HardwareMonitor = None
    _mail: WarningMail = None
    _config = configparser.ConfigParser()
    _config.read('config.ini')
    receiver_mail = _config['receivemail']['email']

    def __init__(self, db: DatabaseConnection, hardware: HardwareMonitor, mail: WarningMail):
        self._db = db
        self._hardware = hardware
        self._mail = mail
        Log.write('Alarm Monitoring started')

    def check_thresholds(self):
        Log.write('Check thresholds')
        # always get current thresholds for ram and cpu
        threshold_ram_soft_percent, threshold_ram_hard = self._db.select_current_threshold(threshold='ram')
        threshold_cpu_soft_percent, threshold_cpu_hard = self._db.select_current_threshold(threshold='cpu')
        current_ram = self._hardware.get_ram()[2]
        current_cpu = self._hardware.get_cpu_percent()

        print('CPU')
        print(threshold_cpu_soft_percent, threshold_cpu_hard)
        print('RAM')
        print(threshold_ram_soft_percent, threshold_ram_hard)

        threshold_cpu_soft_value = threshold_cpu_hard[1] * threshold_cpu_soft_percent[1]
        threshold_ram_soft_value = threshold_ram_hard[1] * threshold_ram_soft_percent[1]

        # only important for render.com Logging
        print('Alarm class check started')
        print(current_cpu)
        print(current_ram)

        # check cpu
        if current_cpu > threshold_cpu_soft_value:
            if current_cpu >= threshold_cpu_hard:
                log_message = f'Current CPU utilization reached your hard limit! \n Current value: {str(current_cpu)}'
                self.trigger_mail(
                    message=log_message)
                self._db.insert_warning_log(value=log_message, is_critical_hardware=True)
            else:
                log_message = f'Current CPU utilization reached your soft limit! \n Current value: {str(current_cpu)}'
                Log.write(log_message)
                self._db.insert_warning_log(value=log_message, is_warning_hardware=True)

        # check ram
        if current_ram > threshold_ram_soft_value:
            if current_ram >= threshold_ram_hard:
                log_message = f'Current used RAM reached your hard limit! \n Current value: {str(current_cpu)}'
                self.trigger_mail(
                    message=log_message)
                self._db.insert_warning_log(value=log_message, is_critical_hardware=True)
            else:
                log_message = f'Current used RAM reached your soft limit! \n Current value: {str(current_cpu)}'
                Log.write(log_message)
                self._db.insert_warning_log(value=log_message, is_warning_hardware=True)

    def trigger_mail(self, message):
        self._mail.send_mail(message, self.receiver_mail)
