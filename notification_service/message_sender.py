#!/usr/bin/env python
# Install the Python helper library from twilio.com/docs/python/install
import os

from twilio.rest import Client

# To set up environmental variables, see http://twil.io/secure
account_sid = 'AC393b2d1c8c597e036a1a2093bb512a3e'
auth_token = 'e5016526aed3f146d679ca7454ff05ee'

client = Client(account_sid, auth_token)
# binding = client.notify.services('ISXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') \
#     .bindings.create(
#     # We recommend using a GUID or other anonymized identifier for Identity
#     identity='00000001',
#     binding_type='sms',
#     address='+918717892888')
# print(binding.sid)

service = client.notify.v1.services.create()
print(service.sid)
def send_sms(text):
    account_sid = 'AC393b2d1c8c597e036a1a2093bb512a3e'
    auth_token = 'e5016526aed3f146d679ca7454ff05ee'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+18633339292',
        body=text,
        to='+918717892888'
    )

    print(message.sid)

# send_sms("Hello")