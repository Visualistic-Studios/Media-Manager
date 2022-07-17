#  _____                           _       
# |_   _|                         | |      
#   | | _ __ ___  _ __   ___  _ __| |_ ___ 
#   | || '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| || | | | | | |_) | (_) | |  | |_\__ \
#  \___/_| |_| |_| .__/ \___/|_|   \__|___/
#                | |                       
#                |_|                       
# -----------------------------------------------------------------------   

import json
import requests
import re
from discord_webhook import DiscordWebhook


from resources.config import settings_core
from resources.utility import string_to_list_of_dictionaries




#  _   _            _       _     _           
# | | | |          (_)     | |   | |          
# | | | | __ _ _ __ _  __ _| |__ | | ___  ___ 
# | | | |/ _` | '__| |/ _` | '_ \| |/ _ \/ __|
# \ \_/ / (_| | |  | | (_| | |_) | |  __/\__ \
#  \___/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/
# -----------------------------------------------------------------------     


settings = settings_core()



#  _____ _                         
# /  __ \ |                        
# | /  \/ | __ _ ___ ___  ___  ___ 
# | |   | |/ _` / __/ __|/ _ \/ __|
# | \__/\ | (_| \__ \__ \  __/\__ \
#  \____/_|\__,_|___/___/\___||___/
# -----------------------------------------------------------------------   


########## ACCOUNT BASE CLASS
#####
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
        accounts = string_to_list_of_dictionaries(settings.get_setting_value("accounts", "encrypted_media_accounts"))

        for account in accounts:
            if account["name"] == self.data['name']:
                self.data = account
                data_loaded = True
                break
        
        posting_locations = self.data['posting_locations']
        
        self.posting_locations = posting_locations.split("|_|") if posting_locations != None else None
    
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
            settings.set_setting_value("accounts","encrypted_media_accounts",str(accounts))
        else:
            settings.set_setting_value("accounts","encrypted_media_accounts",str([data]))

        

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
        settings.set_setting_value("accounts","encrypted_media_accounts",str(accounts))

    
    
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
                settings.set_setting_value("accounts","encrypted_media_accounts",str(accounts))
            else:
                settings.set_setting_value("accounts","encrypted_media_accounts","None")
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



    ########## FORMAT POST DATA
    #####
    def format_post_data(self, post_object):
        """
        Formats a post object for posting to the social media provider.
        """
        raise NotImplementedError



    ########## BUILD MENTIONS LIST
    #####
    def build_mentions_list(self, post_content):
        """
        Used to build a list of mentions.
        """

        working_post_content = post_content.split(settings.mention_tag_end)

        mentions_list = []

        ## Find & extract mentions
        for entry in working_post_content:

            ## Find mention tag
            if settings.mention_tag_start in entry:

                ## Extract mention
                mention_name = entry.split(settings.mention_tag_start)[1]
                mentions_list.append(mention_name)

        return mentions_list


    
    ########## PUBLISH POST
    #####
    def publish_post(self, post_object):
        """
        Publishes a post
        """
        raise NotImplementedError



    ########## PUBLISH POSTS
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



    ########## FORMAT POST DATA
    #####
    def format_post_data(self, post_object):
        """
        Formats a post in a request format for a Discord webhook
        """

        ##### FORMAT POST CONTENT
        ## Temporary, need to implement user defined formatting rules. 
        ## Will also need to take into account the platforms message character limit. 
        ## Probably want to return a list of 'post data' for the publisher function to use. 

        if not post_object.title: 
            content = f"{post_object.description}"
        elif not post_object.description:
            content =  f"{post_object.title}"
        else:
            content = f"**{post_object.title}**\n\n{post_object.description}"
       
        return content


    ########## BUILD MENTIONS LIST
    #####
    def build_mentions_list(self, post_content):
        """
        Used to build a list of mentions.
        """

        mentions_list = Account.build_mentions_list(self, post_content)

        ## Return mentions list        
        return {"users": mentions_list}



    ########## REPLACE MENTIONS
    #####
    def replace_mentions(self, post_content, mentions_dict):
        """
        Replaces mentions in a post with the actual mention string.
        """
        
        ## Initialize mentions list
        mentions_list = mentions_dict['users']
        working_mentions_dict = {"users":[]}

        ## Replace all mentions with the proper formatting.
        for postmention in mentions_list: 

            ## Look for mention in global mentions
            mention_index = settings.global_mentions.find_global_mention_index(postmention)

            ## If global mention found
            if mention_index != None:     
                
                ## Get Global Mention object
                global_mention = settings.global_mentions.entries[mention_index]

                mention_id = global_mention.get_platform_id_by_name('discord')

                text_to_replace = f"{settings.mention_tag_start}{postmention}{settings.mention_tag_end}"

                ## Update Post Content
                post_content = post_content.replace(text_to_replace, f"<@&{mention_id}>")

                ## Update Mentions Dictionary
                working_mentions_dict['users'].append(mention_id)

        ## Return updated post content, updated mentions list
        return [post_content, working_mentions_dict]

        

    ########## PUBLISH POST
    #####
    def publish_post(self, post_object):
        ## Get all the post locations that match this discord account name
        locations_to_post = post_object.get_locations_for_account(self.data['name']) 

        ## Initialize Post Log
        all_posts_published = False
        published_reference = None
        
        ## Post to all discord webhook locations
        for location in locations_to_post:

            loc_data = {}

            ## Webhook URL
            url = post_object.get_url_from_post_location(location)
            if url:
                loc_data['url'] = post_object.get_url_from_post_location(location)
            
            ## Format the Post
            content = self.format_post_data(post_object) # Will eventually be dependant on location
            if content:
                loc_data['content'] = content

            ## Create proper Mentions
            mentions = self.build_mentions_list(loc_data['content'])

            if mentions:

                ## Update Post Content
                updated_mentions_data = self.replace_mentions(content, mentions)
                updated_post_content = updated_mentions_data[0]
                updated_mentions = updated_mentions_data[1]

                ## Log Updated Content
                loc_data['content'] = updated_post_content
                loc_data['allowed_mentions'] = updated_mentions
            
            ## Intialize the Webhook
            webhook = DiscordWebhook(**loc_data)

            ## Prepare Attachments
            files = post_object.get_decrypted_attachments()

            ## Add any attachments to webhook
            if files:
                for _file in files.values():
                    name = _file[0]
                    data = _file[1]
                    webhook.add_file(file=data, filename=name)

            ## Publish Webhook
            r = webhook.execute()

            ## Data
            was_published = False
            response_code = 0

            ## Validate & Log
            if r != None:

                ## Get Response
                response_code = int(re.sub("[^0-9^.]", "", str(r)))

                ## Determine Success
                was_published = True if response_code == 200 or response_code == 204 else False
 
            ## Analyse Results
            if was_published == True:
                published_reference = json.loads(r.content)
                print(f"Published Post @ id {published_reference['id']}")
            else:
                print(f"Webhook failed to post. Response Code <<{response_code}>>")

        ## Return
        return published_reference

    

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

            r = self.publish_post(post)

            ## If all attempted post locations are accounted for
            if len(r) > post.get_num_scheduled_post_locations_for_account():
                # for link in r.['successful_posts']:
                    # post.add_published_link(link)

                ## Log post
                published_posts.append(post)
            else:
                errors.append(r.content)
                continue

        ## If all have been published return true, otherwise return false
        return published_posts



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









