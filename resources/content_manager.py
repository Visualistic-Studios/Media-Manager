
#  _____                           _       
# |_   _|                         | |      
#   | | _ __ ___  _ __   ___  _ __| |_ ___ 
#   | || '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| || | | | | | |_) | (_) | |  | |_\__ \
#  \___/_| |_| |_| .__/ \___/|_|   \__|___/
#                | |                       
#                |_|                       
# -----------------------------------------------------------------------     


from resources.accounts import DiscordAccount
from resources.config import settings_core
from resources.database import Storage


#  _   _            _       _     _           
# | | | |          (_)     | |   | |          
# | | | | __ _ _ __ _  __ _| |__ | | ___  ___ 
# | | | |/ _` | '__| |/ _` | '_ \| |/ _ \/ __|
# \ \_/ / (_| | |  | | (_| | |_) | |  __/\__ \
#  \___/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/
# -----------------------------------------------------------------------      


settings = settings_core()
storage = Storage(settings.s3_access, settings.s3_secret, settings.s3_endpoint, settings.s3_bucket)



#  _____ _                         
# /  __ \ |                        
# | /  \/ | __ _ ___ ___  ___  ___ 
# | |   | |/ _` / __/ __|/ _ \/ __|
# | \__/\ | (_| \__ \__ \  __/\__ \
#  \____/_|\__,_|___/___/\___||___/
# -----------------------------------------------------------------------   


########## CONTENT MANAGER
#####
class ContentManager:

    ##### INIT
    def __init__(self):

        print('Account Manager started')


    ########### PUBLISH POSTS
    #####
    def publish_posts(self, post_objects, account_names, media_connections):

        ## Initialize List
        published_posts = []

        ## Loop through all posts to publish
        for post in post_objects:

            ## Get Account Name & Verify It
            for account_name in account_names:
                if account_name in media_connections.keys():

                    ## Publish Post
                    published_post = media_connections[account_name].publish_post(post)

                    ## Validate Published Post
                    if published_post:

                        ## Save as Published
                        was_saved_as_published = post.save_as_published()

                        ## Remove from Scheduled
                        was_removed_from_scheduled = post.remove_from_scheduled()

                        ## Log if Successful
                        if was_saved_as_published == True & was_removed_from_scheduled == True:
                            published_posts.append(post)


    ########## GET UNIQUE ACCOUNT NAMES FROM POST OBJECTS
    #####
    def get_unique_account_names_from_post_objects(self, post_objects):

        requested_account_names_to_post_to = []

        ## Find all accounts needed for post
        for post in post_objects:
            for account in post.accounts_to_post_to:  

                ## Ensure unique
                if account not in requested_account_names_to_post_to: 

                    ## Store the account name
                    requested_account_names_to_post_to.append(account)

        return requested_account_names_to_post_to


    ########## GET ACCOUNT CONNECTIONS
    #####
    def get_account_connections(self, accounts):
        """
        Creates Account Classes for the input Accounts & Connects them. 

        Returns Successful Connections ([0]) & Failed Connections ([1])
        """

        ## For logging accounts that connect
        connected_accounts = {}
        ## For logging any accounts that don't connect. 
        failed_accounts = []
    
        ## Loop on Each Account
        for account in accounts:

            ## Initialize Connection Status
            account_connected = False

            ## Get Platform Name
            platform = account['media_platform'].lower()

            ##### ACCOUNT TYPES
            # Probably a better way to do this. Could have all account types held in an array with a class reference. 

            ##### Discord
            if platform=='discord':
                account_obj = DiscordAccount(account['name'])
                if account_obj:
                    connected_accounts[account['name']] = account_obj
            else:
                pass

            ##### CREATE & STORE ACCOUNT CONNECTION
            try:
                ## Connect
                connected_accounts[account['name']].connect()
            
                ## Verify Connection
                if connected_accounts[account['name']].is_ready():

                    ## Connection Succeeded
                    account_connected = True

            ## Connection Failed
            except Exception as e:
                print('Could not connect to social media account ' + account['name'] + '\n' + str(e))

            ## Remove Account from list to post if Connection Failed
            if not account_connected:
                failed_accounts.append(account)

        return connected_accounts, failed_accounts



    ########### PROCESS PENDING POSTS
    #####
    def close_connections(self, accounts):
        """
        Closes Account Connections
        """

        ## Needs better handling for accounts that don't get disconnected

        ## Close Connections
        for account_name in accounts.keys():
            try:
                accounts[account_name].disconnect()
            except Exception as e:
                print('Could not disconnect from social media account ' + account_name)
                print(e)

        



    ########### PROCESS PENDING POSTS
    #####
    def process_pending_posts(self, post_objects):
        """
        Processes a list of posts. Requires a list of post objects.
        """

        ##### RETURN IF EMPTY
        if not post_objects:
            print("No pending posts for process_pending_posts")
            return None


        ## List of connections to be closed later
        media_connections = {} 

        ## Get Account Names
        requested_account_names_to_post_to = self.get_unique_account_names_from_post_objects(post_objects)

        ## Get Account Data
        requested_accounts_data_to_post_to = settings.get_media_accounts_with_names(requested_account_names_to_post_to)  

        ## Get Media Connections
        media_connections = self.get_account_connections(requested_accounts_data_to_post_to)[0]
        
        ## Publish Posts
        published_posts = self.publish_posts(post_objects, requested_account_names_to_post_to, media_connections)

        ## Close Connections
        self.close_connections(media_connections)

        ## Return the list of posts that have been published
        return published_posts
        
    
    ########## GET POSTS WITH ACCOUNT NAME
    #####   
    def get_posts_with_account_name(self, account_name, post_objects):
        """
        Gets all posts with a specific account name.
        """

        posts = []

        for post in post_objects:
            if account_name in post.accounts_to_post_to:
                posts.append(post)

        return 