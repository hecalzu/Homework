import requests
import os
import sys
import logging
sys.path.append(os.path.abspath('..'))
from api import request_handler
from tests.user_generator import random_user
import json

def test_list_all_users_successfully_no_users(env_config):
    
    url = request_handler.getURL(env_config)

    logging.log(logging.INFO,"URL")
    logging.log(logging.INFO,url)

    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == []


def test_list_all_users_successfully_3_different_users(env_config):
    url = request_handler.getURL(env_config)

    

    user =  random_user()
    name =  user["name"]
    email = user["email"]
    age =   user["age"]

    body_data = {
        "name":     name,
        "email":    email,
        "age":      age
    }

    logging.log(logging.INFO,"user info: ")
    logging.log(logging.INFO,name)
    logging.log(logging.INFO,email)
    logging.log(logging.INFO,age)

    json_body = json.dumps(body_data)
    requests.post(url,json_body)

    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == json_body