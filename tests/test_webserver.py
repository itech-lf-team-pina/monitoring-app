import unittest
import app.webserver.server


class TestWebserverCase(unittest.TestCase):
    def test_server(self):
        with app.webserver.server.create_app().test_client() as client:
            up_page = client.get('/status')
            html = up_page.data.decode()
            self.assertEqual(200, up_page.status_code)
            assert 'up!' in html



if __name__ == '__main__':
    unittest.main()
