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


auth_2fa = auth_2FA()
