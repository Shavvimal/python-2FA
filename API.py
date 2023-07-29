import requests
import json
from hashlib import blake2b
from twofa import auth_2fa

class auth_api_key:
    '''Class for API calls to AWS for registering, JWT generation and verification, sectret key retrieval etc'''
    
    @staticmethod
    def hash_gen(password:str):
        '''BLAKE2 is a cryptographic hash function defined in RFC 7693 that comes in two flavors. We use BLAKE2b, optimized for 64-bit platforms'''
        b = password.encode('utf-8')
        h = blake2b()
        h.update(b)
        return h.hexdigest()
  
    def register(self, username:str, email:str, password: str):
        '''Function for registering and creating a user'''
        secret_key = auth_2fa.secret_key_gen()
        pload = {
        'username': username,
        'email': email,
        'password': self.hash_gen(password),
        'secret_key': secret_key
        }
        r = requests.post('https://d87k557w60.execute-api.us-east-1.amazonaws.com/default/auth', data = json.dumps(pload))
        print(r.json())
        if r.json()['statusCode'] == 200:
            auth_2fa.gen_qr(secret_key)
            print('Credentials don\'t exist yet, so user has been created. Please scan and add generated QR code to your list of OTP credentials.')

    def login(self, username:str, password: str, otp:str):
        '''Function for logging in and generating a JWT'''
        pload = {
        'username': username,
        'password': self.hash_gen(password),
        'otp': otp
        }
        r = requests.post('https://d87k557w60.execute-api.us-east-1.amazonaws.com/default/login', data = json.dumps(pload))
        print(r.text)

    def request_secret(self, jwt_token:str):
        '''Function for requesting secrets. Requires a valid JWT token in the header'''
        headers = {'jwt-token': jwt_token}
        r = requests.get('https://d87k557w60.execute-api.us-east-1.amazonaws.com/default/secretrequest', headers=headers)
        print(r.text)

api_caller = auth_api_key()

api_caller.register('Marcello2', 'Marcello2@email.com', 'password2' )

# api_caller.login('Marcello', 'password2', '477017' )
# api_caller.login('Ambrose', 'pa1ssword' )

# api_caller.request_secret('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJBbWJyb3NlIiwiZXhwIjoxNjYzMDY5MjkzLCJpYXQiOjE2NjMwNjIwOTMsInRpbWVfaXNzdWVkIjoiMTMvMDkvMjAyMiAwOTo0MTozMiIsInJvbGUiOiJ1c2VyIn0.bPPeykkuCRwfSBTi9Oxht8UisAiMyaZjz0BY4-p0Kwc')

# api_caller.request_secret('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJTaGF2IiwiZXhwIjoxNjYzMDA5MDI5LCJpYXQiOjE2NjMwMDE4MjksInRpbWVfaXNzdWVkIjoiMTIvMDkvMjAyMiAxNjo1NzowOSIsInJvbGUiOiJ1c2VyIn0.7G1BcL1nzRb6EeFhdHaflLhc2g9ekS0jeZVyh9rJ2A4')

# api_caller.request_secret('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJTaGF2IiwiZXhwIjoxNjYzMDY4NzYzLCJpYXQiOjE2NjMwNjE1NjMsInRpbWVfaXNzdWVkIjoiMTMvMDkvMjAyMiAwOTozMjo0MyIsInJvbGUiOiJ1c2VyIn0.HOmQ-qxKMY0IpzHVe5JiMUnQSe0F5Yk5OYQN6e2Ro7I')

# api_caller.login('Eryn', 'Indigo' )

# api_caller.request_secret('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJFcnluIiwiZXhwIjoxNjYzMDY5NDkyLCJpYXQiOjE2NjMwNjIyOTIsInRpbWVfaXNzdWVkIjoiMTMvMDkvMjAyMiAwOTo0NDo1MiIsInJvbGUiOiJhZG1pbiJ9.dhePs_P2Cj5Po06j3lTrqUa2V8vEAfPYqIzeemw-PEc')


