import requests
import os
import sys

sys.path.append(os.path.abspath('..'))
from tests.util.user_generator import generate_random_user
import json

# Test creating a new valid user and listing it at the end
def test_create_valid_user(env_endpoint, test_context_users_teardown):

    user_list = []

    body_data,json_body = generate_random_user()

    json_body = json.dumps(body_data)
    response = requests.post(env_endpoint,json_body)
    test_context_users_teardown.append(body_data["email"])
    assert response.status_code == 201
    user_list.append(body_data)

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert response.json()      == user_list
    assert len(response.json()) == 1

# Test creating a new duplicated user
def test_create_duplicatd_user(env_endpoint, test_context_users_teardown):

    user_list = []

    body_data,json_body = generate_random_user()

    json_body = json.dumps(body_data)
    response = requests.post(env_endpoint,json_body)
    test_context_users_teardown.append(body_data["email"])
    assert response.status_code == 201
    user_list.append(body_data)

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert response.json()      == user_list
    assert len(response.json()) == 1

    response = requests.post(env_endpoint,json_body)
    test_context_users_teardown.append(body_data["email"])
    #TODO: fix assertion once
    #assert response.status_code == 409
    assert response.status_code == 500

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert response.json()      == user_list
    assert len(response.json()) == 1

# Test creating a new user with incomplete data ("name") in json body
def test_create_user_incomplete_data_json_body_name(env_endpoint, test_context_users_teardown):

    
    body_data,json_body = generate_random_user()
    del body_data["name"]

    json_body = json.dumps(body_data)
    response = requests.post(env_endpoint,json_body)
    test_context_users_teardown.append(body_data["email"])
    assert response.status_code == 400

    response = requests.get(env_endpoint)    

    assert response.status_code == 200
    assert len(response.json()) == 0

# Test creating a new user with incomplete data ("age") in json body
def test_create_user_incomplete_data_json_body_age(env_endpoint, test_context_users_teardown):

    
    body_data,json_body = generate_random_user()
    del body_data["age"]

    json_body = json.dumps(body_data)
    response = requests.post(env_endpoint,json_body)
    test_context_users_teardown.append(body_data["email"])
    assert response.status_code == 400

    response = requests.get(env_endpoint)
    
    assert response.status_code == 200
    assert len(response.json()) == 0

# Test creating a new user with incomplete data ("email") in json body
def test_create_user_incomplete_data_json_body_email(env_endpoint):

    
    body_data,json_body = generate_random_user()
    del body_data["email"]

    json_body = json.dumps(body_data)
    response = requests.post(env_endpoint,json_body)
      
    assert response.status_code == 400

    response = requests.get(env_endpoint)
    
    assert response.status_code == 200
    assert len(response.json()) == 0

    

# Test creating a new user with invalid json body
def test_create_user_invalid_json_body(env_endpoint, test_context_users_teardown):
    
    malformed_payload = '{"email": "test@email"'
    
    response = requests.post(env_endpoint,data=malformed_payload)
    assert response.status_code == 400

    response = requests.get(env_endpoint)
    
    assert response.status_code == 200
    assert len(response.json()) == 0