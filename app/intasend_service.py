import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class IntaSendService:
    def __init__(self):
        self.public_key = os.getenv("INTASEND_PUBLIC_KEY")
        self.private_key = os.getenv("INTASEND_PRIVATE_KEY")
        self.base_url = "https://sandbox.intasend.com/api/v1"  # Use live URL for production
        self.headers = {
            "Content-Type": "application/json",
            "X-Public-Key": self.public_key,
            "X-Private-Key": self.private_key,
        }

    def initiate_mpesa_payment(self, phone_number: str, amount: float, transaction_id: str):
        """
        Initiates an MPESA payment using IntaSend API.
        """
        url = f"{self.base_url}/mpesa-stk/push"
        payload = {
            "phone_number": phone_number,
            "amount": amount,
            "currency": "KES",
            "txn_id": transaction_id,
            "callback_url": "https://yourdomain.com/api/payment/callback",
        }

        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response_data = response.json()

            if response.status_code == 200 and response_data.get("status") == "success":
                return response_data
            return {"error": response_data}
        except requests.RequestException as e:
            return {"error": str(e)}

    def check_payment_status(self, transaction_id: str):
        """
        Checks the payment status using IntaSend API.
        """
        url = f"{self.base_url}/transactions/{transaction_id}/"

        try:
            response = requests.get(url, headers=self.headers)
            response_data = response.json()

            if response.status_code == 200:
                return response_data
            return {"error": response_data}
        except requests.RequestException as e:
            return {"error": str(e)}

    def process_payment_callback(self, data: dict):
        """
        Handles the payment callback from IntaSend.
        """
        transaction_id = data.get("txn_id")
        status = data.get("status")

        # Example: Update the transaction status in the database
        # update_transaction_status(transaction_id, status)

        return {
            "message": "Payment status updated",
            "transaction_id": transaction_id,
            "status": status,
        }
