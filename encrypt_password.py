from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import requests
import json
import argparse
from base64 import b64encode
from Crypto.Hash import SHA256

class EncryptPassword:
    def __init__(self,password: str, hostname: str) -> None:
        self.password = password
        self.hostname = hostname
    
    def get_public_key(self):
        url = "{}/api/v1/encryption-config/".format(self.hostname)
        try:
            response = requests.request("GET", url)
            result = json.loads(response.text)
            return result
        except:
            return False
    
        
    def check_password(self):
        payload = {
            "username": "admin",
            "password": self.encrypted_password
            
        }
        headers = {
            'accept': "application/json, text/plain, */*",
            'content-type': "application/json",
        }
        payload = json.dumps(payload)  
        url = "https://webapp-demo.chematica.net/api/v1/auth/jwt/"
        response = requests.request("POST", url, data=payload, headers=headers)
        check_token = json.loads(response.text)
        check_token = "token" in check_token
        if check_token:
            return True
        else:
            return False
    
    def encrypt_password(self):
        result = self.get_public_key()
        try:
            if result['PASSWORD_ENCRYPTION_ENABLED']:
                public_key = result['PASSWORD_ENCRYPTION_PUBLIC_KEY']
                public_key = RSA.import_key(public_key)
                cipher = PKCS1_OAEP.new(key=public_key, hashAlgo=SHA256)
                self.encrypted_password = b64encode(cipher.encrypt(self.password.encode('utf-8')))
                self.encrypted_password = self.encrypted_password.decode('UTF-8')
                status = self.check_password()
                print(self.encrypted_password)
                if status:
                  print(self.encrypted_password)
                  return(self.encrypted_password)
            else:
              print(self.password)
              return(self.password)
        except:
            print(self.password)
            return(self.password)
            
    
    
def get_argparser() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(description="Specify the file")
    arg_parser.add_argument("password", metavar="password", type=str, help="password for the application")
    arg_parser.add_argument("url", metavar="url", type=str, help="url of the application")
    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    arg_parser = get_argparser()
    encrypt_password = EncryptPassword(arg_parser.password,arg_parser.url)
    encrypt_password.encrypt_password()
