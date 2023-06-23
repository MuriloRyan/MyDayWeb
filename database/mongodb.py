from hashlib import sha3_512
from database.attempts import addAttemp
from database.userconfig import User
import pymongo
import os

# URL TO CONNECT
url = os.getenv('MONGO_URL')

# Connect to the database
Cluster = pymongo.MongoClient(url)
database = Cluster.get_database('MydayDb')
db = database.get_collection('users')

def signIn(data):

    userTest = db.find_one({
        'username': data['username'],
        'email': data['email'],
        'password': data['password']
        })
    
    if userTest:
        return None #incorrect request
    else:
        db.insert_one(data)
        return 200 #ok request

def logIn(data):
    userAtempt = db.find_one({'email': data['email'], 'password': data['password']})

    if userAtempt:
        return addAttemp(data)
    
    return None


def findIn(data,user):
    userTest = db.find_one({'email': user})

    if userTest:
        testReturn = {}
        for key in data:
            testReturn[key] = userTest.get(key)
        return testReturn
    else:
        return None

def addTask(user, taskdata):
    # taskdata = {'taskname', 'comment'}

    userTest = db.find_one({'email': user['email']})

    if userTest:
        db.update_one({'_id': userTest['_id']}, {'$push': {'tasks': taskdata}})
        return 200
    else:
        return None

def getTask(user):

    userTest = db.find_one({'email': user['email']})

    if userTest:
        return userTest['tasks']
    else:
        return None

def killTask(user, taskname):
    userTest = db.find_one({'email': user['email']})

    if userTest:
        tasks = userTest['tasks']
        taskIndex = None
        for index, task in enumerate(tasks):
            if task['taskname'] == taskname:
                taskIndex = index
                break

        if taskIndex is not None:
            tasks.pop(taskIndex)  # Remove a tarefa da lista
            db.update_one({'_id': userTest['_id']}, {'$set': {'tasks': tasks}})
            
            return True

    return None
