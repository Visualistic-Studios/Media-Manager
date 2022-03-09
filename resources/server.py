#  _____                           _       
# |_   _|                         | |      
#   | | _ __ ___  _ __   ___  _ __| |_ ___ 
#   | || '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| || | | | | | |_) | (_) | |  | |_\__ \
#  \___/_| |_| |_| .__/ \___/|_|   \__|___/
#                | |                       
#                |_|                       
# -----------------------------------------------------------------------     

from resources.posts import get_all_scheduled_posts, get_all_published_posts
from resources.content_manager import ContentManager


#  _____ _                         
# /  __ \ |                        
# | /  \/ | __ _ ___ ___  ___  ___ 
# | |   | |/ _` / __/ __|/ _ \/ __|
# | \__/\ | (_| \__ \__ \  __/\__ \
#  \____/_|\__,_|___/___/\___||___/
# -----------------------------------------------------------------------   


########## SERVER CLASS
#####
class mm_server:

    """
    The server class abstracts functionality for handling scheduled & published posts.
    """

    ########## INIT
    #####
    def __init__(self):
        self.content_manager = ContentManager()
        pass


    
    ########## LOAD SCHEDULED POSTS
    #####
    def load_scheduled_posts(self):
        """
        Loads all scheduled posts from the database.
        """

        return get_all_scheduled_posts()



    ########## LOAD PUBLISHED POSTS
    #####
    def load_published_posts(self):
        """
        Loads all published posts from the database.
        """
        
        return get_all_published_posts()

  

    ########## GET READY TO PUBLISH POSTS
    #####
    def get_ready_to_publish_posts(self):
        """
        Returns a list of posts that are ready to be published. 
        
        Does this by loading scheduled posts from `get_all_scheduled_posts` & comparing the scheduled time to the current time for each post.
        """

        posts = self.load_scheduled_posts()
        ready_posts = []

        for post in posts:
            ## Get Current Time in the same timezone as the post
            current_time = post.get_current_time_in_timezone()

            ## Check if the current time is greater than the scheduled time
            if post.datetime_to_post <= current_time:
                ready_posts.append(post)
            else:
                pass

        return ready_posts
        


    ########## PROCESS PENDING SCHEDULED POSTS
    #####
    def process_pending_scheduled_posts(self):
        """
        Processes all scheduled posts that are currently pending.
        """

        ##### PROCESS PENDING POSTS
        published_posts = self.content_manager.process_pending_posts(self.get_ready_to_publish_posts())
        if published_posts:
            for post in published_posts:
                post = post[0]
                post.remove_from_scheduled()
                post.save_as_published()



