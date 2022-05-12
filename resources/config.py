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
import pathlib
import configparser
import ast
import pickle


from resources.crypt import Crypt, Key
from resources.utility import string_to_list_of_dictionaries
from resources.database import Storage
from resources.global_mentions import global_mentions_manager


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
        self.current_path = current_path                         
        self.saved_path = str(self.current_path) + "saved/"                                       

        ##### STORAGE
        self.published_posts_file = self.get_setting_value("storage","encrypted_posts_file")
        self.published_posts_file_location = "saved/" + self.published_posts_file
        self.published_posts_file_location_full = current_path + self.published_posts_file
        self.scheduled_posts_file = self.get_setting_value("storage","encrypted_scheduled_posts_file")
        self.scheduled_posts_file_location = "saved/" + self.scheduled_posts_file
        self.scheduled_posts_file_location_full = current_path + self.scheduled_posts_file # This needs to be changed for S3 support
        self.uploaded_media_dir = self.get_setting_value("storage","encrypted_uploaded_media_dir")
        self.full_uploaded_media_dir = self.saved_path + self.uploaded_media_dir
        
        


        ##### ENCRYPTION
        self.key_location = self.get_setting_value("encryption","hidden_key_location")
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
        

        ########## ENCRYPTED
        #####
        if self.crypt_setup: 

            ##### ACCOUNTS
            media_accounts_temp = self.get_setting_value("accounts","encrypted_media_accounts")
            if media_accounts_temp != "None":
                self.media_accounts = string_to_list_of_dictionaries(self.get_setting_value(category="accounts", setting="encrypted_media_accounts"))
            else:
                self.media_accounts = None

            self.supported_media_platforms = self.get_setting_value("accounts","encrypted_supported_media_platforms").split(",")
            
            ##### SERVER
            self.processing_delay_in_seconds = int(self.get_setting_value("server",setting="encrypted_processing_delay_in_seconds", auto_decrypt=True))
            
            ##### S3 CREDENTIALS
            self.s3_access = self.get_setting_value(category="accounts", setting="encrypted_s3_access", deny_plaintext_setting=True)
            self.s3_secret = self.get_setting_value(category="accounts", setting="encrypted_s3_secret", deny_plaintext_setting=True)
            self.s3_endpoint = self.get_setting_value(category="accounts", setting="encrypted_s3_endpoint", deny_plaintext_setting=True)
            self.s3_bucket = self.get_setting_value(category="accounts", setting="encrypted_s3_bucket", deny_plaintext_setting=True)

            ##### S3 SETUP
            self.storage = Storage(self.s3_access, self.s3_secret, self.s3_endpoint, self.s3_bucket)


            ##### GLOBAL MENTIONS
            local_global_mentions = self.get_setting_value(category="posting", setting="encrypted_global_mentions", deny_plaintext_setting=True)
            self.mention_tag_start = self.get_setting_value(category="posting", setting="encrypted_mention_tag_start", deny_plaintext_setting=True)
            self.mention_tag_end = self.get_setting_value(category="posting", setting="encrypted_mention_tag_end", deny_plaintext_setting=True)

            ## No Current Global Manager
            if local_global_mentions == "None": # No current setting, 

                ## Create new Global Mentions Manager
                self.global_mentions = global_mentions_manager()

                ## Write Manager to Settings
                self.set_setting_value(category="posting", setting="encrypted_global_mentions", value=pickle.dumps(self.global_mentions))
            
            ## If Setting is invalid
            elif not local_global_mentions:

                ## Couldn't Decrypt Setting
                self.global_mentions = None

            ## Setting Valid
            else:
                
                ## Load Global Mentions Manager Object
                self.global_mentions = pickle.loads(ast.literal_eval(local_global_mentions))

        else:
            self.media_accounts = None
            self.storage = None
        

        ##### APPLICATION
        self.no_posts_title = self.get_setting_value("app","no_posts_title")
        self.no_posts_description = self.get_setting_value("app","no_posts_description")
        self.post_not_scheduled_for_reason_time_in_past = self.get_setting_value("app","post_not_scheduled_for_reason_time_in_past")
        self.value_redaction_message = self.get_setting_value("app", "value_redaction_message")
        self.new_gid_mention_platform_message = self.get_setting_value("app", "new_gid_mention_platform_message")
        self.new_gid_mention_platform_id_message = self.get_setting_value("app", "new_gid_mention_platform_id_message")
        self.new_global_id_message = self.get_setting_value("app", "new_global_id_message")
        self.global_mentions_updated_message = self.get_setting_value("app", "global_mentions_updated_message")

        ##### PERFORMANCE
        self.posts_cache_time = float(self.get_setting_value("performance","encrypted_posts_cache_time"))
        self.page_cache_time = float(self.get_setting_value("performance","encrypted_page_cache_time"))

        ##### MEDIA
        self.supported_image_types = self.get_setting_value("media","encrypted_supported_image_types").split(",")
        self.supported_video_types = self.get_setting_value("media","encrypted_supported_video_types").split(",")
        self.supported_audio_types = self.get_setting_value("media","encrypted_supported_audio_types").split(",")

        ##### POSTING
        self.utc_timezones = self.get_setting_value("posting","encrypted_utc_timezones").split(",")
        self.default_timezone = self.get_setting_value("posting","encrypted_default_timezone")



    def reload_config(self):
        cfg.read(configpath)


    def read_encrypted_setting(self, setting_value):
        """
        Decrypts an input setting value. Does not read from file, you can input any encrypted value. 
        
        Rejects Plaintext & Failed Decryptions by returning None if input & output are the same. 
        """
        try:
            ## Decrypt 
            return self.crypt.decrypt(setting_value.encode()).decode()
        except Exception as e:
            ## Decryption Failed
            return None



    def set_setting_value(self, category, setting, value):
        try:
            value = self.crypt.encrypt(str(value).encode())
            self.set_setting_value(category, setting, value.decode())
            self.reload_config()
        except Exception as e:
            print(f"Exception while running set_encrypted_value: {str(e)}")
            return None

    ########## GET ALL SETTINGS CATEGORIES
    #####
    def get_all_setting_categories(self):
        return cfg.sections()

    

    ########## GET SETTING CATEGORY
    #####
    def get_setting_category(self, setting):
        """
        Returns the category of a setting
        """

        ## Initialize
        cat = None

        ## Look through Categories
        for category in self.get_all_setting_categories():

            ## Get options in Category 
            options = cfg.options(category)
        
            ## Look for match in category
            if setting in cfg.options(category):
                cat = category
                break
        
        ## Return
        return cat

        

    ########## GET ALL SETTINGS IN CATEGORY
    #####
    def get_all_settings_in_category(self,category):
        return cfg.options(category)



    ########## GET SETTING VALUE
    #####
    def get_setting_value(self,category=None,setting=None, auto_decrypt=True, deny_encrypted_setting=False, deny_plaintext_setting=False):

        ## If no setting provided, return None        
        if setting == None:
            return None

        ## If no category is specified, find it
        if category == None:
            category = self.get_setting_category(setting)
        
        ## Get setting value
        value = cfg.get(category,setting)

        ## Flag Initial Values
        if value == "None":
            return "None"

        ## Check if encrypted
        if setting.startswith("encrypted_"):

            ## Try to decrypt the value. If not none, it's encrypted. 
            decrypted_value = self.read_encrypted_setting(value)

            ## Valid encrypted setting
            if decrypted_value:

                ## Value encrypted when shouldn't be
                if deny_encrypted_setting == False:

                    ## Auto Decrypt
                    if auto_decrypt:
                        value = decrypted_value

                ## Deny Encrypted Setting if Found
                else:
                    return None
            
            ## If value is plaintext 
            else:

                ## Value already decrypted. Assuming tampering
                if deny_plaintext_setting==True:
                    return None

                ## Value already decrypted. Assuming default values
                else:
                    return value

        ## Deny Plaintext if Found
        elif deny_plaintext_setting:
            return None        
    
        return value



    ########## SET SETTING VALUE
    #####
    def set_setting_value(self,category=None,setting=None,value=None):

        ## If no setting provided, return None        
        if setting == None:
            return None

        ## If no category is specified, find it
        if category == None:
            category = self.get_setting_category(setting)

        ## Encrypt if encrypted (soon)
        if setting.startswith("encrypted_"):
            value = self.crypt.encrypt(str(value).encode()).decode()

        ## Set setting value
        cfg.set(category,setting,value)

        ## Write to config file
        with open(configpath, 'w') as configfile:
            cfg.write(configfile)

        ## Reload config
        self.reload_config()


    ########## CREATE NEW SETTING
    #####
    def create_new_setting(self,category,setting,value):
        cfg.add_section(category)
        cfg.set(category,setting,value)
        with open(configpath, 'w') as configfile:
            cfg.write(configfile)
        
        self.reload_config()
    

    ########## CREATE NEW CATEGORY
    #####
    def create_new_category(self,category):
        cfg.add_section(category)
        with open(configpath, 'w') as configfile:
            cfg.write(configfile)
        
        self.reload_config()


    ########## GET MEDIA ACCOUNTS WITH NAMES
    #####
    def get_media_accounts_with_names(self, names):
        
        accounts = []
        
        ## Loop through accounts and check for any that match the names provided
        for account in self.media_accounts:
            if account["name"] in names:
                accounts.append(account)
        
        return accounts

#
#
#class server_settings:
#    
#    def __init__(self):
#
#        
#
#
