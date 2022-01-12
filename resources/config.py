
import os
from dotenv import load_dotenv
import pathlib
import configparser




current_path = str(pathlib.Path(__file__).parent.absolute()) + "/"                   # | # CURRENT DIRECTORY
current_path = current_path.replace("resources/", "")                                              # | # REAL DIR
configpath = str(current_path) + "settings.cfg"                                      # | # CONFIG FILE PATH
cfg = configparser.RawConfigParser()                                                 # | # CREATE CONFIG OBJECT
cfg.read(configpath)                                                                 # | # READ CONFIG FILE 









class settings_core:
    
    def __init__(self):
        


        ##### ALL

        self.current_path = str(pathlib.Path(__file__).parent.absolute()) + "/"                     # | # CURRENT DIRECTORY
        self.current_path = self.current_path.replace("resources/", "")                                              # | # REAL DIR
        self.saved_path = str(self.current_path) + "saved/"                                               # | # REAL DIR



        ##### KEYS



        # string to list of dictionaries
        def string_to_list_of_dictionaries(self,string):

            # split string into list of dictionaries
            string = string.replace("},", "}|--|")
            list = string.split("|--|")

            list_of_dictionaries = []

            # make dictionary string a dictionary object
            for string_dict in list:
                string_dict = string_dict.replace("[", "") # remove [
                string_dict = string_dict.replace("]", "") # remove ]
                list_of_dictionaries.append(eval(string_dict))

            return list_of_dictionaries

        self.safe_storage = cfg.get("storage","safe")                                                 # | # SAFE STORAGE


        self.media_accounts = string_to_list_of_dictionaries(self, self.get_setting_value("accounts","media_accounts"))





        ##### STORAGE
        self.published_posts_file_location = cfg.get("storage","posts_file")
        self.published_posts_file_location_full = current_path + self.published_posts_file_location

        self.scheduled_posts_file_location = cfg.get("storage","scheduled_posts_file")
        self.scheduled_posts_file_location_full = current_path + self.scheduled_posts_file_location

        self.uploaded_media_dir = cfg.get("storage","uploaded_media_dir")
        self.full_uploaded_media_dir = current_path + self.uploaded_media_dir


        ##### ENCRYPTION
        self.secrets_location = cfg.get("accounts","secrets_location")
        self.key_location = cfg.get("accounts","key_location")

        # read key from a file  
        def get_key(location=self.key_location):
            with open(location, "r") as f:
                key = f.read()
            return key
        self.encryption_key = get_key()


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



    ##### CREATE NEW SETTING
    def create_new_setting(self,category,setting,value):
        cfg.add_section(category)
        cfg.set(category,setting,value)
        with open(configpath, 'w') as configfile:
            cfg.write(configfile)
    

    ##### CREATE NEW CATEGORY
    def create_new_category(self,category):
        cfg.add_section(category)
        with open(configpath, 'w') as configfile:
            cfg.write(configfile)


    ##### REGISTERS A NEW SOCIAL MEDIA ACCOUNT    
    def register_media_account(self, display_name, name, key, secret, token, token_secret):
        # get current accounts and add new one
        accounts = self.media_accounts
        accounts.append({"display_name":display_name, "name":name, "key":key, "secret":secret, "token":token, "token_secret":token_secret})
        # save new accounts
        self.set_setting_value("app","media_accounts",str(accounts))


    ##### REMOVES A SOCIAL MEDIA ACCOUNT
    def remove_media_account(self, name):
        # get current accounts and remove one
        accounts = self.media_accounts
        for account in accounts:
            if account["name"] == name:
                accounts.remove(account)
        # save new accounts
        self.set_setting_value("app","media_accounts",str(accounts))

    


