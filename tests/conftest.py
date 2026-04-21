# conftest.py
import pytest
import requests
import logging
from tests import endpoints as ep

def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="dev", help="Environment to run tests against: dev or prod"
    )

@pytest.fixture(scope="session")
def env_config(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def test_context_users_teardown():
    context_users = []
    yield context_users

@pytest.fixture(autouse=True)
def run_before_after_test(test_context_users_teardown, env_endpoint, request_headers):
    response = requests.get(env_endpoint)
    for user in response.json():
        requests.delete(env_endpoint+"/"+user["email"], headers=request_headers)
    yield
    logging.log(logging.INFO, "Cleaning up")
    for email in test_context_users_teardown:
        requests.delete(env_endpoint+"/"+email)
        test_context_users_teardown.remove(email)

@pytest.fixture(scope="session")
def env_endpoint(env_config):
    logging.log(logging.INFO, "endpoint")
    logging.log(logging.INFO, env_config)
    return ep.usersUrl[env_config]

@pytest.fixture(scope="session")
def request_headers(env_config):
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