from kavenegar import *
from twilio.rest import Client

# use kavenegar ---------------------

def send_sms(receptor, token):
    try:
        api = KavenegarAPI('31657945324630726553504B7432556C31726A544336536B586B7A507254723773576F4C366356543270553D')
        params = {
            'sender': '10008663',#optional
            'receptor': f'0{receptor}',#multiple mobile number, split by comma
            'message': f'your otp code : {token}',
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)  
    
    

# use twilio ---------------------------

# account = "AC832497b0d13f0ff44306452381568ba6"
# token = "3ebb0c303ea464916605d5eed02da664"
# client = Client(account, token)

# def send_sms(receptor, token):
#     client.messages.create(to=f"+98{receptor}", from_="+16203180991", body=f"your otp is: {token}")    
    
