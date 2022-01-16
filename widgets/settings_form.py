import pandas as pd
import streamlit as st
from resources.config import settings_core
from resources.accounts import AccountManager, Account
from resources.utility import string_to_list_of_dictionaries


settings = settings_core()
AccountManager = AccountManager()

def app():

    ##### LOAD SETTINGS FILE AND FIND SECTIONS
    settings_file = open(settings.current_path + "settings.cfg", "r")
    sections = settings.get_all_setting_categories()
    setting_buttons_dict = {}
    new_account = {}

    ##### SETTINGS FORM
    with st.form("Settings"):

        for section in sections:   

                ##### TITLE
                st.markdown("#### " + section.capitalize())
                settings_in_category = settings.get_all_settings_in_category(section)

                for setting in settings_in_category:

                    if setting != "media_accounts":
                        ## Create a button for each setting and add it to a dictionairy 
                        setting_buttons_dict[setting] = st.text_input(setting, settings.get_setting_value(section, setting))
                    
                    else:
                        ##### MEDIAS
                        media_accounts = settings.media_accounts#settings.get_setting_value(section, setting)
                        media_account_button_list = []

                        if media_accounts != None:

                            st.markdown("**Media accounts**")

                            ## Create a new account section for each account
                            for media_account in media_accounts:
                                media_account_button_dict = {}
                                media_display_name = media_account["display_name"]
                                media_account_name = media_account["name"]
                                media_account_key = media_account["key"]
                                media_account_secret = media_account["secret"]
                                media_account_access_key = media_account["access_key"]
                                media_account_access_secret = media_account["access_secret"]
                                media_account_media_platform = media_account["media_platform"]
    

                                with st.expander(media_display_name):
                                    media_account_button_dict['request_removal'] = st.checkbox("Remove")
                                    media_account_button_dict["display_name"] = st.text_input("Display name", media_display_name)
                                    media_account_button_dict['key'] = st.text_input(f"Key",f"{media_account_key}", None, media_account["name"], 'password')
                                    media_account_button_dict['secret'] = st.text_input(f"Secret",f"{media_account_secret}", None, media_account["name"], 'password')  
                                    media_account_button_dict['access_key'] = st.text_input(f"Access Key",f"{media_account_access_key}", None, media_account["name"], 'password')
                                    media_account_button_dict['access_secret'] = st.text_input(f"Access Secret",f"{media_account_access_secret}", None, media_account["name"], 'password')
     
                                    ## Find the right multiselection for media platform
                                    media_platforms_df = pd.DataFrame(settings.supported_media_platforms)
                                    media_selected_index = 0   

                                    for index, platform in enumerate(settings.supported_media_platforms):
                                        if str(platform) == str(media_account_media_platform):
                                            media_selected_index = index

                                    # create 3 options in a select box
                                    media_account_button_dict['media_platform'] = st.selectbox("Media platform", media_platforms_df,index = media_selected_index, key=media_account["name"])
                                    media_account_button_dict['name'] = media_account_name
                                    media_account_button_list.append(media_account_button_dict)

                                                # when a button is pressed create an expander



                        else:
                            st.text("No media accounts added")

                        with st.expander("Register New Account"):
                            new_account["name"] = st.text_input("Unique name", "", None,key="new_account_name") 
                            new_account["display_name"] = st.text_input("Display name", "", None, key="new_account_display_name")
                            new_account['key'] = st.text_input(f"Key",f"", None, new_account["name"], 'password')
                            new_account['secret'] = st.text_input(f"Secret",f"", None, new_account["name"], 'password')  
                            new_account['access_key'] = st.text_input(f"Access Key",f"", None, new_account["name"], 'password')
                            new_account['access_secret'] = st.text_input(f"Access Secret",f"", None, new_account["name"], 'password')

                            ## Find the right multiselection for media platform
                            media_platforms_df = pd.DataFrame(settings.supported_media_platforms)
                            media_selected_index = 0 

                            # create 3 options in a select box
                            new_account['media_platform'] = st.selectbox("Media platform", media_platforms_df,index = media_selected_index, key=new_account["name"])
                    


        ##### SUBMIT BUTTON
        submitted = st.form_submit_button("Submit", section)

        if submitted:  # if the user has submitted the form, then the settings.cfg file is updated with the new values.
            with st.expander("Settings Saved"):
                for section2 in sections:
                    for setting in setting_buttons_dict:
                        
                        ##### CHECK IF THE SETTING IS MOST CURRENT
                        try: 
                            if setting_buttons_dict[setting] != settings.get_setting_value(section2, setting):
                                ## Create a notice of changes
                                st.markdown(setting + ": " + f"`{setting_buttons_dict[setting]}`")

                                ##### UPDATE THE SETTING
                                if str(setting) != "media_accounts":
                                    settings.set_setting_value(section2, setting, setting_buttons_dict[setting])

                        except Exception as e:
                            pass
                    
                ##### UPDATE ACCOUNTS
                try:
                    for button in media_account_button_list:
                        button_data = {
                            "display_name": button["display_name"],
                            "name": button["name"],
                            "key": button["key"],
                            "secret": button["secret"],
                            "access_key": button["access_key"],
                            "access_secret": button["access_secret"],
                            "media_platform": button["media_platform"]
                        }

                        button_request_removal = media_account_button_dict["request_removal"]

                        found_difference = False

                        for account in settings.media_accounts:
                            if account['name'] == button["name"]:
                                # compare all data and break if there is a difference
                                for key in button_data:
                                    if button_data[key] != account[key]:
                                        found_difference = True
                                        st.markdown(button['name'] + ": " + f"`Setting {key} has changed`")

                        
                        if button_request_removal:
                            account_to_update = Account(name=button_data["name"])
                            account_to_update.remove()


                        ## If changes in account details, update the settings file
                        if found_difference:
                            account_to_update = Account(name=button_data["name"])
                            account_to_update.load_data()
                            account_to_update.update(display_name=button_data["display_name"], key=button_data["key"], secret=button_data["secret"], access_key=button_data["access_key"], access_secret=button_data["access_secret"], media_platform=button_data["media_platform"])


                except Exception as e:
                    pass
                
                try:
                    if new_account['name'] != "":
                        account_to_add = Account(name=new_account['name'])
                        account_to_add.register(display_name=new_account['display_name'], key=new_account['key'], secret=new_account['secret'], access_key=new_account['access_key'], access_secret=new_account['access_secret'], media_platform=new_account['media_platform'])

                except Exception as e:
                    print(e)