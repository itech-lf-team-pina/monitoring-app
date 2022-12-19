import time

from app.alarm import Alarm
from app.database.DatabaseConnection import DatabaseConnection
from app.hardware.monitor import HardwareMonitor
from app.mail.WarningMail import WarningMail


def start_alarm():
    database = DatabaseConnection()
    mail = WarningMail()
    hardware = HardwareMonitor()

    alarm = Alarm(db=database, hardware=hardware, mail=mail)

    while True:
        alarm.check_thresholds()
        time.sleep(60)
