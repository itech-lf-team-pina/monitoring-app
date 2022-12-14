import os
import time
import psutil
from app.log.log import Log


class HardwareMonitor:
    def write_periodic_logs(self):
        Log.write('CPU count: ' + str(self.get_cpu_count()))
        while True:
            Log.write('---------------------------------------')
            Log.write('RAM total: ' + str(self.bytes2human(self.get_ram()[0])))
            Log.write('RAM available: ' + str(self.bytes2human(self.get_ram()[1])))
            Log.write('RAM used (percent): ' + str(self.get_ram()[2]) + '%')
            Log.write('RAM used (absolute): ' + str(self.bytes2human(self.get_ram()[3])))
            Log.write('Free disk space: ' + str(self.get_free_disk_space_absolute(prettier=True)))
            Log.write('Used disk space in percent: ' + str(self.get_free_disk_space()) + '% used')
            Log.write('CPU utilization: ' + str(self.get_cpu_percent()) + '%')
            users = self.get_users()
            for index, user in enumerate(users):
                Log.write(f'Current users [{str(index)}]: {str(user[0])}')

            Log.write('---------------------------------------')

            time.sleep(10)

    def write_periodic_logs_in_db(self, db):
        db.insert_hardware_data(1, self.get_cpu_count())
        while True:
            db.insert_hardware_data(3, self.get_ram()[1])
            db.insert_hardware_data(4, self.get_ram()[2])
            db.insert_hardware_data(5, self.get_ram()[3])
            db.insert_hardware_data(6, self.get_free_disk_space_absolute())
            db.insert_hardware_data(7, self.get_free_disk_space())
            db.insert_hardware_data(2, self.get_cpu_percent())

            users = self.get_users()
            for index, user in enumerate(users):
                db.insert_hardware_data(8, user[0])

            time.sleep(10)

    def get_cpu_count(self):

        return psutil.cpu_count()

    def get_cpu_percent(self):
        return psutil.cpu_percent()

    def get_ram(self):
        return psutil.virtual_memory()

    def get_free_disk_space(self):
        disk_space = psutil.disk_usage(os.getcwd())[3]
        return disk_space

    def get_free_disk_space_absolute(self, prettier: bool = False):
        disk_usage = psutil.disk_usage(os.getcwd())[2]
        if prettier:
            return self.bytes2human(disk_usage)
        else:
            return disk_usage

    def get_users(self):
        users = psutil.users()
        return users

    def bytes2human(self, n):
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
        return "%sB" % n
