from faker import Faker
import logging
import json

def random_user():
    fake = Faker()
    return {
        "name": fake.name(),
        "email": fake.email(),
        "age": fake.random_int(min=18, max=80)
    }

def generate_random_user():
    user =  random_user()
    name =  user["name"]
    email = user["email"]
    age =   user["age"]

    body_data = {
        "age":      age,
        "email":    email,
        "name":     name        
    }

    logging.log(logging.INFO,"user info: ")
    logging.log(logging.INFO,name)
    logging.log(logging.INFO,email)
    logging.log(logging.INFO,age)

    json_body = json.dumps(body_data)

    return body_data,json_body