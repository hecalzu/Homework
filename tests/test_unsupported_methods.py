"""
Test module for unsupported HTTP methods.

This module contains tests for verifying that the API correctly rejects
unsupported HTTP methods with 405 Method Not Allowed status codes.

Test Coverage:
- PATCH on /users endpoint
- DELETE on /users endpoint (collection delete)
- POST on /users/{email} endpoint
- PUT on /users endpoint (collection update)
- Other unsupported methods on various endpoints
"""

import requests
import os
import sys

sys.path.append(os.path.abspath('..'))
from tests.util.user_generator import generate_random_user
import json


def test_patch_users_returns_405(env_endpoint):
    """
    Test that PATCH requests to /users endpoint return 405 Method Not Allowed.
    
    This test verifies that the API correctly rejects unsupported HTTP methods.
    
    Expected Behavior:
    - Status code: 405 (Method Not Allowed)
    """
    response = requests.patch(env_endpoint)
    assert response.status_code == 405


def test_delete_users_returns_405(env_endpoint, request_headers):
    """
    Test that DELETE requests to /users endpoint return 405 Method Not Allowed.
    
    This test verifies that the API correctly rejects collection delete operations.
    
    Expected Behavior:
    - Status code: 405 (Method Not Allowed)
    """
    response = requests.delete(env_endpoint, headers=request_headers)
    assert response.status_code == 405


def test_post_users_email_returns_405(env_endpoint, request_headers):
    """
    Test that POST requests to /users/{email} endpoint return 405 Method Not Allowed.
    
    This test verifies that the API correctly rejects POST operations on specific user endpoints.
    
    Expected Behavior:
    - Status code: 405 (Method Not Allowed)
    """
    body_data, json_body = generate_random_user()
    response = requests.post(env_endpoint + "/" + body_data["email"], json_body)
    assert response.status_code == 405


def test_put_users_returns_405(env_endpoint, request_headers):
    """
    Test that PUT requests to /users endpoint return 405 Method Not Allowed.
    
    This test verifies that the API correctly rejects collection update operations.
    
    Expected Behavior:
    - Status code: 405 (Method Not Allowed)
    """
    body_data, json_body = generate_random_user()
    response = requests.put(env_endpoint, json_body)
    assert response.status_code == 405


def test_head_users_returns_405(env_endpoint):
    """
    Test that HEAD requests to /users endpoint return 405 Method Not Allowed.
    
    This test verifies that the API correctly rejects HEAD method.
    
    Expected Behavior:
    - Status code: 405 (Method Not Allowed)
    """
    response = requests.head(env_endpoint)
    assert response.status_code == 405


def test_options_users_returns_405(env_endpoint):
    """
    Test that OPTIONS requests to /users endpoint return 405 Method Not Allowed.
    
    This test verifies that the API correctly rejects OPTIONS method.
    
    Expected Behavior:
    - Status code: 405 (Method Not Allowed)
    """
    response = requests.options(env_endpoint)
    assert response.status_code == 405


def test_trace_users_returns_405(env_endpoint):
    """
    Test that TRACE requests to /users endpoint return 405 Method Not Allowed.
    
    This test verifies that the API correctly rejects TRACE method.
    
    Expected Behavior:
    - Status code: 405 (Method Not Allowed)
    """
    response = requests.request('TRACE', env_endpoint)
    assert response.status_code == 405


def test_patch_users_email_returns_405(env_endpoint):
    """
    Test that PATCH requests to /users/{email} endpoint return 405 Method Not Allowed.
    
    This test verifies that the API correctly rejects PATCH operations on specific user endpoints.
    
    Expected Behavior:
    - Status code: 405 (Method Not Allowed)
    """
    body_data, json_body = generate_random_user()
    response = requests.patch(env_endpoint + "/" + body_data["email"])
    assert response.status_code == 405


def test_options_users_email_returns_405(env_endpoint):
    """
    Test that OPTIONS requests to /users/{email} endpoint return 405 Method Not Allowed.
    
    This test verifies that the API correctly rejects OPTIONS method on specific user endpoints.
    
    Expected Behavior:
    - Status code: 405 (Method Not Allowed)
    """
    body_data, json_body = generate_random_user()
    response = requests.options(env_endpoint + "/" + body_data["email"])
    assert response.status_code == 405