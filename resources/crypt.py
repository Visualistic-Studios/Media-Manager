#  _____                           _       
# |_   _|                         | |      
#   | | _ __ ___  _ __   ___  _ __| |_ ___ 
#   | || '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| || | | | | | |_) | (_) | |  | |_\__ \
#  \___/_| |_| |_| .__/ \___/|_|   \__|___/
#                | |                       
#                |_|                       
# -----------------------------------------------------------------------     



import os
import base64
from cryptography.fernet import Fernet

# ______                _   _                 
# |  ___|              | | (_)                
# | |_ _   _ _ __   ___| |_ _  ___  _ __  ___ 
# |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | | | |_| | | | | (__| |_| | (_) | | | \__ \
# \_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
# -----------------------------------------------------------------------     



########## CREATE KEY
#####
# create key from input string and save it to a file
def create_key():
    key = Fernet.generate_key()
    return key



########## STORE KEY
#####
#store key in a local file
def store_key(key, location):
    if location.split()[-1] == '/':
        del location[-1]

    with open(os.open(location + "/.key.pem", os.O_CREAT | os.O_WRONLY, 0o600), "wb") as f:
        f.write(key)



########## GET KEY
#####
# read key from a file  
def get_key(location):
    with open(location, "r") as f:
        key = f.read()
    return key



########## GET FERNET
#####
#get fernet
def get_fernet(key):
    fernet = Fernet(key)
    return fernet



########## ENCRYPT FILE
#####
# encrypt input string
def encrypt(fernet, byte_data):
    encrypted = fernet.encrypt(byte_data)
    return encrypted



########## DECRYPT FILE
##### 
# decrypt input string
def decrypt(fernet, byte_data):
    decrypted = fernet.decrypt(byte_data)
    return decrypted



class Key:


    def __init__(self, path):
        self.path = path

        # load key file into object
        with open(path, "r") as f:
            self._key = f.read()


    


    ##  CREATE KEY
    def create_key(self):
        key = Fernet.generate_key()
        return key



    ## GET KEY
    def get_key(self):
        return self._key



    ## sTORE KEY
    def store_key(self, location):
        if location.split()[-1] == '/':
            del location[-1]
        with open(os.open(location + "/.key.pem", os.O_CREAT | os.O_WRONLY, 0o600), "wb") as f:
            f.write(self.fernet.key)


    ## GET FERNET
    def get_fernet(key):
        fernet = Fernet(key)
        return fernet


class Crypt:
    def __init__(self, key, block_size):
        self.block_size = block_size
        self.fernet = Fernet(key.get_key())

    def encrypt(self, data):
        return self.fernet.encrypt(data)
    
    def decrypt(self, data):
        return self.fernet.decrypt(data)

    def encrypt_stream(self, f, out):
        while True:
            block = f.read(self.block_size)
            if not block:
                break
            out.write(base64.b64encode(self.encrypt(block)) + b"\n")

    def decrypt_stream(self, f, out):
        for l in f:
            line = l.rstrip()
            if (len(line) > 0):
                out.write(self.decrypt(base64.b64decode(line)))