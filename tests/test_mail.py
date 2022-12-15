import unittest
from smtplib import SMTP

from app.mail.WarningMail import WarningMail
from unittest.mock import MagicMock


class TestMailCase(unittest.TestCase):
    def test_connection(self):
        WarningMail.send_mail = MagicMock()

        mail = WarningMail()
        mail.send_mail('', '')

        WarningMail.send_mail.assert_called()


if __name__ == '__main__':
    unittest.main()
