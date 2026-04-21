import requests
import os
import sys

sys.path.append(os.path.abspath('..'))
from tests.util.user_generator import generate_random_user
import json

# Test creating a new valid user and update data
def test_create_valid_user_update_data(env_endpoint, test_context_users_teardown):

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

    body_data_update,json_body_update = generate_random_user()

    body_data_update["email"] = body_data["email"]

    response = requests.put(env_endpoint+"/"+body_data_update["email"],json.dumps(body_data_update))

    assert response.status_code == 200
    assert response.json() == body_data_update


    # Test creating a new valid user and updating with malformed json body
def test_create_valid_user_update_invalid_json(env_endpoint, test_context_users_teardown):

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

    malformed_payload = '{"email": ' + body_data["email"]

    response = requests.put(env_endpoint+"/"+body_data["email"],malformed_payload)

    assert response.status_code == 400

# Test creating a new valid user and try to update data with wrong email
def test_create_valid_user_update_data_wrong_email(env_endpoint, test_context_users_teardown):

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

    body_data_update,json_body_update = generate_random_user()

    body_data_update["email"] = "wrong@mail.com"

    response = requests.put(env_endpoint+"/"+body_data_update["email"],json.dumps(body_data_update))

    assert response.status_code == 404

# Test creating a new valid user and update data using an existing user email
def test_create_valid_user_update_data_with_existing_user_email(env_endpoint, test_context_users_teardown):

    user_list = []

    body_data,json_body = generate_random_user()

    response = requests.post(env_endpoint,json_body)
    test_context_users_teardown.append(body_data["email"])
    assert response.status_code == 201
    user_list.append(body_data)

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert response.json()      == user_list
    assert len(response.json()) == 1

    body_data_update,json_body_update = generate_random_user()

    response = requests.post(env_endpoint,json_body_update)
    test_context_users_teardown.append(body_data_update["email"])
    assert response.status_code == 201
    user_list.append(body_data)

    body_data_update["email"] = body_data["email"]

    response = requests.put(env_endpoint+"/"+body_data["email"],json.dumps(body_data_update))

    assert response.status_code == 200
    assert response.json() == body_data_update