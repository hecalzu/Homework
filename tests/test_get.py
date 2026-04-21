import requests
import os
import sys

sys.path.append(os.path.abspath('..'))
from tests.util.user_generator import generate_random_user
import json

# Test listing all users while no user previously registered
def test_list_all_users_successfully_no_users(env_endpoint):

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert response.json() == []

# Test get non existing user
def test_list_unexisting_user(env_endpoint):

    response = requests.get(env_endpoint+"/"+"myemail@email.com")

    assert response.status_code == 404
    assert response.json() == []

# Test creating 3 different valid users, listing all 3 and getting 1 specific user.
def test_list_all_users_successfully_3_different_users(env_endpoint,test_context_users_teardown):
       
    user_list = []

    body_data,json_body = generate_random_user()
    specific_user_query_email = body_data["email"]
    json_body = json.dumps(body_data)
    requests.post(env_endpoint,json_body)
    test_context_users_teardown.append(body_data["email"])
    user_list.append(body_data)

    response = requests.get(env_endpoint)

    body_data,json_body = generate_random_user()

    json_body = json.dumps(body_data)
    requests.post(env_endpoint,json_body)
    test_context_users_teardown.append(body_data["email"])
    user_list.append(body_data)

    response = requests.get(env_endpoint)

    body_data,json_body = generate_random_user()

    json_body = json.dumps(body_data)
    requests.post(env_endpoint,json_body)
    test_context_users_teardown.append(body_data["email"])
    user_list.append(body_data)

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert response.json()      == user_list
    assert len(response.json()) == 3

    response = requests.get(env_endpoint+"/"+specific_user_query_email)
    assert response.status_code         == 200
    assert response.json()["email"]     == specific_user_query_email
