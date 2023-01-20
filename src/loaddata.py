import json
import requests

with open('temp.json', encoding='utf-8') as f:
    # tasks = json.loads(f.read())
    tasks = json.load(f)
    r = requests.post('http://127.0.0.1:5000/task', json=tasks)

# for task in tasks:
#     r = requests.post('http://127.0.0.1:5000/task', json=task)
#     print(r.text)
    # print("name {} status {} was created".format(task.name, task.status))
    # print(f"Created person {person['first_name']} {person['last_name']} with ID {r.text}")
