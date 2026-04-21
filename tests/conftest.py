"""
Pytest configuration and fixtures for API test suite.

This module defines shared fixtures and configuration for all tests in the suite.
It handles environment setup, authentication headers, and test cleanup.

Fixtures:
- env_config: Determines which environment (dev/prod) to test against
- env_endpoint: Provides the API endpoint URL based on environment
- request_headers: Provides appropriate headers including auth for production
- run_before_after_test: Auto-run fixture that cleans up users before/after each test

Usage:
    pytest tests/ --env=dev    # Run tests against development environment
    pytest tests/ --env=prod   # Run tests against production environment
"""

import pytest
import requests
import logging
from tests import endpoints as ep


def pytest_addoption(parser):
    """
    Add custom command-line options to pytest.
    
    Adds the --env option to specify which environment to test against.
    Default is 'dev' for safety.
    
    Args:
        parser: Pytest parser object
    """
    parser.addoption(
        "--env", action="store", default="dev", help="Environment to run tests against: dev or prod"
    )


@pytest.fixture(scope="session")
def env_config(request):
    """
    Get the target environment configuration from command-line options.
    
    This fixture has session scope, meaning it's created once per test session
    and shared across all tests.
    
    Returns:
        str: The environment name ('dev' or 'prod')
    """
    return request.config.getoption("--env")


@pytest.fixture(autouse=True)
def run_before_after_test(env_endpoint, request_headers):
    """
    Auto-run fixture that cleans up users before and after each test.
    
    This fixture runs automatically before and after every test to ensure
    a clean state. It deletes any existing users before the test starts
    and cleans up any users created during the test.
    
    Note: This fixture is autouse=True, so it runs for every test automatically.
    """
    # Cleanup before test: delete any existing users
    response = requests.get(env_endpoint)
    for user in response.json():
        requests.delete(env_endpoint + "/" + user["email"], headers=request_headers)
    yield
    # Cleanup after test: delete any users created during the test
    logging.log(logging.INFO, "Cleaning up")
    response = requests.get(env_endpoint)
    for user in response.json():
        requests.delete(env_endpoint + "/" + user["email"], headers=request_headers)


@pytest.fixture(scope="session")
def env_endpoint(env_config):
    """
    Provide the API endpoint URL based on the selected environment.
    
    This fixture looks up the appropriate endpoint URL from the endpoints
    module based on whether we're testing against dev or prod.
    
    Args:
        env_config: The environment configuration from env_config fixture
        
    Returns:
        str: The full URL for the users API endpoint
    """
    logging.log(logging.INFO, "endpoint")
    logging.log(logging.INFO, env_config)
    return ep.usersUrl[env_config]


@pytest.fixture(scope="session")
def request_headers(env_config):
    """
    Provide HTTP headers for API requests based on the environment.
    
    For production, includes an authentication token. For development,
    only includes the Content-Type header.
    
    Args:
        env_config: The environment configuration from env_config fixture
        
    Returns:
        dict: Headers to include in API requests
    """
    headers = {}
    if env_config == "prod":
        auth_token = "mysecrettoken"
        headers = {
            "Content-Type": "application/json",
            "Authentication": auth_token
        }
    else:
        headers = {
            "Content-Type": "application/json"
        }
    return headers