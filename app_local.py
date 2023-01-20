from flask import Flask, request, jsonify
import pymongo
import redis
import socket

from task import Task

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
app = Flask(__name__)

mongo_client = pymongo.MongoClient(host = 'localhost', port=27017)
db = mongo_client["gogolook"]
mongo_collection = db["data"]

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)

rr = redis.Redis(connection_pool=pool)


# get content of all tasks
@app.route("/tasks", methods=["GET"])
def get_data():
    try:
        temp_list = []
        cursor = mongo_collection.find()
        # check if the data is in redis cache
        if 'all' not in rr.keys():
            for doc in cursor:
                # processing the output text
                tempstr = str(doc)
                startindex = tempstr.index("\'name\'")
                endindex = tempstr.index(", 'id'")
                res1 = tempstr[startindex:endindex]
                res2 = tempstr[endindex + 2:len(tempstr) - 1]
                res = "{" + res2.strip() + ", " + res1.strip() + "}"
                temp_list.append(res)
            rr_str = 'result: [ {} ]'.format(','.join(temp_list))
            rr.set("all", rr_str, ex=10)
            ans = '{\n'
            ans += '    result: {} '.format(','.join(temp_list))
            ans += '\n}'
            return ans
        else:
            # if cache is available, return by cache
            return "redis is working!\n" + "{ \n" + str(rr.get('all')) + "\n}" + "\n"

    except Exception as e:
        print(e)


# Create a new task
@app.route("/task", methods=["POST"])
def create_data():
    try:
        jj = request.json

        res = 'response status code 200 \n{ \n'
        res += 'result: '
        for obj in jj:
            if len(obj) == 1:
                obj.update({'status': 0})
            task = Task(**obj)
            obj.update({'id': task.id})
            temp_dict = obj
            x = mongo_collection.insert_one(temp_dict)
            res += '{{ \"name\": {} , \"status\": {}, \"id\":{} }} '.format(task.name, task.status, task.id)
        res += '\n}'
        return res
    except Exception as e:
        print(e)
        return "It's a bad request!", 400


# Update a task by id
@app.route("/task/<id>", methods=["PUT"])
def update_age(id):
    try:
        dict_var = {}
        jj = request.json
        for ll in jj:
            dict_var.update(ll)

        query_dict = {'id': int(id)}
        # find the id is in database or not
        doc = mongo_collection.find_one(query_dict)
        if not doc:
            return "No such task!"
        # processing the request if id is found
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


# clear database
@app.route("/clear", methods=["GET"])
def clear_db():
    mongo_collection.drop()
    rr.flushdb()
    return "successfully clear!"


# # Delete a task by ID.
@app.route("/task/<id>", methods=["DELETE"])
def delete_task(id):
    query_dict = {'id': int(id)}
    # find task id is in database or not
    doc = mongo_collection.find_one(query_dict)
    if not doc:
        return "No such task!"
    mongo_collection.delete_many(query_dict)
    return "response status code 200"


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
