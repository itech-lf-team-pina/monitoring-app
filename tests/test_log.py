import unittest
from app.log.log import Log


class LogTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.log = Log()

    def test_if_log_writes(self):
        self.assertIn()


if __name__ == '__main__':
    unittest.main()
