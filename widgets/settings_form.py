import pandas as pd
import streamlit as st
from resources.config import settings_core
from resources.accounts import Account

settings = settings_core()


#   ___              _ _           _   _             
#  / _ \            | (_)         | | (_)            
# / /_\ \_ __  _ __ | |_  ___ __ _| |_ _  ___  _ __  
# |  _  | '_ \| '_ \| | |/ __/ _` | __| |/ _ \| '_ \ 
# | | | | |_) | |_) | | | (_| (_| | |_| | (_) | | | |
# \_| |_/ .__/| .__/|_|_|\___\__,_|\__|_|\___/|_| |_|
#       | |   | |                                    
#       |_|   |_|                                    
# ----------------------------------------------------------------------- 

# Settings Form Widget


########## APPLICATION
#####
def app():

    ## Initialize
    sections = settings.get_all_setting_categories()
    setting_buttons_dict = {}
    new_account = {}
    setting_display_names = {}

    ## Main Settings Form
    with st.form("Settings"):

        ## Create Sections from Categories
        for section in sections:   
                if not section == "server":

                    ## Create Section
                    st.markdown("#### " + section.capitalize())

                    ## Log Settings
                    settings_in_category = settings.get_all_settings_in_category(section)

                    ## Create Settings Buttons
                    for setting in settings_in_category:


                        ########## DISPLAY NAMES
                        #####
                        if setting.lower().startswith("display_name_"):

                            ## Get Associated Setting
                            setting_name = setting.replace("display_name_", "")

                            ## Log Display Name
                            setting_display_names[setting_name] = [settings.get_setting_value(section, setting), section]



                        ########## MEDIA ACCOUNTS
                        #####
                        elif setting == "media_accounts": 

                            ## Initialize
                            media_accounts = settings.media_accounts 
                            media_account_button_list = []
                            if media_accounts != None:
                                st.markdown("**Media accounts**")


                                ## Load data for each account
                                for media_account in media_accounts:
                                    media_account_button_dict = {}
                                    media_display_name = media_account["display_name"]
                                    media_account_name = media_account["name"]
                                    media_account_key = media_account["key"]
                                    media_account_secret = media_account["secret"]
                                    media_account_access_key = media_account["access_key"]
                                    media_account_access_secret = media_account["access_secret"]
                                    media_account_media_platform = media_account["media_platform"]
                                    media_account_posting_locations = media_account["posting_locations"].split("|_|")
        
                                    
                                    ## Create a button for each account and add it to a dropdown
                                    with st.expander(media_display_name):
                                        media_account_button_dict['request_removal'] = st.checkbox("Remove", key=f"Remove_{media_account_name}")
                                        media_account_button_dict["display_name"] = st.text_input("Display name", media_display_name)
                                        media_account_button_dict['key'] = st.text_input(f"Key",f"{media_account_key}", None, media_account["name"], 'password')
                                        media_account_button_dict['secret'] = st.text_input(f"Secret",f"{media_account_secret}", None, media_account["name"], 'password')  
                                        media_account_button_dict['access_key'] = st.text_input(f"Access Key",f"{media_account_access_key}", None, media_account["name"], 'password')
                                        media_account_button_dict['access_secret'] = st.text_input(f"Access Secret",f"{media_account_access_secret}", None, media_account["name"], 'password')
                                        media_account_button_dict['posting_locations'] = st.multiselect(f"Posting Locations",media_account_posting_locations,default=media_account_posting_locations, key=f"Posting Locations_{media_account_name}")
                                        media_account_button_dict['new_posting_locations'] = st.text_input(f"Add New Posting Locations", "", key=f"new_posting_locations_{media_account['name']}",placeholder="Location 1|Location 2|Location 3").split("|")
        
                                        ## Find the right multiselection for media platform
                                        media_platforms_df = pd.DataFrame(settings.supported_media_platforms)
                                        media_selected_index = 0   

                                        for index, platform in enumerate(settings.supported_media_platforms):
                                            if str(platform) == str(media_account_media_platform):
                                                media_selected_index = index

                                        ## Create 3 options in a select box
                                        media_account_button_dict['media_platform'] = st.selectbox("Media platform", media_platforms_df,index = media_selected_index, key=media_account["name"])
                                        media_account_button_dict['name'] = media_account_name
                                        media_account_button_list.append(media_account_button_dict)

                            else:
                                st.text("No media accounts added")

                            ## Add New Media Account
                            with st.expander("Register New Account"):
                                new_account["name"] = st.text_input("Unique name", placeholder="unique-name", key="new_account_name") 
                                new_account["display_name"] = st.text_input("Display name", placeholder="Display Name | Work",key="new_account_display_name")
                                new_account['key'] = st.text_input(f"Key", placeholder="", key='key_new_account', type='password')
                                new_account['secret'] = st.text_input(f"Secret", key='secret_new_account', type='password')  
                                new_account['access_key'] = st.text_input(f"Access Key", key='access_key_new_account', type='password')
                                new_account['access_secret'] = st.text_input(f"Access Secret", key='access_secret_new_account', type='password')
                                new_account['posting_locations'] = st.text_input(f"Posting Locations", placeholder="Location 1|Location 2|Location 3", key='posting_locations_new_account').split("|")


                                ## Find the right multiselection for media platform
                                media_platforms_df = pd.DataFrame(settings.supported_media_platforms)
                                media_selected_index = 0 


                                # create 3 options in a select box
                                new_account['media_platform'] = st.selectbox("Media platform", media_platforms_df,index = media_selected_index, key=new_account["name"])



                        # ########## GLOBAL MENTION IDs
                        # #####
                        # elif setting == "global_mention_ids":

                        #     ## Needs to be a dropdown similar to accounts. The dropdown will have the global user friendly name (the one used in posts & such) 
                        #     ## Below it will have a list of inputs. Platform Name | Platform ID

                        #     setting_buttons_dict[setting] = [st.text_input(f"Global Mention IDs", value=settings.global_mention_ids, key='global_mention_ids', type='password')]



                        ########## REGULAR SETTINGS
                        #####
                        else:
                            
                            ## Define Setting Type (Default/Hidden)
                            setting_type = "password" if setting.lower().startswith("hidden_") else "default"

                            ## Retrieve Display Name
                            display_name = setting_display_names[setting][0] if setting in setting_display_names.keys() else setting

                            ## Retrieve Value
                            value = settings.get_setting_value(section, setting)
                            
                            ## Create a button & log it + the section
                            setting_buttons_dict[setting] = [st.text_input(label=display_name, value=value, key=setting, type=setting_type), section]

                        

        ########## SUBMIT BUTTON
        #####
        submitted = st.form_submit_button("Submit", section)
        if submitted:  

            ## Section Title
            with st.expander("Settings Saved"):

                ########## UPDATE SETTINGS
                #####
                for section2 in sections:

                    ####### INITIALIZE
                    ## Get Settings of Category
                    settings_in_category = settings.get_all_settings_in_category(section2)
                    for setting in settings_in_category:

                        ## Ignorees
                        if setting.lower().startswith("display_name_") or str(setting) == "media_accounts":
                            continue

                        ## Initialize Valid Settings
                        if setting in setting_buttons_dict:
                        
                            setting_ref = setting_buttons_dict[setting]
                            setting_button = setting_ref[0]
                            setting_details = setting_ref[1]
                            setting_category = setting_details[0]

                        ## Look for changes
                        if str(setting_button) != str(settings.get_setting_value(section2, setting)):
                            
                            ## Redact Hidden Setting Values before showing them to user. 
                            setting_response = settings.value_redaction_message if setting.startswith("hidden_") else setting_button

                            ## Notify User through of changes
                            st.markdown(setting + ": " + f"`{setting_response}`")
                                
                            ## Update Setting Value
                            settings.set_setting_value(section2, setting, setting_button)


                ########## UPDATE EXISTING ACCOUNTS
                #####
                try:

                    ## Format Button Data
                    for button in media_account_button_list:

                        ## Initialize Button Data
                        button_data = {"display_name": button["display_name"],"name": button["name"],"key": button["key"],"secret": button["secret"],"access_key": button["access_key"],"access_secret": button["access_secret"],"media_platform": button["media_platform"],"posting_locations": button["posting_locations"]}


                        ########## REQUEST REMOVE ACCOUNT
                        ## Get Reference of Request Removal Button
                        button_request_removal  = button["request_removal"]

                        ## Remove Account if Requested
                        if button_request_removal==True:

                            ## Create Account Object
                            account_to_update = Account(name=button_data["name"])

                            ## Remove Account
                            account_to_update.remove()

                            ## Logß
                            st.success(f"Account {button_data['name']} removed.")

                        ## Register Changed Settings
                        found_difference = False
                        for account in settings.media_accounts:
                            if account['name'] == button["name"]:
                                # compare all data and break if there is a difference
                                for key in button_data:
                                    if str(button_data[key]) != str(account[key]):
                                        found_difference = True
                                        st.markdown(button['name'] + ": " + f"`Setting {key} has changed`")

                        ## Get Reference of New Post Location 
                        new_posting_locations = button["new_posting_locations"]

                        ## Take care of empty button
                        if len(new_posting_locations)==1 and new_posting_locations[0] == "":
                            new_posting_locations = []


                        ## Look for changes in account details, update the settings file if found
                        elif found_difference or len(new_posting_locations) != 0:
                            account_to_update = Account(name=button_data["name"])
                            account_to_update.load_data()

                            ## Append new posting locations to the account if found
                            if len(new_posting_locations) != 0:
                                for new_posting_location in new_posting_locations:
                                    if new_posting_location !="":
                                        button_data['posting_locations'].append(new_posting_location)
                                        st.success("Added new posting location: " + new_posting_location)

                            ## Update the account
                            account_to_update.update(display_name=button_data["display_name"], key=button_data["key"], secret=button_data["secret"], access_key=button_data["access_key"], access_secret=button_data["access_secret"], media_platform=button_data["media_platform"], posting_locations=button_data["posting_locations"])


                            st.success(f"Please Restart the Application & Refresh the page")
                            
                except Exception as e:
                    pass
                

                ########## CREATE NEW ACCOUNT
                #####
                try:
                    if new_account['name'] != "":
                        account_to_add = Account(name=new_account['name'])
                        account_to_add.register(display_name=new_account['display_name'], key=new_account['key'], secret=new_account['secret'], access_key=new_account['access_key'], access_secret=new_account['access_secret'], media_platform=new_account['media_platform'], posting_locations=new_account['posting_locations'])
                        st.success("Account added. Please Restart the Application & Refresh the page")

                except Exception as e:
                    print(e)