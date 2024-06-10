from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_fake_data():
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    # Generate a valid phone number with only digits
    phone_number = ''.join(random.choice('0123456789') for _ in range(10))
    # Generate a birthday no earlier than 1970
    start_date = datetime(1970, 1, 1)
    end_date = datetime.now() - timedelta(days=365*18)  # 18 years ago
    birthday = fake.date_time_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')
    # Add meaningful additional info
    additional_info = f"{first_name} {last_name} is a valued customer."

    fake_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "birthday": birthday,
        "additional_info": additional_info
    }
    return fake_data

if __name__ == "__main__":
    for _ in range(10):  # Generating 10 sets of fake data
        print(generate_fake_data())
