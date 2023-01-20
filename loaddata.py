import json
import requests

with open('temp.json', encoding='utf-8') as f:
    # tasks = json.loads(f.read())
    tasks = json.load(f)
    r = requests.post('http://127.0.0.1:5000/task', json=tasks)
