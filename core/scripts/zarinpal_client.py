import requests
import json


class ZarinPalSandBox:

    _payment_request_url = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    _callback_url = "https://www.redreseller.com/verify"


    def __init__(self, merchant_id):
        self.merchant_id = merchant_id
    

    def payment_request(self, amount):

        payload ={
            "merchant_id": self.merchant_id,
            "amount": amount,
            "callback_url": self._callback_url,
            "description":"test",
        }
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(self._payment_request_url, headers=headers, data=json.dumps(payload))

        return response.json()


    def payment_verify(self, amount, authority):
        
        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": authority
        }
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(self._payment_verify_url, headers=headers, data=json.dumps(payload))
        return response.json()

    def generate_payment_url(self, authority):
        
        return self._payment_page_url + authority 
    

if __name__ == "__main__":
    zarinpal = ZarinPalSandBox(merchant_id="4ced0a1e-4ad8-4309-9668-3ea3ae8e8897")
    response = zarinpal.payment_request(amount=200000)
    print(response)
    input("procced to generating payment url ")
    print(zarinpal.generate_payment_url(response["Authority"]))

    input("check the payment?")

    response= zarinpal.payment_verify(200000,response["Authority"])
    print(response)