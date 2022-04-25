#  ___                                 _        
# |_ _| _ __ ___   _ __    ___   _ __ | |_  ___ 
#  | | | '_ ` _ \ | '_ \  / _ \ | '__|| __|/ __|
#  | | | | | | | || |_) || (_) || |   | |_ \__ \
# |___||_| |_| |_|| .__/  \___/ |_|    \__||___/
#                 |_|                           
# -----------------------------------------------------------------------   

import pathlib
import os
from resources.crypt import store_key, create_key
from resources.database import Storage




# __     __              _         _      _            
# \ \   / /  __ _  _ __ (_)  __ _ | |__  | |  ___  ___ 
#  \ \ / /  / _` || '__|| | / _` || '_ \ | | / _ \/ __|
#   \ V /  | (_| || |   | || (_| || |_) || ||  __/\__ \
#    \_/    \__,_||_|   |_| \__,_||_.__/ |_| \___||___/
# -----------------------------------------------------------------------                                                



# Get path to config file
current_path = str(pathlib.Path(__file__).parent.absolute()) + "/"
current_path = current_path.replace("resources/", "")
configpath = str(current_path) + "settings.cfg"



#  _____                      _    _                    
# |  ___| _   _  _ __    ___ | |_ (_)  ___   _ __   ___ 
# | |_   | | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
# |  _|  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
# |_|     \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
# -----------------------------------------------------------------------                                              



def register_first_time_setup():
    try: 
        open(current_path + "first_time_setup.txt", 'a+').close()
        print('registered first time setup')
        return True
    except Exception as e:
        print('Error While Creating First Time Setup File: ', e)
        return False



def check_first_time_setup():
    """
    Checks to see if the application has been setup. 

    It does this by checking to see if the first time setup file exists.
    """
    # Check if first time setup file exists
    ## If yes, return False to indicate that the application has been setup
    ## if not, create first time setup file & return True to indicate that the application has not been setup
 

    if os.path.exists(current_path + "first_time_setup.txt"):
        return True
    else:
        return False



def delete_first_time_setup():
    """
    Deletes the first time setup file.
    """
    try:
        os.remove(current_path + "first_time_setup.txt")
        return True
    except Exception as e:
        print('Error While Deleting First Time Setup File: ', e)
        return False



def initialize_settings():
    """
    Will copy settings from the template config file to the config file.
    """
    try:
        if not os.path.exists(configpath):
            with open(configpath, 'w') as configfile:
                    with open(current_path + "settings_template.cfg", 'r') as templatefile:
                        configfile.write(templatefile.read())
                        print('Settings File Created')
                        return True
    except Exception as e:
        print('Error While Initializing Settings File: ', e)
        return False



def initialize_app():
    """
    Will create all paths & the settings file when the application is first run.
    """
    try:
        initialize_settings()
        return True
    except Exception as e:
        print('Error While Initializing Application: ', e)
        return False



def initalize_encryption(key=None, key_location=None):
    """
    Will create a new key file from an input key text or by generating a new key.
    """

    from resources.config import settings_core

    settings = settings_core()

    settings.set_setting_value('encryption', 'key_location', key_location + "/.key.pem")

    try: 
        
        if key:
            key_byte = bytes(key, 'utf-8')
        else:
            key_byte = create_key()

        if key_byte:
            
            # check if key file exists
            if os.path.exists(key_location + "/.key.pem"):
                raise Exception('Key File Already Exists, please delete the key file to create a new one.')
            else:
                # if path does not exist, create it
                if not os.path.exists(key_location):
                    os.mkdir(key_location)
                store_key(key_byte, key_location)
                return key_byte, None
        else:
            raise Exception('Error While Creating Key')

    except Exception as e:
        return None, e


def intialize_s3(s3_access, s3_secret, s3_endpoint, s3_bucket):
    """
    Write encrypted S3 credentials to the configuration file.
    """
    try: 
        from resources.config import settings_core
        settings = settings_core()
        settings.set_setting_value("accounts","encrypted_s3_access",s3_access)
        settings.set_setting_value("accounts","encrypted_s3_secret",s3_secret)
        settings.set_setting_value("accounts","encrypted_s3_endpoint",s3_endpoint)
        settings.set_setting_value("accounts","encrypted_s3_bucket",s3_bucket)
        return True
    except: 
        return False



def setup_check():
    """
    Checks to see if the application requires first time setup. 

    It does this by checking to see if the config file exists.
    """
    # Check if config file exists
    ## If yes, return False to indicate that the application is not first time setup
    ## if not, copy settings template to config path & return True to indicate that the application is first time setup
    if not os.path.exists(configpath):
        register_first_time_setup()
        return True
    else:
        return False
    