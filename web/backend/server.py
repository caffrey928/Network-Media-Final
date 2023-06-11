from flask import Flask, request
from flask_cors import CORS
from IOTA_crawler.main import IOTA_crawler

app = Flask(__name__)
CORS(app)

balance = 0

@app.route('/')
def hello():
    return 'Hello, World!'
    
@app.route('/payment', methods=['GET'])
def payment():
    global balance
    if request.method == 'GET':
        # Crawl payment data
        print("Crawling...")
        crawler = IOTA_crawler()
        result = crawler.start()
        print("Crawled!")

        if result["balance"] == "0":
            new_balance = 0.0
        else:
            new_balance = float(result["balance"][:-3])
        payment = new_balance - balance
        balance = new_balance

        # Check the payment
        if(payment <= 0):
            response = "Fail Payment!"
        elif(payment < 5):
            response = "No enough money!"
        else:
            response = "Success Payment!"

        # Return the response
        return response

# run "python3 server.py" to start development server
# run "gunicorn server:app" to start production depployment server
if __name__ == '__main__':
    crawler = IOTA_crawler()
    result = crawler.start()
    if result["balance"] == "0":
        balance = 0.0
    else:
        balance = float(result["balance"][:-3])
    app.run(host='0.0.0.0', port=8000, debug=True)