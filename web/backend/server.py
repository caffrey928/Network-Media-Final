from flask import Flask, request
from flask_cors import CORS
import requests
import multiprocessing
from IOTA_crawler.main import IOTA_crawler

app = Flask(__name__)
CORS(app)

base_url = 'http://172.20.10.4:8000'
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

        if(result["status"]):
            new_balance = result["balance"]
            payment = new_balance - balance
            balance = new_balance
        else:
            payment = 0
        
        work = False
        # Check the payment
        if(payment <= 0):
            response = "Fail Payment!"
        elif(payment < 5):
            response = "No enough money!"
        else:
            work = True
            response = "Success Payment!"
        

        p = multiprocessing.Pool(processes = 1)
        p.apply_async(requests.post, args=[f'{base_url}/payment'], kwds={'json': {"work": work}})
        p.close()

        # Return the response
        return response

# run "python3 server.py" to start development server
# run "gunicorn server:app" to start production depployment server
if __name__ == '__main__':
    print("Start first crawling...")
    crawler = IOTA_crawler()
    result = crawler.start()
    if(result["status"]):
        balance = result["balance"]
    app.run(host='0.0.0.0', port=8000, debug=True)