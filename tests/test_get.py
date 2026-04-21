import requests
import os
import sys
import logging
sys.path.append(os.path.abspath('..'))
from api import request_handler

def test_list_all_users_successfully_no_users(env_config):
    
    url = request_handler.getURL(env_config)

    logging.log(logging.INFO,"URL")
    logging.log(logging.INFO,url)

    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == []


def test_list_all_users_successfully_3_different_users(env_config, random_user):
    url = request_handler.getURL(env_config)

    

    name,email,age = random_user
    logging.log(logging.INFO,"user info: ")
    logging.log(logging.INFO,name)
    logging.log(logging.INFO,email)
    logging.log(logging.INFO,name)
    
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == []