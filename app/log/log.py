class Log:
    def write(self, log_entry):
        file = open('logs/log.log', 'a')
        file.write(log_entry + '\n')
        return file

    def read(self):
        file = open('logs/log.log', 'r')

        return file.read()
