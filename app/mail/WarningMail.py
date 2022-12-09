import smtplib
import configparser


class WarningMail:
    @staticmethod
    def send_mail(log, email):
        config = configparser.ConfigParser()
        config.read('config.ini')
        port = 587  # For starttls
        smtp_server = config['sendermail']['smtp']
        sender_email = config['sendermail']['email']
        password = config['sendermail']['password']
        message = open('mail.txt', 'r').read().replace('$LOG', log)
        message = '\n' + message
        server = smtplib.SMTP(host=smtp_server, port=port)
        server.ehlo()
        server.starttls()
        server.login(sender_email, password)
        server.ehlo()
        header = 'To:' + email + '\n' + 'From: ' + sender_email + '\n' + 'Subject:WARNING \n ' \
                                                                         '\nContent-Type: text/plain; charset=UTF-8 \n'
        msg = header + message

        server.sendmail(from_addr=sender_email, to_addrs=email, msg=msg)
        server.quit()
