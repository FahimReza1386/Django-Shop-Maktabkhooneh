import requests
import json

class ZarinPalSandBox:

    _payment_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    _callback_url = "https://www.redreseller.com/verify"


    def __init__(self, merchant_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"):
        self.merchant_id = merchant_id

    def payment_request(self, amount):

        payload ={
            "merchant_id": self.merchant_id,
            "amount": amount,
            "callback_url": "http://127.0.0.1:8000/",
            "description": "This is a test .",
            "metadata": {"mobile": "09309195958", "email": "info.test@gmail.com"}
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"      
        }

        start_payment_request = requests.post(url=self._payment_request_url, headers=headers, json=payload)
    
        return start_payment_request


    def payment_verify(self, amount, authority):
        
        payload = {
            "MerchantID": self.merchant_id,
            "Amount": amount,
            "Authority": authority,
        }
        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json',
        }

        response = requests.post(self._payment_verify_url, headers=headers, data=json.dumps(payload))
        return response.json()

    def generate_payment_url(self, authority):

        return f"{self._payment_page_url}{authority}" 



if __name__ == "__main__":
    zarinpal= ZarinPalSandBox()
    response = zarinpal.payment_request(140000)
    tt = response.json()
    data = tt["data"]
    authority = data["authority"]
    print(authority)
  