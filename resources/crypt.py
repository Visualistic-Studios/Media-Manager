
# import libraries for cryptography fernet
from cryptography.fernet import Fernet
import os



# create key from input string and save it to a file
def create_key():
    key = Fernet.generate_key()
    return key



#store key in a local file
def store_key(key, location):
    with open(location, "wb") as f:
        f.write(key)



# read key from a file  
def get_key(location):
    with open(location, "r") as f:
        key = f.read()
    return key

# export key from file to file on disk from input string
def export_key(key, location):
    with open(location, "a+") as f:
        f.write(key)


#get fernet
def get_fernet(key):
    fernet = Fernet(key)
    return fernet


# encrypt input string
def encrypt(fernet, byte_data):
    encrypted = fernet.encrypt(byte_data)
    return encrypted

# decrypt input string
def decrypt(fernet, byte_data):
    decrypted = fernet.decrypt(byte_data)
    return str(decrypted.decode())


# read & decrypt encrypted data from file
def read_file(fernet, file_name):
    with open(file_name, "rb") as f:
        encrypted = f.read()
    decrypted = decrypt(fernet, encrypted)
    return decrypted

