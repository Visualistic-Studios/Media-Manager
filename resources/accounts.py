
from resources.config import settings_core
from resources.utility import string_to_list_of_dictionaries
from io import BytesIO

import json
import requests

settings = settings_core()

########## ACCOUNT CLASS

class Account:

    ########## INIT
    #####
    def __init__(self, display_name=None, name=None, key=None, secret=None, access_key=None, access_secret=None, media_platform=None, posting_locations=None):
        self.data = {
            "display_name": display_name,
            "name": name,
            "key": key,
            "secret": secret,
            "access_key": access_key,
            "access_secret": access_secret,
            "media_platform": media_platform,
            "posting_locations": posting_locations
        }

        self.posting_locations = None

    ########## LOAD DATA
    #####
    def load_data(self):
        data_loaded = False

        ## Load Account Data from Settings
        accounts = string_to_list_of_dictionaries(settings.read_encrypted_setting("accounts", "media_accounts"))

        for account in accounts:
            if account["name"] == self.data['name']:
                self.data = account
                data_loaded = True
                break
        
        self.posting_locations = self.data['posting_locations'].split("|_|")
        

        return data_loaded
        

    ########## DATA TO LIST
    #####
    def data_to_list(self,data):

        display_name = data["display_name"]
        name = data["name"]
        key = data["key"]
        secret = data["secret"]
        access_key = data["access_key"]
        access_secret = data["access_secret"]
        media_platform = data["media_platform"]
        posting_locations = data["posting_locations"].replace(",", "|_|")

        return f"{display_name}|-|{name}|-|{key}|-|{secret}|-|{access_key}|-|{access_secret}|-|{media_platform}|-|{posting_locations}"

    ########## POSTING LOCATION TO STRING
    #####
    def posting_location_to_string(self, posting_locations):
        
        posting_locations_string = ""

        if posting_locations[-1].strip(" ") == "":
            del posting_locations[-1]

        for index, loc in enumerate(posting_locations):
            if index == len(posting_locations) - 1 and not loc.strip(" ")=="":
                posting_locations_string += loc
            elif not loc.strip(" ")=="":
                posting_locations_string += loc + "|_|"

        return posting_locations_string


    ########## REGISTER
    #####
    def register(self, display_name, key, secret, access_key=None, access_secret=None, media_platform=None, posting_locations=None):

        data = {
            "display_name": display_name,
            "name": self.data['name'],
            "key": key,
            "secret": secret,
            "access_key": access_key,
            "access_secret": access_secret,
            "media_platform": media_platform,
            "posting_locations": self.posting_location_to_string(posting_locations)
        }

        accounts = settings.media_accounts
        if accounts:
            accounts.append(data)
            # save new accounts
            settings.write_encrypted_setting("accounts","media_accounts",str(accounts))
        else:
            settings.write_encrypted_setting("accounts","media_accounts",str([data]))

        

    ########## UPDATE
    #####
    def update(self, display_name=None, key=None, secret=None, access_key=None, access_secret=None, media_platform=None, posting_locations=None):
        # get current accounts and add new one
        accounts = settings.media_accounts
        for account in accounts:
            if account["name"] == self.data['name']:
                account["display_name"] = display_name
                account["key"] = key
                account["secret"] = secret
                account["access_key"] = access_key
                account["access_secret"] = access_secret
                account["media_platform"] = media_platform
                account["posting_locations"] = self.posting_location_to_string(posting_locations)
                break
        # save new accounts
        settings.write_encrypted_setting("accounts","media_accounts",str(accounts))

    
    ########## REMOVE
    #####
    def remove(self):
        """
        Remove Account from Data. Requires the account name is set.
        """
        try:
            # Get accounts from settings and loop to find the account to remove
            accounts = settings.media_accounts
            for account in accounts:
                if account['name'] == self.data['name']:
                    accounts.remove(account)
                    break

            ## Save New Accounts
            if len(accounts) > 0:
                settings.write_encrypted_setting("accounts","media_accounts",str(accounts))
            else:
                settings.set_setting_value("accounts","media_accounts","None")
            print('account removed')

            return True
            
        except Exception as e:
            print(e)
            return False

    
    ########## CONNECT TO SOCIAL MEDIA PROVIDER
    #####
    def connect(self):
        """
        Creates a connection to the social media provider.
        """
        raise NotImplementedError


    ########## DISCONNECT FROM SOCIAL MEDIA PROVIDER
    #####
    def disconnect(self):
        """
        Disconnects from the social media provider.
        """
        raise NotImplementedError


    ########## CREATE POST
    #####
    def publish_posts(self, post_object):
        """
        Creates a post from post object.
        """
        raise NotImplementedError


    ########## DELETE POST
    #####
    def delete_posts(self, post_id):
        """
        Deletes a post from the platform & cleans up the database. Will no longer be available for analytics
        """
        ## Parent function here will clean up the database & associated files
        pass

    ########## IS READY
    #####
    def is_ready(self):
        """
        Checks if the account is ready to be used.
        """
        raise NotImplementedError




########## DISCORD
#####

class DiscordAccount(Account):
    """
    Class for Discord Account with connection, posting, and more functionality.

    Requires a unique name for an account that's already been registered.
    
    Child class of Account. Can only be used after Account is created / registered."""



    ########## INIT
    #####
    def __init__(self, account_unique_name):


        ## Call Parent Init
        super().__init__(name=account_unique_name)

        self.load_data()



    ########## CONNECT
    #####
    def connect(self):
        """
        Doesn't do anything in this case, Discord accounts use a simple webhook. 
        """

        return True



    ########## DISCONNECT
    #####
    def disconnect(self):
        """
        Doesn't do anything in this case, Discord accounts use a simple webhook. 
        """

        return True

        

    ########## CREATE POST
    #####
    def publish_posts(self, post_objects):
        """
        Creates a post from post object.
        """

        published_posts = []
        errors = []

        ##### FOR EACH POST
        for post in post_objects:

            ## Get all the post locations that match this discord account name
            locations_to_post = post.get_locations_for_account(self.data['name']) 
            
            ## Post to all discord webhook locations
            for location in locations_to_post:

                data = {'content': f"**{post.title}**\n\n```{post.description}```"}


                ##### PREPARE ATTACHMENTS
                files = None

                if post.attachments:
                    files={}
                    for index, f in enumerate(post.load_attachments()):

                        # ## Decrypt File
                        file_final = BytesIO()
                        settings.crypt.decrypt_stream(f, file_final)
                        file_final.seek(0)

                        ## Set Filename
                        file_name = f.full_name.split("/")[-1]

                        ## Add to an array for later
                        files[f"file{index+1}"] = (file_name, file_final)

                ## Get the webhook url from the location
                split_location = location.split("://")
                webhook_url = split_location[1] + "://" + split_location[2]
                

                ##### PUBLISH THE POST
                if files:
                    r = requests.post(webhook_url, data=data, files=files, stream=True)
                else:
                    r = requests.post(webhook_url, data=data)
                

                ##### LOG SUCCESSFUL POSTS
                if r:
                    published_posts.append(post)
                else:
                    errors.append(r.content)
                    continue

        ## If all have been published return true, otherwise return false
        if len(published_posts) == len(post_objects):
            return True
        else:
            print(errors)
            return False



    ##### DELETE POST
    def delete_posts(self, post_ids):
        # do whatever discord needs to to delete the post
        pass


    ##### RETREIVE POST ANALYTICS
    def get_posts_analytics(self, post_ids):
        # do whatever discord needs to to get the post analytics
        pass


    ##### IS READY
    def is_ready(self):
        return True









