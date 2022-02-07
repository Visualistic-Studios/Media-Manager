#  ___                                 _        
# |_ _| _ __ ___   _ __    ___   _ __ | |_  ___ 
#  | | | '_ ` _ \ | '_ \  / _ \ | '__|| __|/ __|
#  | | | | | | | || |_) || (_) || |   | |_ \__ \
# |___||_| |_| |_|| .__/  \___/ |_|    \__||___/
#                 |_|                           
# -----------------------------------------------------------------------   



import streamlit as st
from resources.setup import initalize_encryption, delete_first_time_setup, intialize_s3


#  _____                      _    _                    
# |  ___| _   _  _ __    ___ | |_ (_)  ___   _ __   ___ 
# | |_   | | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
# |  _|  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
# |_|     \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
# -----------------------------------------------------------------------                                              



def app():

    with st.form("Application Setup"):
        
        st.markdown("#### Welcome!")

        st.write("###### Hello there! Welcome to Media Manager. Since this is your first time running the app, we need to set up encryption :)")

        st.markdown("#### Encryption Key")

        st.write("###### We encrypt your data to keep it safe; we'll use a key that will be stored locally in a safe space. You can generate a key below, or you can use one that's already been generated.")

        encryption_selection = st.selectbox("Encryption Setup", ["Generate New Key", "Use Existing Key"])
        encryption_key_location = st.text_input("Key Location", placeholder="/home/user/.media-manager")
        encryption_key = st.text_input("Key", placeholder="[EXISTING_KEY_HERE]")

        st.markdown("#### S3 Credentials")

        st.write("###### Media Manager uses S3 to store much of the saved data for this application. All of it's encrypted locally with the key mentioned above before being sent to the server. You can use a service like Storj.io to create S3 credentials in minutes; more info avaiable on the GitHub page.")

        s3_access = st.text_input("", placeholder="access-key", type='password')
        s3_secret = st.text_input("", placeholder="secret-key", type='password')
        s3_endpoint = st.text_input("", placeholder="https://gateway.eu1.storjshare.io", type='password')
        s3_bucket = st.text_input("", placeholder="bucket-name", type='password')

        ##### SUBMIT BUTTON
        submitted = st.form_submit_button("Submit")

        ##### IF SUBMITTED
        if submitted:
            if encryption_key_location:
                    if encryption_selection == "Generate New Key":
                        encryption_key = None
                    encryption_key = initalize_encryption(encryption_key, encryption_key_location)
                    if encryption_key[0]:  
                        if s3_access and s3_secret and s3_endpoint and s3_bucket:
                        ## Successful Key Creation / Load

                            intialize_s3(s3_access, s3_secret, s3_endpoint, s3_bucket)
                            st.success("Application Setup Complete!")
                            st.write("Here's a copy of your key, back it up somewhere safe and don't lose it!")
                            st.text_input("Key", encryption_key[0].decode('utf-8'), type='password')
                            st.write("You'll need this everytime you reinstall the app, or you'll lose your data!")
                            st.success("Please restart the Application")
                            
                            delete_first_time_setup()



            ##### ERRORS
                        else:
                            st.error("Please enter S3 details")
                    else:
                        st.error(encryption_key[1])
            else:
                st.error("Please enter a key location.")
