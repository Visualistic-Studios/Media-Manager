
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

#  _____ _                         
# /  __ \ |                        
# | /  \/ | __ _ ___ ___  ___  ___ 
# | |   | |/ _` / __/ __|/ _ \/ __|
# | \__/\ | (_| \__ \__ \  __/\__ \
#  \____/_|\__,_|___/___/\___||___/
# -----------------------------------------------------------------------   


settings = settings_core()
storage = Storage(settings.s3_access, settings.s3_secret, settings.s3_endpoint, settings.s3_bucket)




########## CONTENT MANAGER
#####
class ContentManager:

    ##### INIT
    def __init__(self):

        print('Account Manager started')
        


    ########### PROCESS PENDING POSTS
    #####
    def process_pending_posts(self, post_objects):
        """
        Processes a list of posts. Requires a list of post objects.
        """

        if not post_objects:
            print("No pending posts for process_pending_posts")
            return None

            


        ## List of connections to be closed later
        media_connections = {}

        ## Loop through all posts to create a list of all unique accounts that have been requested to post to
        requested_accounts_data_to_post_to = []
        requested_account_names_to_post_to = []


        ##### GET A UNIQUE LIST OF ACCOUNTS TO POST TO
        ## Find any unique names
        for post in post_objects:
            for account in post.accounts_to_post_to:
                if account not in requested_account_names_to_post_to:

                    ## Store the account name
                    requested_account_names_to_post_to.append(account)


        ##### CREATE & STORE CONNECTIONS
        ## Get Account Data        
        requested_accounts_data_to_post_to = settings.get_media_accounts_with_names(requested_account_names_to_post_to)  

        for account in requested_accounts_data_to_post_to:

            ## Find Platform Name
            platform = account['media_platform'].lower()


            ##### CREATE ACCOUNT OBJECT
            ## Discord
            if platform=='discord':
                account_obj = DiscordAccount(account['name'])
                if account_obj:
                    media_connections[account['name']] = account_obj
            else:
                pass


            ##### CONNECT TO ACCOUNT 
            ## Connect to Social Media & Check if ready 
            try:

                ## Connect
                media_connections[account['name']].connect()
                

                ## Check if connected
                if media_connections[account['name']].is_ready():
                    account_connected = True
                else:
                    account_connected = False


            except Exception as e:
                print('Could not connect to social media account ' + account['name'])
                print(e)
                
                account_connected = False   

            ###### REMOVE & SKIP IF NOT CONNECTED
            if not account_connected:
                
                ## Remove account from temp data
                requested_accounts_data_to_post_to.remove(account)
                del media_connections[account['name']]
        
        

        ##### PUBLISH POSTS

        published_posts = []

        ## Loop through all posts to publish
        for post in post_objects:
            for account_name in requested_account_names_to_post_to:

                ## Publish Post
                if account_name in media_connections.keys():

                    ## Add the post to the list of posts that have been published
                    post_ref = media_connections[account_name].publish_posts([post])
                    if post_ref:
                        published_posts.append(post_ref)


        ##### CLOSE CONNECTIONS
        for account_name in media_connections.keys():
            try:
                media_connections[account_name].disconnect()
            except Exception as e:
             
                print('Could not disconnect from social media account ' + account_name)
                print(e)


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



