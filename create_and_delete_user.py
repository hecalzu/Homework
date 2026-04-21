#!/usr/bin/env python3
import requests
import random
import string
import json

def generate_random_name():
    """Generate a random name"""
    first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_email():
    """Generate a random email address"""
    domains = ["example.com", "test.com", "demo.org", "sample.net", "mail.com"]
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    domain = random.choice(domains)
    return f"{username}@{domain}"

def generate_random_age():
    """Generate a random age between 18 and 80"""
    return random.randint(18, 80)

def main():
    # API endpoints
    base_url = "http://localhost:3000/prod/users"
    auth_token = "mysecrettoken"
    
    # Generate random user data
    name = generate_random_name()
    email = generate_random_email()
    age = generate_random_age()
    
    user_data = {
        "name": name,
        "email": email,
        "age": age
    }
    
    print(f"Generated user data: {user_data}")
    
    # Headers with authentication token (Note: uses 'Authentication' header, not 'Authorization')
    headers = {
        "Content-Type": "application/json",
        "Authentication": auth_token
    }
    
    # Step 1: Create user with POST request
    print("\n=== Creating user ===")
    try:
        response = requests.post(base_url, json=user_data, headers=headers)
        print(f"POST Response Status Code: {response.status_code}")
        print(f"POST Response Body: {response.text}")
        
        if response.status_code in [200, 201]:
            print("✅ User created successfully!")
        else:
            print(f"❌ Failed to create user. Status: {response.status_code}")
            return
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating user: {e}")
        return
    
    # Step 2: Delete user with DELETE request
    print(f"\n=== Deleting user with email: {email} ===")
    delete_url = f"{base_url}/{email}"
    
    try:
        response = requests.delete(delete_url, headers=headers)
        print(f"DELETE Response Status Code: {response.status_code}")
        print(f"DELETE Response Body: {response.text}")
        
        if response.status_code == 204:
            print("✅ User deleted successfully!")
        else:
            print(f"❌ Failed to delete user. Status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error deleting user: {e}")

if __name__ == "__main__":
    main()