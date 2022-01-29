
from resources.config import settings_core
from resources.utility import string_to_list_of_dictionaries

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




# Class for managing multiple accounts at once / posting. 
class AccountManager:
    def __init__(self):
        self.accounts = []
        print('Account Manager started')
