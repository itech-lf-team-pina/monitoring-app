import time


class Log:
    logfile = 'logs/application.log'

    @staticmethod
    def write(log_entry):
        t = time.localtime()
        current_time = time.strftime("%d.%m.%Y, %H:%M:%S", t)
        file = open(Log.logfile, 'a')
        file.write(f'[{current_time}] ' + log_entry + '\n')
        return file

    @staticmethod
    def read():
        file = open(Log.logfile, 'r')

        return file.read()
