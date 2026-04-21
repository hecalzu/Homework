"""
API endpoint configuration for the test suite.

This module centralizes all API endpoint URLs used in tests, making it easy
to update endpoints when the API changes or when switching between environments.

Endpoints:
- usersUrl: User management API endpoints for dev and prod environments
"""

# User management API endpoints for different environments
usersUrl = {
    'dev': "http://localhost:3000/dev/users",
    'prod': "http://localhost:3000/prod/users"
}