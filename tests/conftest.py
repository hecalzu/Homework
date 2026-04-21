# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="dev", help="Environment to run tests against: dev or prod"
    )

@pytest.fixture(scope="session")
def env_config(request):
    return request.config.getoption("--env")
