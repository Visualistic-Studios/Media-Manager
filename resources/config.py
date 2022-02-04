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
from dotenv import load_dotenv
import pathlib
import configparser

from resources.crypt import Crypt, Key
from resources.utility import string_to_list_of_dictionaries




#  _   _            _       _     _           
# | | | |          (_)     | |   | |          
# | | | | __ _ _ __ _  __ _| |__ | | ___  ___ 
# | | | |/ _` | '__| |/ _` | '_ \| |/ _ \/ __|
# \ \_/ / (_| | |  | | (_| | |_) | |  __/\__ \
#  \___/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/
# -----------------------------------------------------------------------                         



current_path = str(pathlib.Path(__file__).parent.absolute()) + "/"                   # | # CURRENT DIRECTORY
current_path = current_path.replace("resources/", "")                                              # | # REAL DIR
configpath = str(current_path) + "settings.cfg"                                      # | # CONFIG FILE PATH
cfg = configparser.RawConfigParser()                                                 # | # CREATE CONFIG OBJECT
cfg.read(configpath)                                                                 # | # READ CONFIG FILE 








#  _____ _                         
# /  __ \ |                        
# | /  \/ | __ _ ___ ___  ___  ___ 
# | |   | |/ _` / __/ __|/ _ \/ __|
# | \__/\ | (_| \__ \__ \  __/\__ \
#  \____/_|\__,_|___/___/\___||___/
# -----------------------------------------------------------------------   



class settings_core:
    
    def __init__(self):
        


        ##### ALL
        self.current_path = str(pathlib.Path(__file__).parent.absolute()) + "/"                     
        self.current_path = self.current_path.replace("resources/", "")                             
        self.saved_path = str(self.current_path) + "saved/"                                       


        ##### STORAGE
        self.published_posts_file_location = cfg.get("storage","posts_file")
        self.published_posts_file_location_full = current_path + self.published_posts_file_location

        self.scheduled_posts_file_location = cfg.get("storage","scheduled_posts_file")
        self.scheduled_posts_file_location_full = current_path + self.scheduled_posts_file_location

        self.uploaded_media_dir = cfg.get("storage","uploaded_media_dir")
        self.full_uploaded_media_dir = current_path + self.uploaded_media_dir


        ##### ENCRYPTION
        self.key_location = cfg.get("encryption","key_location")
        
        self.crypt = None

        ## Has encryption been setup?
        if os.path.isfile(self.key_location):
            # Yes, get key & block size
            self.encryption_key = Key(self.key_location)
            self.block_size = self.get_setting_value("encryption", "block_size")
            # No, set block size
            if str(self.block_size) == "None":
                self.set_setting_value("encryption", "block_size", "4096")
                self.block_size = 4096
            else:
                self.block_size = int(self.block_size)

            self.crypt = Crypt(self.encryption_key, self.block_size)

            self.crypt_setup = True
        else:
            self.crypt_setup = False
            
            print('user needs to setup initial key')
        

        ##### ACCOUNTS
        if self.crypt_setup: 
            media_accounts_temp = cfg.get("accounts","media_accounts")
            if media_accounts_temp != "None":
                self.media_accounts = string_to_list_of_dictionaries(self.read_encrypted_setting("accounts", "media_accounts"))
            else:
                self.media_accounts = None
        else:
            self.media_accounts = None


        self.supported_media_platforms = cfg.get("accounts","supported_media_platforms").split(",")

        ##### APPLICATION
        self.no_posts_title = cfg.get("app","no_posts_title")
        self.no_posts_description = cfg.get("app","no_posts_description")
        self.post_not_scheduled_for_reason_time_in_past = cfg.get("app","post_not_scheduled_for_reason_time_in_past")


        ##### PERFORMANCE
        self.posts_cache_time = float(cfg.get("performance","posts_cache_time"))
        self.page_cache_time = float(cfg.get("performance","page_cache_time"))

        ##### MEDIA
        self.supported_image_types = cfg.get("media","supported_image_types").split(",")
        self.supported_video_types = cfg.get("media","supported_video_types").split(",")


        ##### POSTING
        self.utc_timezones = cfg.get("posting","utc_timezones").split(",")
        self.default_timezone = cfg.get("posting","default_timezone")


    def reload_config(self):
        cfg.read(configpath)


    def read_encrypted_setting(self, category, setting):
        try:
            encrypted_setting = self.get_setting_value(category, setting)
            setting = self.crypt.decrypt(encrypted_setting.encode()).decode()
            return setting
        except Exception as e:
            print(e)
            return None

    def write_encrypted_setting(self, category, setting, value):
        try:
            value = self.crypt.encrypt(str(value).encode())
            self.set_setting_value(category, setting, value.decode())
            self.reload_config()
        except Exception as e:
            print(e)
            return None

    ##### GET ALL SETTINGS CATEGORIES
    def get_all_setting_categories(self):
        return cfg.sections()



    ##### GET ALL SETTINGS IN CATEGORY
    def get_all_settings_in_category(self,category):
        return cfg.options(category)



    ##### GET SETTING VALUE
    def get_setting_value(self,category,setting):
        return cfg.get(category,setting)


    ##### SET SETTING VALUE
    def set_setting_value(self,category,setting,value):
        cfg.set(category,setting,value)
        with open(configpath, 'w') as configfile:
            cfg.write(configfile)

        self.reload_config()

    ##### CREATE NEW SETTING
    def create_new_setting(self,category,setting,value):
        cfg.add_section(category)
        cfg.set(category,setting,value)
        with open(configpath, 'w') as configfile:
            cfg.write(configfile)
        
        self.reload_config()
    

    ##### CREATE NEW CATEGORY
    def create_new_category(self,category):
        cfg.add_section(category)
        with open(configpath, 'w') as configfile:
            cfg.write(configfile)
        
        self.reload_config()



class settings_server:
    
    def __init__(self):
        

        ##### ALL
        self.current_path = str(pathlib.Path(__file__).parent.absolute()) + "/"                     
        self.current_path = self.current_path.replace("resources/", "")                             
        self.saved_path = str(self.current_path) + "saved/"                                       


        ##### STORAGE
        self.published_posts_file_location = cfg.get("storage","posts_file")
        self.published_posts_file_location_full = current_path + self.published_posts_file_location

        self.scheduled_posts_file_location = cfg.get("storage","scheduled_posts_file")
        self.scheduled_posts_file_location_full = current_path + self.scheduled_posts_file_location

        self.uploaded_media_dir = cfg.get("storage","uploaded_media_dir")
        self.full_uploaded_media_dir = current_path + self.uploaded_media_dir


        ##### ENCRYPTION
        self.key_location = cfg.get("encryption","key_location")

        ## Has encryption been setup?
        if os.path.isfile(self.key_location):
            # Yes
            self.encryption_key = Key(self.key_location)
            self.block_size = int(self.read_encrypted_setting("encryption", "block_size"))
            print('block size = ' + str(self.block_size))
            if str(self.block_size) == "None":
                self.write_encrypted_setting("encryption", "block_size", "4096")
                self.block_size = 4096
            self.crypt = Crypt(self.encryption_key, self.block_size)

            self.crypt_setup = True
        else:
            self.crypt_setup = False
            # No
            print('user needs to setup initial key')
        

        ##### ACCOUNTS
        if self.crypt_setup: 
            media_accounts_temp = cfg.get("accounts","media_accounts")
            if media_accounts_temp != "None":
                self.media_accounts = string_to_list_of_dictionaries(self.read_encrypted_setting("accounts", "media_accounts"))
            else:
                self.media_accounts = None
        else:
            self.media_accounts = None




    def reload_config(self):
        cfg.read(configpath)


    def read_encrypted_setting(self, category, setting):
        try:
            encrypted_setting = self.get_setting_value(category, setting)
            setting = self.crypt.decrypt(encrypted_setting.encode()).decode()
            return setting
        except Exception as e:
            print('crypt not setup')
            return None

    def write_encrypted_setting(self, category, setting, value):
        try:
            value = self.crypt.encrypt(str(value).encode())
            self.set_setting_value(category, setting, value.decode())
            self.reload_config()
        except Exception as e:
            print('crypt not setup')
            return None

    ##### GET ALL SETTINGS CATEGORIES
    def get_all_setting_categories(self):
        return cfg.sections()



    ##### GET ALL SETTINGS IN CATEGORY
    def get_all_settings_in_category(self,category):
        return cfg.options(category)



    ##### GET SETTING VALUE
    def get_setting_value(self,category,setting):
        return cfg.get(category,setting)


    ##### SET SETTING VALUE
    def set_setting_value(self,category,setting,value):
        cfg.set(category,setting,value)
        with open(configpath, 'w') as configfile:
            cfg.write(configfile)

        self.reload_config()

    ##### CREATE NEW SETTING
    def create_new_setting(self,category,setting,value):
        cfg.add_section(category)
        cfg.set(category,setting,value)
        with open(configpath, 'w') as configfile:
            cfg.write(configfile)
        
        self.reload_config()
    

    ##### CREATE NEW CATEGORY
    def create_new_category(self,category):
        cfg.add_section(category)
        with open(configpath, 'w') as configfile:
            cfg.write(configfile)
        
        self.reload_config()



