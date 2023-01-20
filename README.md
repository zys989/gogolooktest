# Restful TASK LIST API

# Prerequisites
* Python 3.8
* docker
* docker compose

# Get the source code
* Clone the repository from GitHub:
* git clone https://github.com/zys989/gogolooktest.git
* cd gogolooktest
* pip3 install -r requirements.txt  

# How to run the code
* method 1
(1) Command line : python3 app_local.py   
    Note: use another terminal typing command line to start mongodb if mongodb is not working: mongod.  
    Browse to http://127.0.0.1:5000 to see the response from the web or using Postman.  
* method 2 (using docker)
(2) To start the containers use Command line: docker-compose up  
    Browse to http://127.0.0.1:5000 to see the response from the web or using Postman.  

# Unit testing
(1) Command line : pytest test_flask.py   

# Note:
The coverage of unit test is not complete: due to the New year vacation is coming, and I overestimate
my free time for this test...
