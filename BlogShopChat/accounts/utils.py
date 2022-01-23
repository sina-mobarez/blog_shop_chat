from twilio.rest import Client

account = "AC832497b0d13f0ff44306452381568ba6"
token = "3ebb0c303ea464916605d5eed02da664"
client = Client(account, token)

def send_sms(receptor, token):
    client.messages.create(to=f"+98{receptor}", from_="+16203180991", body=f"your otp is: {token}")    
    
    