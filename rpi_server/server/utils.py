from demo_lcd import lcd

def process_data(data):
    # Process the data and return the result
    # Replace this with your own logic
    return data

def process_payment(data):
    # Process the data and return the result
    if data["value"] >= 10:
        lcd()
        return "Payment Success!"
    else:
        return "Payment Fail!"