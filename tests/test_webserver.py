import unittest

import mysql

import app.webserver.server
from unittest.mock import MagicMock

from app.database.DatabaseConnection import DatabaseConnection
from app.log.log import Log


class TestWebserverCase(unittest.TestCase):
    def test_server(self):
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
            Log.write = MagicMock()

            with app.webserver.server.create_app().test_client() as client:
                up_page = client.get('/status')
                html = up_page.data.decode()
                self.assertEqual(200, up_page.status_code)
                assert 'up!' in html


if __name__ == '__main__':
    unittest.main()
