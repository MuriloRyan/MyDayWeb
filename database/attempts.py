from hashlib import sha3_512
import requests
import pymongo
import socket
from dotenv import load_dotenv
import os

load_dotenv()
# URL TO CONNECT
url = os.getenv('MONGO_URL')

# Connect to the database
Cluster = pymongo.MongoClient(url)
database = Cluster.get_database('MydayDb')
db = database.get_collection('users')

def addAttemp(credentials):
    response = requests.get('https://api.ipify.org?format=json')
    publicIp = response.json()['ip']
    localIp = socket.gethostbyname(socket.gethostname())

    db = database.get_collection('users')
    userAtempt = db.find_one({'email': credentials['email'], 'password': credentials['password']})

    if userAtempt:
        if userAtempt['password'] == credentials['password']:
            attemptsDATA = {
                "publicIP": publicIp,
                "localIP": localIp,
                "strikes": userAtempt.get('strikes', 0),
                "LogInData": {
                    "email": credentials['email'],
                    "password": credentials['password']
                }
            }

            existingIP = {"publicIP": publicIp, "localIP": localIp}
            
            db = database.get_collection('attempts')
            existingattempts = db.find_one(existingIP)

            if existingattempts:
                attemptsDATA['strikes'] = existingattempts['strikes']
            else:
                db.insert_one(attemptsDATA)

            sessionHash = sha3_512(f'{publicIp}{localIp}'.encode()).hexdigest()
            db.delete_one({ 'publicIP': attemptsDATA['publicIP'],
                            'localIP': attemptsDATA['localIP']})
            return sessionHash

    return None