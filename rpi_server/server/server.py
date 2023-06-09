from flask import Flask, request
from utils import process_data, process_payment
from demo_lcd import lcd
from pusher import pusher
import time

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        # Access the request data
        data = request.get_json()
        
        # Process the data
        result = process_data(data)
        
        # Prepare the response
        response = {'result': result}
        
        # Return the response
        return response
    
@app.route('/payment', methods=['POST'])
def payment():
    if request.method == 'POST':
        # Access the request data
        data = request.get_json()
        
        # Process the data
        if(data["work"]):
            lcd("Success Payment")
            pusher()
        else:
            lcd("Fail Payment")
        
        time.sleep(3)

        lcd("Pay 5Mi to buy!")
        
        # Return the response
        return

# run "python3 server.py" to start development server
# run "gunicorn server:app" to start production depployment server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)