#  _____                           _       
# |_   _|                         | |      
#   | | _ __ ___  _ __   ___  _ __| |_ ___ 
#   | || '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| || | | | | | |_) | (_) | |  | |_\__ \
#  \___/_| |_| |_| .__/ \___/|_|   \__|___/
#                | |                       
#                |_|                       
# -----------------------------------------------------------------------   



import streamlit as st
from resources.config import settings_core
from widgets import global_mentions_registration



#  _   _            _       _     _           
# | | | |          (_)     | |   | |          
# | | | | __ _ _ __ _  __ _| |__ | | ___  ___ 
# | | | |/ _` | '__| |/ _` | '_ \| |/ _ \/ __|
# \ \_/ / (_| | |  | | (_| | |_) | |  __/\__ \
#  \___/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/
# -----------------------------------------------------------------------     



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



def app():

    ## Initialize
    global_mentions = settings.global_mention_ids
    global_mentions_dict = {}
    global_mentions_values = list(global_mentions.values())
    new_global_mention_platform = {}

    ## Title
    with st.expander("Global Mention IDs"):

        ## Dividers
        st.markdown(f"-----")

        ## Loop on Mentions
        if len(global_mentions) > 0:

            ########## CURRENT GLOBAL MENTIONS
            for index, gID in enumerate(global_mentions):

                ## Initialize
                gID_mention_entries = global_mentions_values[index][1]
                platform_mentions = []

                #### 
                gID_input = st.text_input(label="Global ID",value=gID)

                ##### MENTION ENTRIES
                for index2, platform_data in enumerate(gID_mention_entries):

                    ## Initialize Platform Data
                    gID_platform = platform_data[0]
                    gID_platform_ID = platform_data[1]
                    
                    ## Create Setting Layout
                    col1, col2 = st.columns(2)

                    ## Platform
                    with col1:
                        gID_platform_data = st.text_input(label="Platform", value=gID_platform, key=f"{gID}_platform_{index2}")

                    ## Platform ID
                    with col2:
                        gID_platform_data_id = st.text_input(label="Platform ID", value=gID_platform_ID, key=f"{gID}_platform_ID_{index2}") 

                    ## Add to Platforms List
                    platform_mentions.append([gID_platform_data, gID_platform_data_id])

                    ## New Platform Mention Registration
                    if index2 == len(gID_mention_entries)-1:
                            
                        ## Create Setting Layout
                        col1, col2 = st.columns(2)

                        ## Platform
                        with col1:
                            new_gID_platform_data = st.text_input(label="Platform", value=settings.new_gid_mention_platform_message, key=f"new_gid_mention_{gID}_platform_{index2}")

                        ## Platform ID
                        with col2:
                            new_gID_platform_data_id = st.text_input(label="Platform ID", value=settings.new_gid_mention_platform_id_message, key=f"new_gid_mention_{gID}_platform_ID_{index2}") 

                        ## Not Default Values & Not Empty
                        if not new_gID_platform_data == settings.new_gid_mention_platform_message or not new_gID_platform_data == "" and not new_gID_platform_data_id == settings.new_gid_mention_platform_id_message or not new_gID_platform_data_id == "" :
                            platform_mentions.append([new_gID_platform_data, new_gID_platform_data_id])
                        
                ## Dividers                
                st.markdown(f"-----")

                ## Get list of other platform mentions
                global_mentions_dict[gID] = [gID_input,platform_mentions]



        ########## NEW GLOBAL MENTIONS
        #####

        ## Global Mention Registration
        global_mentions_registration_return = global_mentions_registration.app()
        if global_mentions_registration_return:

            ## Initialization
            global_mention_id = global_mentions_registration_return[0]
            platform_mention_data = global_mentions_registration_return[1]

            ## Add to Global Mention IDs
            global_mentions_dict[global_mention_id] = [global_mention_id,platform_mention_data]


        ########## RETURN
        #####

        ## Global Mentions Valid
        if len(global_mentions_dict) > 0:
            return global_mentions_dict
        
        ## Global Mentions Invalid
        else:
            return None

            