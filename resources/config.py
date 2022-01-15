
import os
from dotenv import load_dotenv
import pathlib
import configparser

import resources.crypt as crypt
from resources.utility import string_to_list_of_dictionaries

current_path = str(pathlib.Path(__file__).parent.absolute()) + "/"                   # | # CURRENT DIRECTORY
current_path = current_path.replace("resources/", "")                                              # | # REAL DIR
configpath = str(current_path) + "settings.cfg"                                      # | # CONFIG FILE PATH
cfg = configparser.RawConfigParser()                                                 # | # CREATE CONFIG OBJECT
cfg.read(configpath)                                                                 # | # READ CONFIG FILE 





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

        ## Has encryption been setup?
        if os.path.isfile(self.key_location):
            # Yes
            self.encryption_key = crypt.get_key(self.key_location)

            self.crypt_setup = True
        else:
            self.crypt_setup = False
            # No
            print('user needs to setup initial key')
        


        ##### ACCOUNTS
        if self.crypt_setup: 
            self.media_accounts = string_to_list_of_dictionaries(self.read_encrypted_setting("accounts", "media_accounts"))
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


        #print('reading encrypted data:\n------------------------------------------------')
        #if self.crypt_setup: 
        #    print(self.media_accounts)
        #    print(type(self.media_accounts))
        
        #print('----------------------------------------------') 
        

    def reload_config(self):
        cfg.read(configpath)


    def read_encrypted_setting(self, category, setting):
        if self.crypt_setup:
            key = self.encryption_key
            encrypted_setting = self.get_setting_value(category, setting)
            fernet = crypt.get_fernet(key)
            setting = crypt.decrypt(fernet, encrypted_setting.encode())
            return setting
        else:
            print('crypt not setup')
            return None

    def write_encrypted_setting(self, category, setting, value):
        if self.crypt_setup:
            key = self.encryption_key
            fernet = crypt.get_fernet(key)
            value = crypt.encrypt(fernet, str(value).encode())
            self.set_setting_value(category, setting, value.decode())
            self.reload_config()
        else:
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

