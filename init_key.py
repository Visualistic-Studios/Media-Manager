

# Imports
import os
from resources.config import settings_core
from resources.crypt import *
import configparser
import pathlib

## Get Key Configuration
current_path = str(pathlib.Path(__file__).parent.absolute()) + "/"                   # | # CURRENT DIRECTORY
current_path = current_path.replace("resources/", "")                                              # | # REAL DIR
configpath = str(current_path) + "settings.cfg"  
cfg = configparser.RawConfigParser()                                                 # | # CREATE CONFIG OBJECT
cfg.read(configpath) 
key_location = cfg.get("encryption","key_location")



# Check if key file exists at location
if not os.path.exists(key_location):
    #if not, create it
    store_key(create_key(), key_location)
    print("Key file created at: " + key_location)

