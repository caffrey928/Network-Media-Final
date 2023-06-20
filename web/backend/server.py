from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import ast
import requests
import multiprocessing

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

from IOTA_crawler.main import IOTA_crawler
from utils import uint8array_from_dict

app = Flask(__name__)
CORS(app)

base_url = 'http://172.20.10.4:8000'
balance = 0
Users = []

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/payment/', methods=['GET'])
def payment():
    global balance
    if request.method == 'GET':
        # Crawl payment data
        print("Crawling...")
        result = crawler.get_balance()
        print("Crawled!")

        if(result["status"]):
            new_balance = result["balance"]
            payment = new_balance - balance
            balance = new_balance
        else:
            payment = 0
        
        # Check the payment
        work = False
        if(payment <= 0):
            response = { 'data': "Failed Payment!" }
        elif(payment < 5):
            response = { 'data': "No enough money!" }
        else:
            work = True
            response = { 'data': "Success Payment!" }
        
        try:
            p = multiprocessing.Pool(processes = 1)
            p.apply_async(requests.post, args=[f'{base_url}/payment'], kwds={'json': {"work": work}})
            p.close()
        except Exception as e:
            print(e)
            print("Fail to send request to rpi_server!")
        
        

        # Return the response
        return response

@app.route('/payment/<string:name>', methods=['GET'])
def member_payment(name):
    global balance
    if request.method == 'GET':
        # Crawl payment data
        print("Crawling...")
        result = crawler.get_balance()
        print("Crawled!")

        # Find user data based on name
        user = next(filter(lambda x: x['name'] == name, Users), None)
        money = user['money']
        payment = 0

        if(result["status"]):
            new_balance = result["balance"]
            payment = new_balance - balance
            balance = new_balance
        else:
            payment = 0

        # Calculate the total money for the member
        total = money + payment
        
        # Check the payment
        work = False
        if(total < 5):
            user['money'] = total
            with open("Users.txt", "w") as f:
                f.write(str(Users))
            response = { 'data': f"No enough money!", "money": str(user['money']) }
        else:
            work = True
            total -= 5
            user['money'] = total
            with open("Users.txt", "w") as f:
                f.write(str(Users))
            response = { 'data': "Success Payment!", "money": str(user['money']) }
        
        try:
            p = multiprocessing.Pool(processes = 1)
            p.apply_async(requests.post, args=[f'{base_url}/payment'], kwds={'json': {"work": work}})
            p.close()
        except Exception as e:
            print(e)
            print("Fail to send request to rpi_server!")

        # Return the response
        return response

@app.route('/UserDB/<string:name>', methods=['GET', 'POST'])
def User(name):
    if request.method == 'GET':
        user = next(filter(lambda x: x['name'] == name, Users), None)
        if user:
            res = jsonify({'User': user})
            return res, 200
        else:
            res = jsonify({'message': 'User not found'})
            return res, 404
    elif request.method == 'POST':
        if next(filter(lambda x: x['name'] == name, Users), None):
            return jsonify({'message': f'An user with name {name} already exists ..'}), 403
        
        data = request.get_json()
        User = {'name': name, 'id': data['id'], 'publicKey': data['publicKey'], 'money': data['money']}
        Users.append(User)
        with open("Users.txt", "w") as f:
            f.write(str(Users))
        print("User Added!")

        res = jsonify(User)
        
        return res, 201


@app.route('/UserDB/', methods=['GET'])
def UsersList():
    print("Getting Users List...")
    res = jsonify({'Users': Users})

    return res


@app.route('/Auth/<string:name>', methods=['POST'])
def AuthUser(name):
    user = next(filter(lambda x: x['name'] == name, Users), None)
    # print(user)
    publickey = user['publicKey']
    curve = ec.SECP256R1()

    data = request.get_json()
    # print(data)
    clientData = uint8array_from_dict(data['clientData'])
    authData = uint8array_from_dict(data['authData'])
    signature = uint8array_from_dict(data['signature'])

    # check signature
    try:
        hash_method = hashes.SHA256()
        digest = hashes.Hash(hash_method)
        digest.update(clientData)
        concat_data = authData + digest.finalize()

        if publickey['-1'] != 1:
            print("Unsupported elliptic curve")
            return { 'status': False, 'data': 0 }, 201

        ec.EllipticCurvePublicNumbers(
            int.from_bytes(uint8array_from_dict(publickey['-2']), byteorder="big"), 
            int.from_bytes(uint8array_from_dict(publickey['-3']), byteorder="big"), 
            curve
        ).public_key().verify(
            signature, concat_data, ec.ECDSA(hash_method)
        )

        return { 'status': True, 'data': str(user['money']) }, 201

    except InvalidSignature:
        print("Sinature Fail!")
        return { 'status': False, 'data': 0 }, 201

    except Exception as e:
        print(e)
        return { 'status': False, 'data': 0 }, 201

# run "python3 server.py" to start development server
# run "gunicorn server:app" to start production depployment server
if __name__ == '__main__':
    # initial crawl to set initial balance
    print("Start first crawling...")
    crawler = IOTA_crawler()
    result = crawler.get_balance()
    if(result["status"]):
        balance = result["balance"]
    
    # read or initial Users list
    if(os.path.exists("Users.txt")):
        with open("Users.txt", "r") as f:
            Users = ast.literal_eval(f.read())
    else:
        with open("Users.txt", "w") as f:
            f.write(str(Users))
    print("User Count: " + str(len(Users)))

    app.run(host='0.0.0.0', port=8000, debug=True)