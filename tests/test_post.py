"""
Test module for POST API endpoints.

This module contains tests for the POST operations on the user management API,
including creating users with valid data, handling duplicates, and validating
input data requirements.

Test Coverage:
- Creating a new valid user
- Attempting to create a duplicate user (same email)
- Creating a user with incomplete data (missing name, age, or email)
- Creating a user with invalid/malformed JSON body
"""

import logging

import requests
import os
import sys

sys.path.append(os.path.abspath('..'))
from tests.util.user_generator import generate_random_user
import json


def test_create_valid_user(env_endpoint, request_headers):
    """
    Test creating a new valid user with all required fields.
    
    This test verifies that a user can be successfully created with valid data
    and that the user appears in the list of all users after creation.
    
    Expected Behavior:
    - Status code: 201 (Created)
    - User appears in the list of all users
    - List contains exactly 1 user with matching data
    """

    user_list = []

    body_data, json_body = generate_random_user()

    json_body = json.dumps(body_data)
    response = requests.post(env_endpoint, json_body)
    logging.log(logging.INFO, "user created: ")
    logging.log(logging.INFO, body_data["email"])
    assert response.status_code == 201
    user_list.append(body_data)

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert response.json() == user_list
    assert len(response.json()) == 1


def test_create_duplicatd_user(env_endpoint, request_headers):
    """
    Test that attempting to create a user with a duplicate email is handled correctly.
    
    This test creates a user, then attempts to create another user with the same email.
    The API should reject the duplicate with an appropriate error status code.
    
    Note: Currently the API returns 500 instead of the expected 409 (Conflict).
    This is a known issue tracked in the bug report.
    
    Expected Behavior:
    - First POST returns 201 (Created)
    - Second POST with same email should return 409 (Conflict) - currently returns 500
    - User list still contains only 1 user after duplicate attempt
    """

    user_list = []

    body_data, json_body = generate_random_user()

    json_body = json.dumps(body_data)
    response = requests.post(env_endpoint, json_body)
    logging.log(logging.INFO, "user created: ")
    logging.log(logging.INFO, body_data["email"])
    assert response.status_code == 201
    user_list.append(body_data)

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert response.json() == user_list
    assert len(response.json()) == 1

    # Attempt to create duplicate user with same email
    response = requests.post(env_endpoint, json_body)
    logging.log(logging.INFO, "user created: ")
    logging.log(logging.INFO, body_data["email"])
    # TODO: fix assertion once API returns correct 409 status code for duplicates
    # Expected: 409 (Conflict) - Currently returns 500 (Internal Server Error)
    assert response.status_code == 500

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert response.json() == user_list
    assert len(response.json()) == 1


def test_create_user_incomplete_data_json_body_name(env_endpoint, request_headers):
    """
    Test that creating a user without a 'name' field returns an error.
    
    This test verifies that the API validates required fields and rejects
    requests with missing 'name' attribute.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    - No user is created (list remains empty)
    """

    body_data, json_body = generate_random_user()
    del body_data["name"]

    json_body = json.dumps(body_data)
    response = requests.post(env_endpoint, json_body)
    logging.log(logging.INFO, "user created: ")
    logging.log(logging.INFO, body_data["email"])
    assert response.status_code == 400

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_create_user_incomplete_data_json_body_age(env_endpoint, request_headers):
    """
    Test that creating a user without an 'age' field returns an error.
    
    This test verifies that the API validates required fields and rejects
    requests with missing 'age' attribute.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    - No user is created (list remains empty)
    """

    body_data, json_body = generate_random_user()
    del body_data["age"]

    json_body = json.dumps(body_data)
    response = requests.post(env_endpoint, json_body)
    logging.log(logging.INFO, "user created: ")
    logging.log(logging.INFO, body_data["email"])
    assert response.status_code == 400

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_create_user_incomplete_data_json_body_email(env_endpoint):
    """
    Test that creating a user without an 'email' field returns an error.
    
    This test verifies that the API validates required fields and rejects
    requests with missing 'email' attribute. Email is typically the primary
    identifier for users, so this validation is critical.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    - No user is created (list remains empty)
    """

    body_data, json_body = generate_random_user()
    del body_data["email"]

    json_body = json.dumps(body_data)
    response = requests.post(env_endpoint, json_body)
    assert response.status_code == 400

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_create_user_invalid_json_body(env_endpoint, request_headers):
    """
    Test that creating a user with malformed JSON returns an error.
    
    This test verifies that the API correctly handles and rejects requests
    with invalid JSON syntax in the request body.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    - No user is created (list remains empty)
    """

    malformed_payload = '{"email": "test@email"'

    response = requests.post(env_endpoint, data=malformed_payload)

    assert response.status_code == 400

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_create_user_age_below_minimum(env_endpoint, request_headers):
    """
    Test that creating a user with age below minimum (1) returns an error.
    
    This test verifies that the API validates the age field minimum boundary.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    - No user is created (list remains empty)
    """
    body_data = {
        "name": "Test User",
        "email": "test@example.com",
        "age": 0
    }

    response = requests.post(env_endpoint, json.dumps(body_data))

    assert response.status_code == 400

    response = requests.get(env_endpoint)
    assert len(response.json()) == 0


def test_create_user_age_at_minimum(env_endpoint, request_headers):
    """
    Test that creating a user with age at minimum (1) is successful.
    
    This test verifies that the API accepts the minimum boundary value for age.
    
    Expected Behavior:
    - Status code: 201 (Created)
    - User is created successfully
    """
    body_data = {
        "name": "Test User",
        "email": "test@example.com",
        "age": 1
    }

    response = requests.post(env_endpoint, json.dumps(body_data))

    assert response.status_code == 201

    response = requests.get(env_endpoint)
    assert len(response.json()) == 1
    assert response.json()[0]["age"] == 1


def test_create_user_age_at_maximum(env_endpoint, request_headers):
    """
    Test that creating a user with age at maximum (150) is successful.
    
    This test verifies that the API accepts the maximum boundary value for age.
    
    Expected Behavior:
    - Status code: 201 (Created)
    - User is created successfully
    """
    body_data = {
        "name": "Test User",
        "email": "test@example.com",
        "age": 150
    }

    response = requests.post(env_endpoint, json.dumps(body_data))

    assert response.status_code == 201

    response = requests.get(env_endpoint)
    assert len(response.json()) == 1
    assert response.json()[0]["age"] == 150


def test_create_user_age_above_maximum(env_endpoint, request_headers):
    """
    Test that creating a user with age above maximum (150) returns an error.
    
    This test verifies that the API validates the age field maximum boundary.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    - No user is created (list remains empty)
    """
    body_data = {
        "name": "Test User",
        "email": "test@example.com",
        "age": 151
    }

    response = requests.post(env_endpoint, json.dumps(body_data))

    assert response.status_code == 400

    response = requests.get(env_endpoint)
    assert len(response.json()) == 0


def test_create_user_negative_age(env_endpoint, request_headers):
    """
    Test that creating a user with negative age returns an error.
    
    This test verifies that the API rejects negative age values.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    - No user is created (list remains empty)
    """
    body_data = {
        "name": "Test User",
        "email": "test@example.com",
        "age": -5
    }

    response = requests.post(env_endpoint, json.dumps(body_data))

    assert response.status_code == 400

    response = requests.get(env_endpoint)
    assert len(response.json()) == 0


def test_create_user_non_integer_age(env_endpoint, request_headers):
    """
    Test that creating a user with non-integer age returns an error.
    
    This test verifies that the API validates the age field type.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    - No user is created (list remains empty)
    """
    body_data = {
        "name": "Test User",
        "email": "test@example.com",
        "age": 25.5
    }

    response = requests.post(env_endpoint, json.dumps(body_data))

    assert response.status_code == 400

    response = requests.get(env_endpoint)
    assert len(response.json()) == 0


def test_create_user_invalid_email_format(env_endpoint, request_headers):
    """
    Test that creating a user with invalid email format returns an error.
    
    This test verifies that the API validates the email field format.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    - No user is created (list remains empty)
    """
    body_data = {
        "name": "Test User",
        "email": "invalid-email",
        "age": 25
    }

    response = requests.post(env_endpoint, json.dumps(body_data))

    assert response.status_code == 400

    response = requests.get(env_endpoint)
    assert len(response.json()) == 0


def test_create_user_empty_email(env_endpoint, request_headers):
    """
    Test that creating a user with empty email returns an error.
    
    This test verifies that the API rejects empty email strings.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    - No user is created (list remains empty)
    """
    body_data = {
        "name": "Test User",
        "email": "",
        "age": 25
    }

    response = requests.post(env_endpoint, json.dumps(body_data))

    assert response.status_code == 400

    response = requests.get(env_endpoint)
    assert len(response.json()) == 0


def test_create_user_empty_body(env_endpoint, request_headers):
    """
    Test that creating a user with empty body returns an error.
    
    This test verifies that the API rejects empty request bodies.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    - No user is created (list remains empty)
    """
    response = requests.post(env_endpoint, data='{}')

    assert response.status_code == 400

    response = requests.get(env_endpoint)
    assert len(response.json()) == 0
