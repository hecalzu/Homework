"""
Test module for DELETE API endpoints.

This module contains tests for the DELETE operations on the user management API,
including deleting users, handling non-existent users, and verifying authentication
requirements for delete operations.

Test Coverage:
- Deleting a non-existent user
- Creating and deleting a valid user
- Attempting to delete without authentication (production environment)
"""

import logging

import requests
import os
import sys
import pytest

sys.path.append(os.path.abspath('..'))
from tests.util.user_generator import generate_random_user
import json


def test_delete_unexisting_user(env_endpoint, request_headers):
    """
    Test that attempting to delete a non-existent user returns 404.
    
    This test verifies the API correctly handles delete requests for users
    that do not exist in the system. Uses a randomly generated email that
    is guaranteed not to exist.
    
    Expected Behavior:
    - Status code: 404 (Not Found)
    """
    body_data, json_body = generate_random_user()
    response = requests.delete(env_endpoint + "/" + body_data["email"], headers=request_headers)
    assert response.status_code == 404


def test_create_valid_user_and_delete_it(env_endpoint, request_headers):
    """
    Test the complete lifecycle of creating, verifying, and deleting a user.
    
    This test verifies the full workflow:
    1. Create a new user with valid data
    2. Verify the user appears in the list
    3. Delete the user
    4. Verify the user is no longer in the list
    
    Expected Behavior:
    - POST returns 201 (Created)
    - GET returns 200 with the user in the list
    - DELETE returns 204 (No Content)
    - Final GET returns 200 with empty list
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

    # Delete the user
    response = requests.delete(env_endpoint + "/" + body_data["email"], headers=request_headers)
    assert response.status_code == 204

    # Verify user is no longer in the list
    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert response.json() == []
    assert len(response.json()) == 0


def test_create_valid_user_and_delete_it_with_invalid_auth(env_endpoint, request_headers, env_config):
    """
    Test that deleting a user without proper authentication is rejected.
    
    This test verifies that the DELETE endpoint requires authentication.
    It creates a user, then attempts to delete without including the auth headers.
    
    Note: This test is skipped in non-production environments as the authorization
    token validation is only enforced in production.
    
    Expected Behavior (Production):
    - POST returns 201 (Created)
    - DELETE without auth headers returns 401 (Unauthorized)
    - User still exists after failed delete attempt
    """
    if env_config != 'prod':
        pytest.skip("This test is production-only due to authorization token")

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

    # Attempt delete without authentication headers
    response = requests.delete(env_endpoint + "/" + body_data["email"])
    assert response.status_code == 401

    # Verify user still exists
    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_user_with_invalid_auth_token(env_endpoint, request_headers, env_config):
    """
    Test that deleting a user with an invalid authentication token is rejected.
    
    This test verifies that the DELETE endpoint rejects invalid authentication tokens.
    
    Expected Behavior (Production):
    - POST returns 201 (Created)
    - DELETE with invalid auth token returns 401 (Unauthorized)
    - User still exists after failed delete attempt
    """
    if env_config != 'prod':
        pytest.skip("This test is production-only due to authorization token")

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

    # Attempt delete with invalid authentication token
    invalid_headers = {
        "Content-Type": "application/json",
        "Authentication": "invalid-token-12345"
    }
    response = requests.delete(env_endpoint + "/" + body_data["email"], headers=invalid_headers)
    assert response.status_code == 401

    # Verify user still exists
    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_user_idempotency(env_endpoint, request_headers):
    """
    Test that deleting a user is idempotent.
    
    This test verifies that:
    1. First DELETE on an existing user returns 204 (No Content)
    2. Second DELETE on the same user returns 404 (Not Found)
    
    Expected Behavior:
    - First DELETE returns 204
    - Second DELETE returns 404
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

    # First delete - should succeed
    response = requests.delete(env_endpoint + "/" + body_data["email"], headers=request_headers)
    assert response.status_code == 204

    # Verify user is no longer in the list
    response = requests.get(env_endpoint)
    assert response.status_code == 200
    assert len(response.json()) == 0

    # Second delete - should return 404 (user not found)
    response = requests.delete(env_endpoint + "/" + body_data["email"], headers=request_headers)
    assert response.status_code == 404


def test_delete_user_with_empty_auth_header(env_endpoint, request_headers, env_config):
    """
    Test that deleting a user with an empty authentication header is rejected.
    
    This test verifies that the DELETE endpoint rejects empty authentication headers.
    
    Expected Behavior (Production):
    - POST returns 201 (Created)
    - DELETE with empty auth header returns 401 (Unauthorized)
    - User still exists after failed delete attempt
    """
    if env_config != 'prod':
        pytest.skip("This test is production-only due to authorization token")

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

    # Attempt delete with empty authentication header
    empty_auth_headers = {
        "Content-Type": "application/json",
        "Authentication": ""
    }
    response = requests.delete(env_endpoint + "/" + body_data["email"], headers=empty_auth_headers)
    assert response.status_code == 401

    # Verify user still exists
    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert len(response.json()) == 1
