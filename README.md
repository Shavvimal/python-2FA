# Implementing TOTP (Time-Based One-Time Password) Authentication in Python using PyOTP

## How does 2 Factor AUthentication work?

2FA is a common method for verifying the identity of users. Here we implement TOTPs, similar to mobile authenticator apps, such as Google Authenticator. We generate temporary passwords that typically expire after 30, 60, 120 or 240 seconds

PyOTP is a Python library for generating and verifying one-time passwords. It can be used to implement two-factor (2FA) or multi-factor (MFA) authentication methods in web applications and in other systems that require users to log in.

Creating a simple `auth_2FA` class for out Auth Methods:

```python
import pyotp
import qrcode

class auth_2FA:
    '''Class for verifying one-time passwords (TOTP: Time-Based One-Time Password Algorithm). For use with Google Authenticator'''
    @staticmethod
    def secret_key_gen():
        '''A helper function provided to generate a 32-character base32 secret, compatible with Google Authenticator and other OTP apps:'''
        return pyotp.random_base32()

    def gen_qr(self, secret_key:str):
        '''Generate provisioning URIs for use with the QR Code scanner built into MFA client apps - works with the Google Authenticator iPhone and Android app'''
        provisioning_uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name='nduk@duvera.co.uk', issuer_name='NDUK')
        img = qrcode.make(provisioning_uri)
        img.save("./totp_qr.png")

    def totp_gen(self, secret_key:str):
        '''Generates the Time-Based One-Time Password. Used for dev'''
        totp = pyotp.TOTP(secret_key)
        print("Current OTP:", totp.now())
        return totp.now()

    def validate_otp(self, code_to_verify: str, secret_key:str):
        '''TOTP verified for current time. Returns True or False. Used for Dev'''
        totp = pyotp.TOTP(secret_key)
        return totp.verify(code_to_verify)
```

We now have the methods we need. The flow is going to be:

1. _User registers_. When a user registers for an account on your application or website, you'll first store their hashed password securely in the database, just as you would with any regular password-based authentication system When we save their hashed passwords, we also generate a Base32 Secret using `secret_key_gen()` to enable TOTP for the user, and save this in the users table within our database aswell.
2. _QR Code_ PyOTP works with the Google Authenticator iPhone and Android app, as well as other OTP apps. PyOTP includes the ability to generate provisioning URIs for use with the QR Code scanner built into these MFA client apps. This is what `gen_qr()` does. We use the `qrcode` module to generate a QR code. We send this to the user.
3. _TOTP_ The TOTP algorithm uses the `HMAC-SHA1` (Hash-based Message Authentication Code with SHA-1) to generate the one-time passwords. The algorithm takes the secret key and the current timestamp as input and produces a unique, time-based OTP
4. _Validation_ When the user attempts to log in, along with their regular password, they will also be asked for the one-time password. The server uses the stored secret key associated with the user's account, and the current time, to calculate the expected OTP. It then compares the entered OTP with the expected OTP. If they match, the user is successfully authenticated. This is what we use `validate_otp` for.

To account for slight variations in time between the server and the user's device, a small grace period is usually allowed during OTP verification. For example, if the OTP generated for the user is not accepted, the server may check the OTPs for the previous and next time steps as well, to accommodate minor time differences.

As a developer, you might want to implement a backup mechanism for users to regain access in case they lose their TOTP device. This could include backup codes or alternative two-factor authentication methods, such as SMS or email verification.
