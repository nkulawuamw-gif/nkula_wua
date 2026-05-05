import requests
from django.conf import settings


class SMSService:
    def __init__(self, user_profile):
        self.profile = user_profile
        self.provider = user_profile.sms_provider
        self.api_key = user_profile.sms_api_key
        self.api_secret = user_profile.sms_api_secret
        self.sender_id = user_profile.sms_sender_id
    
    def send_sms(self, phone_number, message):
        if self.provider == "none":
            return {"status": "success", "message": "SMS sent (Demo Mode)", "simulated": True}
        
        if self.provider == "twilio":
            return self._send_twilio(phone_number, message)
        elif self.provider == "africastalking":
            return self._send_africastalking(phone_number, message)
        elif self.provider == "bulksms":
            return self._send_bulksms(phone_number, message)
        elif self.provider == "msg91":
            return self._send_msg91(phone_number, message)
        else:
            return {"status": "error", "message": "Invalid SMS provider"}
    
    def _send_twilio(self, phone_number, message):
        try:
            account_sid = self.api_key
            auth_token = self.api_secret
            from_number = self.sender_id
            
            url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
            data = {
                "To": phone_number,
                "From_": from_number,
                "Body": message
            }
            response = requests.post(url, data=data, auth=(account_sid, auth_token))
            
            if response.status_code == 201:
                return {"status": "success", "message": "SMS sent successfully"}
            else:
                return {"status": "error", "message": response.json().get("message", "Failed to send SMS")}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _send_africastalking(self, phone_number, message):
        try:
            api_key = self.api_key
            username = self.api_secret
            from_number = self.sender_id
            
            url = "https://api.africastalking.com/version1/messaging"
            headers = {"apiKey": api_key, "Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "username": username,
                "to": phone_number,
                "message": message,
                "from": from_number
            }
            response = requests.post(url, headers=headers, data=data)
            result = response.json()
            
            if "SMSMessageData" in result and "Recipients" in result["SMSMessageData"]:
                return {"status": "success", "message": "SMS sent successfully"}
            return {"status": "error", "message": "Failed to send SMS"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _send_bulksms(self, phone_number, message):
        try:
            url = "https://api.bulksms.com/v1/sms"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            data = {
                "from": self.sender_id,
                "to": phone_number,
                "body": message
            }
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code in [200, 201]:
                return {"status": "success", "message": "SMS sent successfully"}
            return {"status": "error", "message": "Failed to send SMS"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _send_msg91(self, phone_number, message):
        try:
            authkey = self.api_key
            country = "91"
            route = "4"
            sender = self.sender_id
            
            url = "https://api.msg91.com/api/v5/flow/"
            headers = {
                "authkey": authkey,
                "Content-Type": "application/json"
            }
            payload = {
                "mobiles": phone_number.replace("+", ""),
                "message": message,
                "sender": sender,
                "country": country,
                "route": route
            }
            response = requests.post(url, json=payload, headers=headers)
            result = response.json()
            
            if result.get("type") == "success":
                return {"status": "success", "message": "SMS sent successfully"}
            return {"status": "error", "message": "Failed to send SMS"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


def send_sms_to_client(user_profile, phone_number, message):
    service = SMSService(user_profile)
    return service.send_sms(phone_number, message)
