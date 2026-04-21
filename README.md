# API Test Suite - User Management

A comprehensive automated testing suite for a RESTful User Management API, built with Python and pytest.

## 📋 Overview

This project is an automated testing solution for a User Management API that supports CRUD operations (Create, Read, Update, Delete). The test suite validates API functionality across two environments (development and production) and is designed as part of an SDET challenge.

## 🏗️ Project Structure

```
Homework/
├── api/                        # API-related utilities (if any)
├── tests/                      # Test suite directory
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration and fixtures
│   ├── endpoints.py           # API endpoint configurations
│   ├── test_get.py            # GET endpoint tests
│   ├── test_post.py           # POST endpoint tests
│   ├── test_put.py            # PUT endpoint tests
│   ├── test_delete.py         # DELETE endpoint tests
│   ├── test_unsupported_methods.py  # Tests for unsupported HTTP methods
│   └── util/
│       ├── __init__.py
│       └── user_generator.py  # Utility for generating random test users
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI/CD pipeline
├── sdet_challenge_api.yml     # OpenAPI 3.0 specification
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
├── create_and_delete_user.py  # Utility script for user management
├── TestCases.MD               # Detailed test case documentation
└── Bugs.MD                    # Bug tracking and known issues
```

## 🎯 API Endpoints

The test suite covers the following User Management API endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | List all users |
| GET | `/users/{email}` | Get a specific user by email |
| POST | `/users` | Create a new user |
| PUT | `/users/{email}` | Update an existing user |
| DELETE | `/users/{email}` | Delete a user (requires authentication) |

### User Schema

```json
{
  "name": "string",
  "email": "string (email format)",
  "age": "integer (1-150)"
}
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Docker (for running the API server locally)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/hecalzu/Homework.git
cd Homework
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Tests

#### Local Testing

1. Start the API server using Docker:
```bash
docker run -p 3000:3000 -d ghcr.io/danielsilva-loanpro/sdet-interview-challenge:latest
```

2. Wait for the server to be ready (approximately 10 seconds), then run tests:

```bash
# Run tests against development environment (default)
pytest tests/ --env=dev -v

# Run tests against production environment
pytest tests/ --env=prod -v
```

#### Generate HTML Reports

```bash
pytest tests/ --env=dev --html=reports/report.html
```

## 🔄 CI/CD Pipeline

The project includes a GitHub Actions workflow that automatically:

- Runs on every push to main/master branches and pull requests
- Tests against both `dev` and `prod` environments in parallel
- Starts a Docker container with the API server
- Executes the full test suite with HTML and JUnit reports
- Uploads test reports as artifacts
- Generates an extended test summary

### Workflow Triggers

- **Push**: Runs on `main` and `master` branches
- **Pull Request**: Runs on PRs targeting `main` and `master` branches

## 📊 Test Coverage

The test suite includes comprehensive coverage of:

### Functional Tests
- **GET Tests** (`test_get.py`):
  - List all users (empty state)
  - Retrieve non-existent user (404 handling)
  - List multiple users and retrieve specific user by email

- **POST Tests** (`test_post.py`):
  - Create user with valid data
  - Handle duplicate email errors (409)
  - Validate required fields

- **PUT Tests** (`test_put.py`):
  - Update existing user
  - Handle user not found (404)
  - Validate update data

- **DELETE Tests** (`test_delete.py`):
  - Delete user with authentication
  - Handle missing authentication (401)
  - Handle user not found (404)

- **Unsupported Methods** (`test_unsupported_methods.py`):
  - Verify proper error handling for unsupported HTTP methods

## 🛠️ Configuration

### Pytest Options

| Option | Description | Default |
|--------|-------------|---------|
| `--env` | Target environment (dev/prod) | dev |
| `-v` | Verbose output | - |
| `--html` | Generate HTML report | - |
| `--junitxml` | Generate JUnit XML report | - |

### Environment Variables

The test suite uses the following configuration:

- **Development**: `http://localhost:3000/dev/users`
- **Production**: `http://localhost:3000/prod/users` (requires authentication token for some endpoints)

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `pytest` | Testing framework |
| `requests` | HTTP client for API calls |
| `faker` | Random data generation for tests |

## 📝 Additional Documentation

- **[TestCases.MD](TestCases.MD)**: Detailed test case descriptions and scenarios
- **[Bugs.MD](Bugs.MD)**: Known issues and bug reports
- **[sdet_challenge_api.yml](sdet_challenge_api.yml)**: Complete OpenAPI 3.0 specification

## 🔧 Utility Scripts

### create_and_delete_user.py
A standalone script for manually creating and deleting users for testing purposes.

## 🤝 Contributing

This is an SDET challenge project. For questions or issues, please contact the repository owner.

## 📄 License

This project is part of a software testing challenge and is intended for educational purposes.

## 👤 Author

**Hecalzu**  
[GitHub Profile](https://github.com/hecalzu)