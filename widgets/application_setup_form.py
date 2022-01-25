#  ___                                 _        
# |_ _| _ __ ___   _ __    ___   _ __ | |_  ___ 
#  | | | '_ ` _ \ | '_ \  / _ \ | '__|| __|/ __|
#  | | | | | | | || |_) || (_) || |   | |_ \__ \
# |___||_| |_| |_|| .__/  \___/ |_|    \__||___/
#                 |_|                           
# -----------------------------------------------------------------------   



import streamlit as st
from resources.setup import initalize_encryption, delete_first_time_setup


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
        encryption_key_location = st.text_input("Key Location ('/home/user/.media-manager')", placeholder="Where would you like to store your key? Pick somewhere safe!!")
        encryption_key = st.text_input("Key", placeholder="[EXISTING_KEY_HERE]")

        ##### SUBMIT BUTTON
        submitted = st.form_submit_button("Submit")

        ##### IF SUBMITTED
        if submitted:
            if encryption_key_location:
                if encryption_selection == "Generate New Key":
                    encryption_key = None
                encryption_key = initalize_encryption(encryption_key, encryption_key_location)
                if encryption_key[0]:  
                    st.success("Application Setup Complete!")
                    st.write("Here's a copy of your key, back it up somewhere safe and don't lose it!")
                    st.text_input("Key", encryption_key[0].decode('utf-8'), type='password')
                    st.write("You'll need this everytime you reinstall the app, or you'll lose your data!")
                    st.success("Please restart the Application")
                    delete_first_time_setup()
                else:
                    st.error(encryption_key[1])
            else:
                st.error("Please enter a key location.")
