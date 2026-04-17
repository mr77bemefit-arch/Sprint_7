from faker import Faker
import uuid

fake = Faker()

def password_generator():
    generated_password = fake.password(length=10, special_chars=False, digits=True, upper_case=True, lower_case=True)
    return generated_password

def courier_login_generator():
    generated_name = f"{fake.user_name()}_{uuid.uuid4().hex[:8]}"
    return generated_name

def courier_firstName_generator():
    generated_name = fake.first_name()
    return generated_name



 