#  _____                           _       
# |_   _|                         | |      
#   | | _ __ ___  _ __   ___  _ __| |_ ___ 
#   | || '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| || | | | | | |_) | (_) | |  | |_\__ \
#  \___/_| |_| |_| .__/ \___/|_|   \__|___/
#                | |                       
#                |_|                       
# -----------------------------------------------------------------------     



import pickle


#  _   _            _       _     _           
# | | | |          (_)     | |   | |          
# | | | | __ _ _ __ _  __ _| |__ | | ___  ___ 
# | | | |/ _` | '__| |/ _` | '_ \| |/ _ \/ __|
# \ \_/ / (_| | |  | | (_| | |_) | |  __/\__ \
#  \___/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/
# -----------------------------------------------------------------------     





#  _____ _                         
# /  __ \ |                        
# | /  \/ | __ _ ___ ___  ___  ___ 
# | |   | |/ _` / __/ __|/ _ \/ __|
# | \__/\ | (_| \__ \__ \  __/\__ \
#  \____/_|\__,_|___/___/\___||___/
# -----------------------------------------------------------------------   



########## GLOBAL MENTIONS MANAGER
#####
class global_mentions_manager:
    """
    Manager Class for Global Mentions
    """

    ########## INIT
    #####
    def __init__(self, entries=None):

        ## List of Global Mentions
        self.entries = [] if entries == None else entries



    ########## FIND GLOBAL MENTION INDEX
    #####
    def find_global_mention_index(self, global_mention_id):
        
        global_mentions = self.entries

        return_index = None

        for index, global_mention in enumerate(global_mentions):
            if global_mention.id == global_mention_id:
                return_index = index
                break

        return return_index



    ########## ADD GLOBAL MENTION
    #####
    def add_global_mention(self, global_mention):
        """
        Adds a Global Mention entry.
        """

        ## Ensure Unique
        if not self.find_global_mention_index(global_mention.id):

            ## Add new one
            self.entries.insert(0,global_mention)

            return True

        else:
            print("Attempted to add a duplicate global mention. Please check your input")
            return False



    ########## REMOVE GLOBAL MENTION
    #####
    def remove_global_mention(self, global_mention_id):
        """
        Removes a Global Mention entry.

        Args:
            id (str): The ID of the Global Mention to remove.
        """

        ## Get Mention Index
        mention_index = self.find_global_mention_index(global_mention_id)

        ## Remove mention
        del self.entries[mention_index]
            


    ########## RENAME GLOBAL MENTION
    #####
    def rename_global_mention(self, current_id, new_id):
        """
        Removes a Global Mention entry.

        Args:
            id (str): The ID of the Global Mention to remove.
        """

        ## Get Data from old mention
        global_mention_data = self.entries[self.find_global_mention_index(current_id)]

        ## Create new mention with that data
        new_global_mention = global_mention(new_id, global_mention_data)

        ## Remove old mention
        self.remove_global_mention(current_id)

        ## Add new one
        self.add_global_mention(new_global_mention)



    ########## UPDATE GLOBAL MENTION
    #####
    def update_global_mention(self, gID, global_mention):
        """
        Updates a Global Mention entry.

        Args:
            id (str): The ID of the Global Mention to update.
            global_mention (dict): The New Global Mention Data
        """

        ## Remove old mention
        self.remove_global_mention(gID)

        ## Add new one
        self.add_global_mention(global_mention)



    ########## DIFF
    #####
    def diff(self, global_mentions_manager_diff):
        """
        Checks for differences between input global mentions manager & self.

        Args: 
            Inputs
            global_mentions_manager_diff: The global mentions manager to diff against

            Outputs
            bool: Whether or not changes were found
        """

        try:

            ## If lengths are the same & both have entries, verify entry data
            if len(global_mentions_manager_diff.entries) == len(self.entries) and not len(self.entries) == 0:

                ## Look for changes
                for index, mention in enumerate(self.entries):

                    ## Changes found
                    if global_mentions_manager_diff.entries[index] != mention:
                        return True

                    ## No change found
                    else:
                        return False
                    
            ## Input has no entries
            else:
                ## User Cleared ALL Global Mentions
                return True

        except Exception as e:
            print(e)

    

    ########## EXPORT DATA
    #####
    def export_data(self):
        """
        Exports the Global Mention Data to a list of dictionaries.
        """

        global_mentions_data = []

        for global_mention in self.entries:
            global_mentions_data.append(global_mention.export_data())

        return global_mentions_data



    ########## SAVE
    #####
    def save(self):

        from resources.config import settings_core
        settings = settings_core()

        clone = global_mentions_manager(self.entries)

        pickled_clone = pickle.dumps(clone)

        ## Object Serialization for each global mention
        settings.set_setting_value(category="posting", setting="encrypted_global_mentions", value=pickled_clone)



########## GLOBAL MENTION
#####
class global_mention:
    """
    Global Mention class
    """

    ########## INIT
    #####
    def __init__(self, global_id, platform_mentions):

        self.id = global_id
        self.platform_mentions = platform_mentions



    ########## GET PLATFORM MENTION BY ID
    #####
    def get_platform_mention_by_id(self, platform_id):
        """
        Get platform mention by id
        """

        for index, platform_mention in enumerate(self.platform_mentions):
            if platform_mention[1] == platform_id:
                return platform_mention, index



    ########## GET PLATFORM ID AT INDEX
    #####
    def get_platform_id_at_index(self, index):
        """
        Gets the platform ID of the specified index
        """

        return self.platform_mentions[index][1]



    ########## GET PLATFORM AT INDEX
    #####
    def get_platform_at_index(self, index):
        """
        Gets the platform at the specified index
        """

        return self.platform_mentions[index][0]



    ########## ADD PLATFORM MENTION
    #####
    def get_registered_platforms(self):
        """
        Gets all registred platform names from platform mentions
        """

        return [item[0] for item in self.platform_mentions]
        


    ########## ADD PLATFORM MENTION
    #####
    def register_platform_check(self, platform, platform_id):
        """
        Ensures that platform registration submission meets requirements. 
        """

        from resources.config import settings_core
        settings = settings_core()

        ## Not Empty & Not Default Values
        if not platform == settings.new_gid_mention_platform_message or not platform_id == "" and not platform == settings.new_gid_mention_platform_id_message and not platform_id == "" :

            ## Platform not already registered 
            if not platform in self.get_registered_platforms():

                return True

        ## Default Values / Platform already registered
        return False



    ########## ADD PLATFORM MENTION
    #####
    def add_platform_mention(self, platform, platform_id):
        """
        Add platform mention
        """

        ## Check requirements
        if self.register_platform_check(platform, platform_id):

            ## Submit
            self.platform_mentions.insert(0, [platform, platform_id])

            ## Success
            return True
        else:
            ## Rejected
            return True


    ########## ADD PLATFORM MENTION
    #####
    def export_data(self):
        """
        Exports the Global Mention Data to a dictionary.
        """

        global_mention_data = {
            "id": self.id,
            "platform_mentions": self.platform_mentions
        }

        return global_mention_data