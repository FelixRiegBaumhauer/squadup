
# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest.ip_messaging import TwilioIpMessagingClient

# Your Account Sid and Auth Token from twilio.com/user/account
account = "AC5ab857de1d62b39b0f89b33f9131321b"
token = "3dd51b71379b851c2930de472f9e9b35"
client = TwilioIpMessagingClient(account, token)

for service in client.services.list():
    print(service.sid)
