import requests
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import json
from django.urls import reverse



start_payment_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


class StartPaymentView():
    def get(self, *args, **kwargs):
        data = {
            "merchant_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "amount": 1000000,
            "callback_url": "http://127.0.0.1:8000/payment_result/",
            "description": "This is a test .",
            "metadata": {"mobile": "09309195958", "email": "info.test@gmail.com"}

        }
        start_payment_request = requests.post(url=start_payment_url, headers=headers, json=data)

        if start_payment_request.status_code == 200:
            response = json.loads(start_payment_request.text)
            data = response["data"]
            authority = data["authority"]
            payment_url = f"https://sandbox.zarinpal.com/pg/StartPay/{authority}/"
            return HttpResponseRedirect(redirect_to=payment_url)


class VerifyPaymentView():
    def get(self, *args, **kwargs):
        path = self.request.get_full_path()
        querystring = path.split(sep="/?Authority=")[1]
        authority = querystring.split(sep="&")[0]
        status = querystring.split(sep="&Status=")[1]

        if status == "OK":
            verify_payment_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
            data = {
                "merchant_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "amount": 1000000,
                "authority": authority

            }

            verify_payment_request = requests.post(url=verify_payment_url, headers=headers, json=data)
            code = verify_payment_request.json()["data"].get("code")

            if code == 100:
                response = verify_payment_request.json()["data"]
                ref_id = response["ref_id"]
                message = f"پرداخت موفق : {ref_id}"
                self.request.session["message"] = message
                return redirect(to=reverse(viewname="blog:home"))

            else:
                message = "پرداخت نا موفق بوده است !"
                self.request.session["message"] = message
                return redirect(to=reverse(viewname="blog:home"))

        elif status == "NOK":
            message = "پرداخت نا موفق بوده است !"
            self.request.session["message"] = message
            return redirect(to=reverse(viewname="blog:home"))

