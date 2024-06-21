import os
import requests

from dotenv import load_dotenv

load_dotenv()
SHORT_CODE = os.getenv('SHORT_CODE')
BEARER_TOKEN = os.getenv('BEARER_KEY')


headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {BEARER_TOKEN}'
}

payload = {
    "ShortCode": SHORT_CODE,
    "ResponseType": "Completed",
    "ConfirmationURL": "https://mydomain.com/confirmation",
    "ValidationURL": "https://mydomain.com/validation",
  }
response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl', headers = headers, data = payload)


print(response.text.encode('utf8'))