"""
User data generator utility for tests.

This module provides functions to generate random user data for testing purposes.
It uses the Faker library to create realistic but fake user information.

Functions:
- random_user(): Generates a dictionary with random user data
- generate_random_user(): Generates user data and returns both dict and JSON string
"""

from faker import Faker
import logging
import json


def random_user():
    """
    Generate a dictionary with random user data.
    
    Creates a fake user with:
    - name: Random full name
    - email: Random email address
    - age: Random integer between 18 and 80
    
    Returns:
        dict: User data with 'name', 'email', and 'age' fields
    """
    fake = Faker()
    return {
        "name": fake.name(),
        "email": fake.email(),
        "age": fake.random_int(min=18, max=80)
    }


def generate_random_user():
    """
    Generate random user data and prepare it for API requests.
    
    This function generates random user data and returns both the dictionary
    format (for assertions) and JSON string format (for request bodies).
    
    Returns:
        tuple: (body_data, json_body) where:
            - body_data: dict with user data for assertions
            - json_body: JSON string for API request body
    """
    user = random_user()
    name = user["name"]
    email = user["email"]
    age = user["age"]

    body_data = {
        "age": age,
        "email": email,
        "name": name
    }

    logging.log(logging.INFO, "user info: ")
    logging.log(logging.INFO, name)
    logging.log(logging.INFO, email)
    logging.log(logging.INFO, age)

    json_body = json.dumps(body_data)

    return body_data, json_body