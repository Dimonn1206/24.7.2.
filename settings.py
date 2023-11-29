import os

from  dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

fake_email = os.getenv('fake_email')
fake_password = os.getenv('fake_password')

