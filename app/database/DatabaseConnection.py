import mysql.connector as db
import sys
import configparser

from app.log.log import Log


class DatabaseConnection:
    _connection = None
    _cursor = None
    config = configparser.ConfigParser()
    config.read('config.ini')

    def __init__(self):
        try:
            self._connection = db.connect(
                host=self.config['dbconnection']['host'],
                database=self.config['dbconnection']['database'],
                user=self.config['dbconnection']['user'],
                port=self.config['dbconnection']['port'],
                password=self.config['dbconnection']['password']
            )
            Log.write('Connected to database')
            print('Connected to database')
            self._cursor = self._connection.cursor()
        except db.Error as e:
            Log.write(f'Error connecting to MariaDB server: {e}')
            sys.exit(1)

    def insert_hardware_data(self, hardware_type, value):
        try:

            if hardware_type == 8:
                self._cursor.execute('INSERT INTO hardware (value_string, hardware_type) VALUES (%s, %s)',
                                     (value, hardware_type))
                self._connection.commit()
            elif hardware_type:
                self._cursor.execute('INSERT INTO hardware (value_int, hardware_type) VALUES (%s, %s)',
                                     (value, hardware_type))
                self._connection.commit()
            else:
                Log.write('Error while inserting. No hardware type given')
        except db.Error as e:
            Log.write(f'Error while inserting new hardware data: {e}')

    def insert_new_thresholds(self, hardware_type, threshold, limit_type):
        try:
            if hardware_type:
                query = "INSERT INTO threshold (value, hardware_type, limit_type) VALUES (%s, %s, %s)"
                values = (threshold, hardware_type, limit_type)
                self._cursor.execute(query, values)
                self._connection.commit()
            else:
                Log.write('Error while inserting. No hardware type given')
        except db.Error as e:
            Log.write(f'Error while inserting new thresholds: {e}')

    def select_all_hardware(self):
        self._cursor.execute(
            "Select * from hardware h inner join hardware_type ht on h.hardware_type = ht.id")
        records = self._cursor.fetchall()
        return records

    def select_all_thresholds(self):
        query = "Select * from threshold h inner join hardware_type ht on h.hardware_type = " \
                "ht.id inner join limit_type lt on h.limit_type = lt.id"

        self._cursor.execute(query)

        records = self._cursor.fetchall()

        return records

    def select_current_threshold(self, threshold):
        if threshold is None:
            Log.write('Error: no threshold given')
            return 0, 0
        else:
            if threshold == 'ram':
                threshold_name = 4
            else:
                threshold_name = 2

            self._cursor.execute(
                "Select * from threshold h inner join hardware_type ht on h.hardware_type = "
                "ht.id inner join limit_type lt on h.limit_type = lt.id WHERE hardware_type=%s AND limit_type=%s ORDER "
                "BY timestamp ASC LIMIT 1", (threshold_name, 1))
            current_soft_limit = self._cursor.fetchall()
            self._cursor.execute(
                "Select * from threshold h inner join hardware_type ht on h.hardware_type = "
                "ht.id inner join limit_type lt on h.limit_type = lt.id WHERE hardware_type=%s AND limit_type=%s "
                "ORDER BY timestamp DESC LIMIT 1", (threshold_name, 2))
            current_hard_limit = self._cursor.fetchall()

            return current_soft_limit, current_hard_limit
