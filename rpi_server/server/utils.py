from demo_lcd import lcd
from pusher import pusher

def process_data(data):
    # Process the data and return the result
    return data

def process_payment(data):
    # Process the data and return the result
    if data["value"] >= 10:
        lcd("Success Payment")
        pusher()
        return "Payment Success!"
    else:
        return "Payment Fail!"