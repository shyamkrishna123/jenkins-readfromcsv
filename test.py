from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import requests
import json
from base64 import b64encode
from Crypto.Hash import SHA256

hostname = "https://webapp-demo.chematica.net"
url = "{}/api/v1/encryption-config/".format(hostname)
response = requests.request("GET", url)
result = json.loads(response.text)
message = "passwordpassword"
if result['PASSWORD_ENCRYPTION_ENABLED']:
    print("true")
    public_key = result['PASSWORD_ENCRYPTION_PUBLIC_KEY']
    public_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key=public_key, hashAlgo=SHA256)
    encrypted_message = b64encode(cipher.encrypt(message.encode('utf-8')))
    login_url = "https://webapp-demo.chematica.net/api/v1/auth/jwt/"
    headers = {
    'accept': "application/json, text/plain, */*",
    'content-type': "application/json",
    }
    encrypted_message = encrypted_message.decode('UTF-8')
    payload = {
        "username":"admin",
        "password": encrypted_message }
    
    payload = json.dumps(payload)
    #print(payload)
    response = requests.request("POST", login_url, data=payload, headers=headers)

    print(response.text)
else:
    print("false")
