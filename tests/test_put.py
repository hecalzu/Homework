"""
Test module for PUT API endpoints.

This module contains tests for the PUT operations on the user management API,
including updating user data, handling invalid requests, and edge cases
like updating with non-existent emails or duplicate email conflicts.

Test Coverage:
- Updating a valid user with new data
- Updating a user with malformed JSON body
- Attempting to update a non-existent user (wrong email)
- Updating a user with an email that already exists
"""

import logging

import requests
import os
import sys

sys.path.append(os.path.abspath('..'))
from tests.util.user_generator import generate_random_user
import json


def test_create_valid_user_update_data(env_endpoint, request_headers):
    """
    Test updating an existing user with new valid data.
    
    This test creates a user, then updates their name and age while keeping
    the same email (which serves as the identifier). Verifies that the update
    is successful and the user data is modified correctly.
    
    Expected Behavior:
    - User creation returns 201 (Created)
    - PUT request returns 200 (OK)
    - Response body contains the updated user data
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

    # Update user data while keeping the same email (identifier)
    body_data_update, json_body_update = generate_random_user()

    body_data_update["email"] = body_data["email"]

    response = requests.put(env_endpoint + "/" + body_data_update["email"], json.dumps(body_data_update))

    assert response.status_code == 200
    assert response.json() == body_data_update


def test_create_valid_user_update_invalid_json(env_endpoint, request_headers):
    """
    Test that updating a user with malformed JSON returns an error.
    
    This test creates a valid user, then attempts to update with invalid JSON
    syntax. Verifies that the API correctly rejects malformed requests.
    
    Expected Behavior:
    - User creation returns 201 (Created)
    - PUT request with malformed JSON returns 400 (Bad Request)
    """

    user_list = []

    body_data, json_body = generate_random_user()

    json_body = json.dumps(body_data)
    response = requests.post(env_endpoint, json_body)
    assert response.status_code == 201
    user_list.append(body_data)

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert response.json() == user_list
    assert len(response.json()) == 1

    # Attempt update with malformed JSON
    malformed_payload = '{"email": ' + body_data["email"]

    response = requests.put(env_endpoint + "/" + body_data["email"], malformed_payload)

    assert response.status_code == 400


def test_create_valid_user_update_data_wrong_email(env_endpoint, request_headers):
    """
    Test that updating a non-existent user returns an error.
    
    This test creates a valid user, then attempts to update a user with an
    email that doesn't exist in the system. Verifies proper error handling.
    
    Expected Behavior:
    - User creation returns 201 (Created)
    - PUT request for non-existent user returns 404 (Not Found)
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

    # Attempt to update using a non-existent email
    body_data_update, json_body_update = generate_random_user()

    body_data_update["email"] = "wrong@mail.com"

    response = requests.put(env_endpoint + "/" + body_data_update["email"], json.dumps(body_data_update))

    assert response.status_code == 404


def test_create_valid_user_update_data_with_existing_user_email(env_endpoint, request_headers):
    """
    Test updating a user to use an email that already belongs to another user.
    
    This test creates two users, then attempts to update the first user's email
    to match the second user's email. This tests how the API handles potential
    email conflicts during updates.
    
    Expected Behavior:
    - Both users are created successfully
    - PUT request returns 409 (Conflict) - duplicate email not allowed
    """

    user_list = []

    # Create first user (User A)
    body_data_a, json_body_a = generate_random_user()
    response = requests.post(env_endpoint, json.dumps(body_data_a))
    logging.log(logging.INFO, "user A created: ")
    logging.log(logging.INFO, body_data_a["email"])
    assert response.status_code == 201
    user_list.append(body_data_a)

    # Create second user (User B)
    body_data_b, json_body_b = generate_random_user()
    response = requests.post(env_endpoint, json.dumps(body_data_b))
    logging.log(logging.INFO, "user B created: ")
    logging.log(logging.INFO, body_data_b["email"])
    assert response.status_code == 201
    user_list.append(body_data_b)

    # Update User A's email to match User B's email (should fail with 409)
    body_data_a["email"] = body_data_b["email"]

    response = requests.put(env_endpoint + "/" + body_data_a["email"], json.dumps(body_data_a))

    assert response.status_code == 409


def test_update_user_age_below_minimum(env_endpoint, request_headers):
    """
    Test that updating a user with age below minimum (1) returns an error.
    
    This test verifies that the API validates the age field minimum boundary during update.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    """
    # Create a user first
    body_data, json_body = generate_random_user()
    response = requests.post(env_endpoint, json.dumps(body_data))
    assert response.status_code == 201

    # Attempt to update with age below minimum
    body_data["age"] = 0
    response = requests.put(env_endpoint + "/" + body_data["email"], json.dumps(body_data))

    assert response.status_code == 400


def test_update_user_age_above_maximum(env_endpoint, request_headers):
    """
    Test that updating a user with age above maximum (150) returns an error.
    
    This test verifies that the API validates the age field maximum boundary during update.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    """
    # Create a user first
    body_data, json_body = generate_random_user()
    response = requests.post(env_endpoint, json.dumps(body_data))
    assert response.status_code == 201

    # Attempt to update with age above maximum
    body_data["age"] = 151
    response = requests.put(env_endpoint + "/" + body_data["email"], json.dumps(body_data))

    assert response.status_code == 400


def test_update_user_negative_age(env_endpoint, request_headers):
    """
    Test that updating a user with negative age returns an error.
    
    This test verifies that the API rejects negative age values during update.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    """
    # Create a user first
    body_data, json_body = generate_random_user()
    response = requests.post(env_endpoint, json.dumps(body_data))
    assert response.status_code == 201

    # Attempt to update with negative age
    body_data["age"] = -5
    response = requests.put(env_endpoint + "/" + body_data["email"], json.dumps(body_data))

    assert response.status_code == 400


def test_update_user_invalid_email_format(env_endpoint, request_headers):
    """
    Test that updating a user with invalid email format returns an error.
    
    This test verifies that the API validates the email field format during update.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    """
    # Create a user first
    body_data, json_body = generate_random_user()
    response = requests.post(env_endpoint, json.dumps(body_data))
    assert response.status_code == 201

    # Attempt to update with invalid email format
    body_data["email"] = "invalid-email"
    response = requests.put(env_endpoint + "/" + body_data["email"], json.dumps(body_data))

    assert response.status_code == 400


def test_update_user_empty_email(env_endpoint, request_headers):
    """
    Test that updating a user with empty email returns an error.
    
    This test verifies that the API rejects empty email strings during update.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    """
    # Create a user first
    body_data, json_body = generate_random_user()
    response = requests.post(env_endpoint, json.dumps(body_data))
    assert response.status_code == 201

    # Attempt to update with empty email
    body_data["email"] = ""
    response = requests.put(env_endpoint + "/" + body_data["email"], json.dumps(body_data))

    assert response.status_code == 400


def test_update_user_empty_body(env_endpoint, request_headers):
    """
    Test that updating a user with empty body returns an error.
    
    This test verifies that the API rejects empty request bodies during update.
    
    Expected Behavior:
    - Status code: 400 (Bad Request)
    """
    # Create a user first
    body_data, json_body = generate_random_user()
    response = requests.post(env_endpoint, json.dumps(body_data))
    assert response.status_code == 201

    # Attempt to update with empty body
    response = requests.put(env_endpoint + "/" + body_data["email"], data='{}')

    assert response.status_code == 400
