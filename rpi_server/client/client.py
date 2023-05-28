import requests

# URL of the Flask server
base_url = 'http://localhost:8000'

def send_payment(value, date):
    # Data to send in the request
    data = {'value': value, 'date': date}

    # Send POST request to the Flask server
    response = requests.post(f'{base_url}/payment', json=data)

    # Check the response
    if response.status_code == 200:
        result = response.json()['result']
        print(f'{result}')
    else:
        print('Error occurred while sending the request.')

send_payment(5, "5/28/2023")
send_payment(10, "5/28/2023")
