import unittest

import mysql
import configparser

from app.database.DatabaseConnection import DatabaseConnection
from unittest.mock import MagicMock


class TestDatabaseCase(unittest.TestCase):
    def test_connection(self):
        with unittest.mock.patch.dict(DatabaseConnection.config, {
            'dbconnection':
                {
                    'host': '',
                    'database': '',
                    'user': '',
                    'port': 0,
                    'password': ''
                 }
        }):
            mysql.connector.connect = MagicMock()
            DatabaseConnection()
            mysql.connector.connect.assert_called()


if __name__ == '__main__':
    unittest.main()
