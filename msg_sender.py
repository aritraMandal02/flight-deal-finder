from twilio.rest import Client
import smtplib
from auth import twilio_ph_no, my_ph_no, my_email, password



class MailMan(Client):
    def __init__(self, account_sid, auth_token):
        super().__init__(account_sid, auth_token)

    def send_sms(self, body: str):
        message = self.messages.create(
            body=body,
            from_=twilio_ph_no,
            to=my_ph_no,
        )
        print(message.status)
    
    def send_email(self, body: str, addr: str):
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=addr,
                                msg=f'{body}')
