import os

from flask import Flask, request, jsonify
from task import Task
import pymongo
import redis
import socket
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
app = Flask(__name__)

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["golook"]
mongo_collection = db["data"]
# mongo_collection.drop()

# pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
rr = redis.Redis(host = '127.0.0.1', port = 6379)
rr.flushdb()


@app.route("/tasks", methods=["GET"])
def get_data():
    try:
        rr.ping()
        temp_list = []
        cursor = mongo_collection.find()
        if 'all' not in rr.keys():
            for doc in cursor:
                tempstr = str(doc)
                startindex = tempstr.index("\'name\'")
                endindex = tempstr.index(", 'id'")
                res1 = tempstr[startindex:endindex]
                res2 = tempstr[endindex + 2:len(tempstr) - 1]
                res = "{" + res2.strip() + ", " + res1.strip() + "}"
                temp_list.append(res)
            rr_str = 'result: [ {} ]'.format(','.join(temp_list))
            rr.set('all', rr_str)
            ans = '{\n'
            ans += '    result: {} '.format(','.join(temp_list))
            ans += '\n}'
            # print(rr.get('all'))
            return ans
        else:
            return "redis is working!\n" + "{ \n" + rr.get('all') + "\n}" + "\n"

        # return "ok"
    except Exception as e:
        print(e)



# Create a new person.
@app.route("/task", methods=["POST"])
def create_data():
    # print(IPAddr)
    try:
        jj = request.json

        res = 'response status code 200 \n{ \n'
        res += 'result: '
        for obj in jj:
            if len(obj) == 1:
                obj.update({'status': 0})
            task = Task(**obj)
            print(task)
            obj.update({'id': task.id})
            print(obj)
            temp_dict = obj
            x = mongo_collection.insert_one(temp_dict)
            print(x.inserted_id)
            res += '{{ \"name\": {} , \"status\": {}, \"id\":{} }} '.format(task.name, task.status, task.id)
        res += '\n}'
        return res
    except Exception as e:
        print(e)
        return "It's a bad request!", 400


# Update a person's age.
@app.route("/task/<id>", methods=["PUT"])
def update_age(id):
    try:
        dict_var = {}
        jj = request.json
        for ll in jj:
            dict_var.update(ll)

        query_dict = {'id': int(id)}
        # print(temp_dict)
        doc = mongo_collection.find_one(query_dict)
        if not doc:
            return "No such task!"
        for x in doc:
            print(x)
        newvalues = {"$set": dict_var}
        mongo_collection.update_many(query_dict, newvalues)
        res = 'response status code 200 \n{ \n'
        res += 'result: '
        res += str(jj)
        res += '}\n' + '}'
        return res

    except Exception as e:
        print(e)
        return "It's a bad request!", 400


# # Delete a person by ID.
@app.route("/task/<id>", methods=["DELETE"])
def delete_task(id):
    query_dict = {'id': int(id)}
    doc = mongo_collection.find_one(query_dict)
    if not doc:
        return "No such task!"
    mongo_collection.delete_many(query_dict)
    return "response status code 200"

# Create a RediSearch index for instances of the Person model.
if __name__ == "__main__":

    print(IPAddr)
    app.run('0.0.0.0', port="5000", debug=True)

