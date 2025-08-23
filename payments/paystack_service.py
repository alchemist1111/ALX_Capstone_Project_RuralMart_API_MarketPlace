from paystackapi.paystack import Paystack
from django.conf import settings

# Initialize Paystack API with the secret key
paystack_api = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)

# Verify payment
def verify_payment(transaction_reference):
    try:
        # Call Paystack to verify the payment status
        verification = paystack_api.transaction.verify(transaction_reference)
        return verification
    except Paystack.exceptions.PaystackError as e:
        return {"error": str(e)}


# Initialize payment
def initialize_payment(email, amount, order_id):
    try:
        # Call Paystack to create a payment
        payment = paystack_api.transaction.initialize(
            email=email,
            amount=amount * 100,
            order_id=order_id
        )
        return payment
    except Paystack.exceptions.PaystackError as e:
        return {"error": str(e)}        