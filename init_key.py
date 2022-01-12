


import os
from resources.config import settings_core
from resources.crypt import *


settings = settings_core()


if not os.path.exists(settings.safe_storage):
    os.mkdir(settings.safe_storage)
    

#check if key file exists at location
if not os.path.exists(settings.key_location):
    #if not, create it
    store_key(create_key())
    print("Key file created at: " + settings.key_location)

if not os.path.exists(settings.secrets_location):
    #if not, create it
    with open(settings.secrets_location, "wb") as f:
        pass
    print("Secrets file created at: " + settings.secrets_location)
