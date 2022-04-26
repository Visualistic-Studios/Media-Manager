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
from resources.global_mentions import global_mentions_manager as gmm, global_mention as gm


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
    global_mentions_manager_current = settings.global_mentions
    global_mentions_manager_working = gmm()
    
    

    ## Title
    with st.expander("Global Mentions"):

        ## Dividers
        st.markdown(f"-----")

        ## Loop on Mentions
        if global_mentions_manager_current:
            if global_mentions_manager_current.entries:
                if len(global_mentions_manager_current.entries) > 0: # global_mentions

                    ########## CURRENT GLOBAL MENTIONS
                    ## For each Global Mention
                    for index, global_mention in enumerate(global_mentions_manager_current.entries): # gID

                        gID_input = st.text_input(label="Global ID",value=global_mention.id, key=f"{global_mention.id}{index}")

                        if not gID_input == "":

                            platform_mentions = []

                            ########## EXISTING PLATFORM ENTRIES
                            for index2, platform_data in enumerate(global_mention.platform_mentions):

                                ## Initialize Platform Data
                                gID_platform = platform_data[0]
                                gID_platform_ID = platform_data[1]
                                
                                ## Create Setting Layout
                                col1, col2 = st.columns(2)

                                ## Platform
                                with col1:
                                    gID_platform_data = st.text_input(label="Platform", value=gID_platform, key=f"{global_mention.id}_platform_{index2}")

                                ## Platform ID
                                with col2:
                                    gID_platform_data_id = st.text_input(label="Platform ID", value=gID_platform_ID, key=f"{global_mention.id}_platform_ID_{index2}") 

                                ## Add to Platforms List
                                if gID_platform_data == "" or gID_platform_data_id == "": # Maybe this needs to check for none? idk

                                    ## Don't log empty platform 
                                    continue
                                
                                else:
                                    ## Log platform
                                    platform_mentions.append([gID_platform_data, gID_platform_data_id])



                                ########## NEW PLATFORM REGISTRATION
                                if index2 == len(global_mention.platform_mentions)-1:
                                        
                                    ## Create Setting Layout
                                    col1, col2 = st.columns(2)

                                    ## Platform
                                    with col1:
                                        new_gID_platform_data = st.text_input(label="Platform", value=settings.new_gid_mention_platform_message, key=f"new_gid_mention_{global_mention.id}_new_platform_{index2}")

                                    ## Platform ID
                                    with col2:
                                        new_gID_platform_data_id = st.text_input(label="Platform ID", value=settings.new_gid_mention_platform_id_message, key=f"new_gid_mention_{global_mention.id}_new_platform_ID_{index2}") 

                                    ## Check registration & add if valid
                                    if global_mention.register_platform_check(new_gID_platform_data, new_gID_platform_data_id):
                                        platform_mentions.append([new_gID_platform_data, new_gID_platform_data_id])

                        else:
                            ## Empty GID, user has removed it
                            continue
        
                        ## Dividers                
                        st.markdown(f"-----")

                        ## Add to Working Global Mentions
                        if not len(platform_mentions) == 0:

                            ## Create new mention from data above (Final Global Mention Obj)
                            local_mention = gm(gID_input, platform_mentions)
                            
                            ## Log it with manager
                            global_mentions_manager_working.add_global_mention(local_mention)



            ########## NEW GLOBAL MENTIONS
            #####

            ## Global Mention Registration
            global_mentions_registration_return = global_mentions_registration.app()
            if global_mentions_registration_return:

                ## Register New Global Mention
                global_mentions_manager_working.add_global_mention(global_mentions_registration_return)


            ########## RETURN
            #####

            ## Global Mentions Valid
            if global_mentions_manager_working:
                return global_mentions_manager_working
            
            ## Global Mentions Invalid
            else:
                return None

        else:
            print('no global mention manager found in settings')
            return None
                