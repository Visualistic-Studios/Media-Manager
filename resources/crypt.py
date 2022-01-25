#  _____                           _       
# |_   _|                         | |      
#   | | _ __ ___  _ __   ___  _ __| |_ ___ 
#   | || '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| || | | | | | |_) | (_) | |  | |_\__ \
#  \___/_| |_| |_| .__/ \___/|_|   \__|___/
#                | |                       
#                |_|                       
# -----------------------------------------------------------------------     



from cryptography.fernet import Fernet
import os



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
        location = location[:-1]

    with open(os.open(location + "/.key.pem", os.O_CREAT | os.O_WRONLY, 0o600), "wb") as f:
        f.write(key)



########## GET KEY
#####
# read key from a file  
def get_key(location):
    with open(location, "r") as f:
        key = f.read()
    return key



########## EXPORT KEY
#####
# export key from file to file on disk from input string
def export_key(key, location):
    with open(os.open(location + "/.key.pem", os.O_CREAT | os.O_WRONLY, 0o600), "a+") as f:
        f.write(key)



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
    return str(decrypted.decode())



########## READ FILE
##### 
# read & decrypt encrypted data from file
def read_file(fernet, file_name):
    with open(file_name, "rb") as f:
        encrypted = f.read()
    decrypted = decrypt(fernet, encrypted)
    return decrypted



