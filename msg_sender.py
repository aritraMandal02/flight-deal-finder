from twilio.rest import Client
from auth import twilio_ph_no, my_ph_no


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
