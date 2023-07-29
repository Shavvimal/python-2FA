# conda install -c conda-forge pycryptodome
# In Python 3, encode it into a bytearray and decode

from Crypto.Cipher import AES
from hashlib import md5
import base64

password = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
input = 'hello world'

BLOCK_SIZE = 16

def pad (data):
    pad = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + pad * chr(pad)

def unpad (padded):
    pad = ord(chr(padded[-1]))
    return padded[:-pad]

def get_key_iv (password):
    m = md5()
    m.update(password.encode('utf-8'))
    key = m.hexdigest()

    m = md5()
    m.update((password + key).encode('utf-8'))
    iv = m.hexdigest()
    
    return [key.encode("utf8"),iv.encode("utf8")]

def _encrypt(data, password):
    key,iv = get_key_iv(password)
    data = pad(data).encode("utf8")
    aes = AES.new(key, AES.MODE_CBC, iv[:16])

    encrypted = aes.encrypt(data)
    return base64.urlsafe_b64encode(encrypted).decode("utf8")

def _decrypt(edata, password):
    edata = base64.urlsafe_b64decode(edata)
    key,iv = get_key_iv(password)

    aes = AES.new(key, AES.MODE_CBC, iv[:16])
    return unpad(aes.decrypt(edata)).decode("utf8")


output = _encrypt(input, password) 
print(output)
plaintext = _decrypt(output, password)
print(plaintext)

