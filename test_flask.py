# test_hello_add.py
import json
from app_local import app
from flask import json


def setup_module(module):
    # clear database
    app.test_client().get('/clear')
    print("-------------- setup before module --------------")


def teardown_module(module):
    print("-------------- teardown after module --------------")

# test POST request
def test_post():
    # given the data to database
    with open('temp.json', encoding='utf-8') as f:
        # tasks = json.loads(f.read())
        tasks = json.load(f)
        response = app.test_client().post(
            '/task',
            json=tasks,
            content_type='application/json',
        )
    # response = app.test_client().get('/tasks')
    print(response.text)
    json_response = response
    str = ('response status code 200 \n'
           '{ \n'
           'result: { "name": Jack , "status": 1, "id":0 } { "name": bike , "status": 0, '
           '"id":1 } \n'
           '}')
    assert response.text == str


# test GET request
def test_get():
    response = app.test_client().get('/tasks')
    str = ('{\n'
           "    result: {'id': 0, 'name': 'Jack', 'status': 1},{'id': 1, 'name': 'bike', "
           "'status': 0} \n"
           '}')
    assert response.text == str

    #check redis database is working fine
    response_redis = app.test_client().get('/tasks')
    str = ('redis is working!\n'
           '{ \n'
           "result: [ {'id': 0, 'name': 'Jack', 'status': 1},{'id': 1, 'name': 'bike', "
           "'status': 0} ]\n"
           '}\n')
    assert response_redis.text == str

    # assert response.text == str


def test_put():
    with open('temp_put.json', encoding='utf-8') as f:
        # tasks = json.loads(f.read())
        tasks = json.load(f)
        response = app.test_client().put(
            '/task/1',
            json=tasks,
            content_type='application/json',
        )
    # response = app.test_client().get('/tasks')
    print(response.text)
    json_response = response
    str = ('response status code 200 \n'
           '{ \n'
           "result: [{'id': 1, 'name': '早餐', 'status': 0}]}\n"
           '}')
    assert response.text == str


# test_DELETE_request
def test_delete():
    response = app.test_client().delete('/task/1')
    str = 'response status code 200'
    assert response.text == str

    # assert response.text == str
