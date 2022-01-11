
import streamlit as st
from resources.config import settings_core

settings = settings_core()


def app():

    ##### LOAD SETTINGS FILE AND FIND SECTIONS
    settings_file = open(settings.current_path + "settings.cfg", "r")
    sections = settings.get_all_setting_categories()
    setting_buttons_dict = {}


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
                        ## Create secrets buttons for each media account. 
                        media_accounts = settings.media_accounts#settings.get_setting_value(section, setting)
                        media_accounts_list = []

                        if media_accounts != None:

                            for media_account in media_accounts:
                                media_accounts_list.append(media_account)

                            for media_account in media_accounts_list:
                                media_display_name = media_account["display_name"]
                                media_account_name = media_account["name"]
                                media_account_key = media_account["key"]
                                media_account_secret = media_account["secret"]
                                media_account_access_key = media_account["access_key"]
                                media_account_access_secret = media_account["access_secret"]
    


                                with st.expander(media_display_name):
                                    st.text_input(f"Key",f"{media_account_key}", None, None, "password")
                                    st.text_input(f"Secret",f"{media_account_secret}", None, None, "password")  
                                    if media_account_access_key != "":
                                        st.text_input(f"Access Key",f"{media_account_access_key}", None, None, "password")
                                    if media_account_access_secret != "":
                                        st.text_input(f"Access Secret",f"{media_account_access_secret}", None, None, "password")
                        else:
                            st.text("No media accounts added")

        ##### SUBMIT BUTTON
        submitted = st.form_submit_button("Submit", section)


        if submitted:  # if the user has submitted the form, then the settings.cfg file is updated with the new values.
            with st.expander("Settings Saved"):
                for section in sections:
                    for setting in setting_buttons_dict:
                        
                        ##### CHECK IF THE SETTING IS MOST CURRENT
                        try: 
                            if setting_buttons_dict[setting] != settings.get_setting_value(section, setting):
                                st.markdown(setting + ": " + f"`{setting_buttons_dict[setting]}`")

                                ##### UPDATE THE SETTING
                                settings.set_setting_value(section, setting, setting_buttons_dict[setting])
                        except:
                            pass
