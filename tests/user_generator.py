from faker import Faker

def random_user():
    fake = Faker()
    return {
        "name": fake.name(),
        "email": fake.email(),
        "age": 10
    }