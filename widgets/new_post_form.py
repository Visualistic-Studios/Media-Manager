import os
from datetime import datetime

import streamlit as st

from resources.utility import convert_strings_to_datetime
from resources.config import settings_core
from resources.posts import post
from resources.accounts import Account
from resources.crypt import Key, Crypt
from hashlib import new, sha256
from io import StringIO


settings = settings_core()


def format_timezone(timezone):
    return f"UTC{timezone}"


def app():

    ##### NEW POSTS FORM
    with st.form("new_post_form"):
        st.markdown("#### Create a new post")


        ##### DATE / TIME
        datetime_col_date, datetime_col_time, datetime_col_timezone = st.columns(3)

        # Get default timezone from settings & find it in the list of timezones
        default_timezone = settings.default_timezone
        timezones = settings.utc_timezones

        # find default timezone in timezones
        default_timezone_index = 0
        for i in range(0, len(timezones)):
            if timezones[i] == default_timezone:
                default_timezone_index = i
                break
            else:
                default_timezone_index = 14
        
        with datetime_col_date:
            date_input = st.date_input("DATE")
        with datetime_col_time:
            time_input = st.time_input("TIME")
        with datetime_col_timezone:
            timezone_input = st.selectbox("UTC TIMEZONE", settings.utc_timezones,key="timezone_input", format_func=format_timezone, index=default_timezone_index)
        

        datetime_input = convert_strings_to_datetime(date_input, time_input, timezone_input)

        ##### TITLE / DESCRIPTION
        chosen_title = st.text_input("Title")
        chosen_description = st.text_area("Description")


        ##### POST LOCATION
        st.write("Where would you like to post?")

        
        ##### ACCOUNT LOCATION SELECTION
        def format_post_option(option=[]):
            return option

        ## Create a list of locations from each account
        account_locations = []
        if settings.media_accounts:
            for account in settings.media_accounts:
                account_to_update = Account(name=account["name"])
                account_to_update.load_data()
                if account_to_update:

                    for location in account_to_update.posting_locations:
                        account_locations.append(f"{account['name']}://{location}")


            if account_locations:
                media_accounts_checkboxes = st.multiselect("Select media accounts", account_locations, format_func=format_post_option)
            else:
                st.markdown("> No media account locations found -- Please add at least 1 in settings")
        else:
            st.markdown("> No media account locations found -- Please add at least 1 in settings")

        

        ##### FILE UPLOAD
        uploaded_file_list = []

        uploaded_files = st.file_uploader("Upload attachments", accept_multiple_files=True)

        st.info("Files that are uploaded first get put first in order when published.")
        



        ##### SUBMIT BUTTON
        submitted = st.form_submit_button("Submit")

        ##### IF SUBMITTED
        if submitted:
            new_post_progress = st.progress(0)
            new_post_progress.progress(5)

            ##### CREATE POST
            st.spinner("Creating post...")
            
            # get current time in chosen timezone
            current_time = datetime.now(datetime.strptime(timezone_input, '%z').tzinfo)
            new_post_progress.progress(5)

            ##### IF POST IN FUTURE
            if datetime_input > current_time:

                ##### CHECK FOR MEDIAS SELECTED
                desired_locations = []

                ##### IF MEDIA ACCOUNTS SELECTED
                try: 
                    if len(media_accounts_checkboxes) > 0:
                        for media_account in media_accounts_checkboxes:
                            desired_locations.append(media_account)
                        
                        
                        new_post_progress.progress(35)
                        current_progress = 35


                        ##### GET UPLOADED FILES
                        if len(uploaded_files) > 0:
                            ##### SAVE ENCRYPTED UPLOADED FILES
                            per_file_increase = 60 / (len(uploaded_files) + 1)
                            per_file_increase = int(per_file_increase)
                            for your_file in uploaded_files:
                                
                                ## Track Progress
                                current_progress += per_file_increase
                                new_post_progress.progress(current_progress)

                                ## Create Filename & Path
                                chosen_file_name = sha256(your_file.getvalue()).hexdigest() + "." + your_file.name.split(".")[-1]
                                new_file_path = os.path.join(settings.uploaded_media_dir, chosen_file_name)

                                ## Create Encrypted File
                                if not settings.storage.does_file_exist(new_file_path):
                                    with settings.storage.open_file(new_file_path, 'wb') as new_file:
                                        settings.crypt.encrypt_stream(your_file, new_file)
                                    
                                    print(f"Saved file {chosen_file_name}")
                                    uploaded_file_list.append(new_file_path)
                                    print("Verifying File...")
                                    if settings.storage.does_file_exist(new_file_path):
                                        continue
                                    else:
                                        st.exception("File not found on storage after uploading")
                                        break
                                    

                                ## Reference Existing File
                                else:  
                                    print(f"File {chosen_file_name} already exists. File has been referenced rather than saved.")
                                    uploaded_file_list.append(new_file_path)


                        ##### IF UPLOADED FILES
                        if uploaded_file_list:
                        
                            ##### CREATE POST OBJECT
                            desired_post = post(chosen_title, chosen_description, "n/a", date_input, time_input, timezone_input, desired_locations, uploaded_file_list)
                        else:

                            ##### CREATE POST OBJECT
                            desired_post = post(chosen_title, chosen_description, "n/a", date_input, time_input, timezone_input, desired_locations)

                        new_post_progress.progress(95)
                        
                        ##### SAVE POST OBJECT
                        desired_post.save_as_scheduled()

                        new_post_progress.progress(100)

                        ##### SUCCESS FEEDBACK
                        st.success(f""""{chosen_title}" has been Scheduled!""")

                        new_post_progress.empty()
                    
                    else:
                        st.error("Please select at least one media account")
                except Exception as e:
                    st.error("Please add a media account in 'Settings'")
                    print(e)

            ##### IF POST IN PAST
            else:    
                ##### ERROR FEEDBACK
                st.warning(settings.post_not_scheduled_for_reason_time_in_past)
