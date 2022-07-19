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
        return True



    ########## DISCONNECT FROM SOCIAL MEDIA PROVIDER
    #####
    def disconnect(self):
        """
        Disconnects from the social media provider.
        """
        return True



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
        
        published_posts = []
        errors = []

        ##### FOR EACH POST
        for post in post_objects:

            ## Publish
            r = self.publish_post(post)

            ## Validate Publishing
            if len(r) > post.get_num_scheduled_post_locations_for_account():

                ## Log
                published_posts.append(post)

            ## Debug
            else:
                errors.append(r.content)
                continue

        ## If all have been published return true, otherwise return false
        return published_posts
        



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
        return True




########## DISCORD
#####

class DiscordAccount(Account):
    """
    Class for Discord Account with connection, posting, and more functionality.

    Requires a unique name for an account that's already been registered.
    
    Child class of Account. Can only be used after Account is created / registered.
    """



    ########## INIT
    #####
    def __init__(self, account_unique_name):


        ## Call Parent Init
        super().__init__(name=account_unique_name)
        
        ## Load data
        self.load_data()



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
        was_published = False
        
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
            response_code = 0

            ## Validate & Log
            if r != None:

                ## Get Response
                response_code = int(re.sub("[^0-9^.]", "", str(r)))

                ## Determine Success
                was_published = True if response_code == 200 or response_code == 204 else False
 
            ## Success
            if was_published == True:
                
                ## Publish Data
                published_reference = json.loads(r.content)
                published_id = published_reference['id']

                # Debug
                print(f"Published Post @ id {published_id}")

            ## failed
            else:
                print(f"Webhook failed to post. Response Code <<{response_code}>>")

        final_data = {
            'ok': was_published,
            'id': published_id,
        }

        ## Return
        return final_data



    ########## DELETE POST
    #####
    def delete_posts(self, post_ids):
        """
        Deletes a number of posts based on IDs
        """
        pass



    ########## RETREIVE POST ANALYTICS
    #####
    def get_posts_analytics(self, post_ids):
        """
        Retreives analytics data for a post
        """
        
        pass





########## TELEGRAM
#####

class TelegramAccount(Account):
    """
    Class for Telegram Account with connection, posting, and more functionality.

    Requires a unique name for an account that's already been registered.
    
    Child class of Account. Can only be used after Account is created / registered.
    """


    ########## INIT
    #####
    def __init__(self, account_unique_name):

        ## Call Parent Init
        super().__init__(name=account_unique_name)

        ## Load data
        self.load_data()    
        


    ########## TG REQUEST
    #####
    def tg_request(self, endpoint, arguments={}):
        
        """
        Uses requests to interact with Telegram.
        
        Endpoints can be found here: https://core.telegram.org/bots/api

        Arguments are optional & should follow this format: {"ARG_Name":ARG_Data}
        """
        
        ## Retreive Bot Token
        bot_token = self.data['key']
        
        ## Build Initial Arguments String
        request_string = f"https://api.telegram.org/bot{bot_token}/{endpoint}"
        
        ## Add arguments if they exist
        if len(arguments) > 0:
            for index, argument in enumerate(arguments.keys()):
                
                ## Initial '?'
                if index == 0:
                    request_string = f"{request_string}?{argument}={str(arguments[argument])}"
                
                ## Sequential '&'
                else:
                    request_string = f"{request_string}&{argument}={str(arguments[argument])}"
        
        ## Send Request
        result = requests.get(request_string)
    
        ## Return result
        return result
    


    ########## FORMAT POST DATA
    #####
    def format_post_data(self, post_object):
        """
        Formats a post in a request format for a Telegram webhook
        """

        return post_object.description



    ########## BUILD MENTIONS LIST
    #####
    def build_mentions_list(self, post_content):
        """
        Used to build a list of mentions.
        """

        return None



    ########## REPLACE MENTIONS
    #####
    def replace_mentions(self, post_content, mentions_dict):
        """
        Replaces mentions in a post with the actual mention string.
        """
        
        return None



    ########## PUBLISH POST
    #####
    def publish_post(self, post_object):
        """
        Publishes a post from post object

        - Gets all data for post

        - Formats the data properly for this platform

        - Replaces mention IDs with their associated mention

        - Publishes the post
        """

        ## Get all the post locations that match this telegram account name
        locations_to_post = post_object.get_location_data_for_account(self.data['name']) 


        ## Initialize Variables
        all_posts_published = False
        published_reference = None
        was_published = False
        response_code = 0
        valid_result = False
        final_data = {'ok':"",'id':""}

        
        ## Post to all locations
        for location in locations_to_post:
            
            ###### FORMATTING
            # Format Post Data
            content = self.format_post_data(post_object) # Will eventually be dependant on location


            ##### PUBLISH
            r = self.tg_request("sendMessage", {"chat_id":location,"text":content})


            ##### ANALYSE
            ## Validate & Log
            if r != None:
                if r.ok:
                    # telegram logs @ chat_id/message_id

                    ## Load data
                    published_reference = json.loads(r.content)
                    message_id = published_reference['result']['message_id']
                    channel_id = published_reference['result']['chat']['id']
                    final_id = str(channel_id) + "://" + str(message_id)
                    
                    ## Format
                    final_data = {
                        'ok': True,
                        'id': final_id,
                    }
                    
                    ## Debug
                    print(f"Published Post @ id {final_id}")

                else:
                    print(f"Webhook failed to post. Response Code <<{response_code}>>")


        ## Return 
        return final_data



    ########## DELETE POST
    #####
    def delete_posts(self, post_ids):
        """
        Deletes a post on the platform.
        """
        pass



    ########## RETREIVE POST ANALYTICS
    #####
    def get_posts_analytics(self, post_ids):
        """
        Retreives analytics data for a post
        """
        pass
