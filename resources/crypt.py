
# import libraries for cryptography fernet
from cryptography.fernet import Fernet
from resources.config import settings_core

settings = settings_core()


# create key from input string and save it to a file
def create_key():
    key = Fernet.generate_key()
    return key

#store key in a local file
def store_key(key, location=settings.key_location):
    with open(location, "wb") as f:
        f.write(key)

# read key from a file  
def get_key(location=settings.key_location):
    with open(location, "r") as f:
        key = f.read()
    return key

# export key from file to file on disk from input string
def export_key(key, location):
    with open(location, "a+") as f:
        f.write(key)

#get fernet
def get_fernet(location=settings.key_location):
    key = get_key(location)
    fernet = Fernet(key)
    return fernet


# encrypt input string
def encrypt(fernet, string):
    encrypted = fernet.encrypt(string)
    return encrypted

# decrypt input string
def decrypt(fernet, string):
    decrypted = fernet.decrypt(string)
    return decrypted


# read & decrypt encrypted data from file
def read_file(fernet, file_name):
    with open(file_name, "rb") as f:
        encrypted = f.read()
    decrypted = decrypt(fernet, encrypted)
    return decrypted

