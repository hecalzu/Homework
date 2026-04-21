"""
Test module for GET API endpoints.

This module contains tests for the GET operations on the user management API,
including listing all users and retrieving specific users by email.

Test Coverage:
- Listing all users when no users exist
- Attempting to retrieve a non-existent user
- Listing multiple users and retrieving a specific user
"""

import requests
import os
import sys

sys.path.append(os.path.abspath('..'))
from tests.util.user_generator import generate_random_user
import json


def test_list_all_users_successfully_no_users(env_endpoint):
    """
    Test that lists all users returns an empty list when no users exist.
    
    This test verifies the API correctly handles the initial state of the system
    where no users have been created yet.
    
    Expected Behavior:
    - Status code: 200 (OK)
    - Response body: Empty list []
    """

    response = requests.get(env_endpoint)

    assert response.status_code == 200
    assert response.json() == []


def test_list_unexisting_user(env_endpoint):
    """
    Test that attempts to retrieve a non-existent user returns 404.
    
    This test verifies the API correctly handles requests for users that
    do not exist in the system.
    
    Expected Behavior:
    - Status code: 404 (Not Found)
    - Response body: Empty list []
    """

    response = requests.get(env_endpoint + "/" + "myemail@email.com")

    assert response.status_code == 404
    assert response.json() == []


def test_list_all_users_successfully_3_different_users(env_endpoint, request_headers):
    """
    Test listing multiple users and retrieving a specific user by email.
    
    This test creates 3 different users and verifies:
    1. All users can be listed successfully
    2. A specific user can be retrieved by their email address
    3. The returned data matches the created user data
    
    Expected Behavior:
    - Creating users returns 201 (Created)
    - Listing all users returns 200 with all 3 users
    - Retrieving a specific user returns 200 with correct data
    """

    user_list = []

    # Create first user
    body_data, json_body = generate_random_user()
    specific_user_query_email = body_data["email"]
    json_body = json.dumps(body_data)
    requests.post(env_endpoint, json_body)
    user_list.append(body_data)

    response = requests.get(env_endpoint)

    # Create second user
    body_data, json_body = generate_random_user()

    json_body = json.dumps(body_data)
    requests.post(env_endpoint, json_body)
    user_list.append(body_data)

    response = requests.get(env_endpoint)

    # Create third user
    body_data, json_body = generate_random_user()

    json_body = json.dumps(body_data)
    requests.post(env_endpoint, json_body)
    user_list.append(body_data)

    response = requests.get(env_endpoint)

    # Verify all 3 users are returned
    assert response.status_code == 200
    assert response.json() == user_list
    assert len(response.json()) == 3

    # Verify specific user can be retrieved by email
    response = requests.get(env_endpoint + "/" + specific_user_query_email)
    assert response.status_code == 200
    assert response.json()["email"] == specific_user_query_email