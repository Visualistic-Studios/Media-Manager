import os
from datetime import datetime

import streamlit as st

from resources.utility import convert_strings_to_datetime
from resources.config import settings_core
from resources.posts import post
from resources.accounts import Account

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
        for account in settings.media_accounts:
            account_to_update = Account(name=account["name"])
            account_to_update.load_data()
            for location in account_to_update.posting_locations:
                account_locations.append(f"{account['name']}://{location}")


        if account_locations:
            media_accounts_checkboxes = st.multiselect("Select media accounts", account_locations, format_func=format_post_option)
        else:
            st.markdown("> No media account locations found -- Please add at least 1 in settings")

        

        ##### FILE UPLOAD
        uploaded_file_list = None

        uploaded_files = st.file_uploader("Upload attachments", accept_multiple_files=True)

        st.info("Files that are uploaded first get put first in order when published.")
        
        if len(uploaded_files) > 0:
        
            ##### FOR UPLOADED FILES
            for your_file in uploaded_files:

                ##### CREATE A FILE NAME

                ## append datetime to file name to make it unique
                chosen_file_name = datetime.now().strftime("%Y-%m-%M-%S") + "-" + your_file.name

                #chosen_file_name = str(hash(your_file.getvalue())) + "." + your_file.name.split(".")[-1]
                new_file_path = os.path.join(settings.uploaded_media_dir, chosen_file_name)

                if not os.path.exists(new_file_path):
                    ##### SAVE THE FILE
                    with open(new_file_path, "wb") as f:
                        f.write(your_file.getbuffer())
                        print(f"Saved file {chosen_file_name} to disk")
                        uploaded_file_list.append(chosen_file_name)
            
                else:  
                    print(f"File {chosen_file_name} already exists. File has been referenced rather than saved.")
                    uploaded_file_list.append(chosen_file_name)


        ##### SUBMIT BUTTON
        submitted = st.form_submit_button("Submit")

        ##### IF SUBMITTED
        if submitted:

            ##### CREATE POST
            st.spinner("Creating post...")
            
            # get current time in chosen timezone
            current_time = datetime.now(datetime.strptime(timezone_input, '%z').tzinfo)

            ##### IF POST IN FUTURE
            if datetime_input > current_time:

                ##### CHECK FOR MEDIAS SELECTED
                desired_locations = []

                ##### IF MEDIA ACCOUNTS SELECTED
                try: 
                    if len(media_accounts_checkboxes) > 0:
                        for media_account in media_accounts_checkboxes:
                            desired_locations.append(media_account)


                        if uploaded_file_list:
                        
                            ##### CREATE POST OBJECT
                            desired_post = post(chosen_title, chosen_description, "n/a", date_input, time_input, timezone_input, desired_locations, uploaded_file_list)
                        else:

                            ##### CREATE POST OBJECT
                            desired_post = post(chosen_title, chosen_description, "n/a", date_input, time_input, timezone_input, desired_locations)
                        
                        ##### SAVE POST OBJECT
                        desired_post.save_as_scheduled()

                        ##### SUCCESS FEEDBACK
                        st.success(f""""{chosen_title}" has been Scheduled!""")
                    
                    else:
                        st.error("Please select at least one media account")
                except Exception as e:
                    st.error("Please add a media account in 'Settings'")
                    print(e)

            ##### IF POST IN PAST
            else:    
                ##### ERROR FEEDBACK
                st.warning(settings.post_not_scheduled_for_reason_time_in_past)
