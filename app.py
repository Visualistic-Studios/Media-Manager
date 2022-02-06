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
import numpy as np
import pandas as pd
import time
import os
import pathlib
from resources.setup import setup_check, initialize_settings, check_first_time_setup, initialize_app


## Checking for first time setup, will generate settings file & only allow for first time setup screen
setup_check()
if check_first_time_setup():
    initialize_app()

## Continue the imports
from resources.page_manager import PageManager
from resources.config import settings_core
from pages import new_posts, settings_page, app_setup




#  _   _            _       _     _           
# | | | |          (_)     | |   | |          
# | | | | __ _ _ __ _  __ _| |__ | | ___  ___ 
# | | | |/ _` | '__| |/ _` | '_ \| |/ _ \/ __|
# \ \_/ / (_| | |  | | (_| | |_) | |  __/\__ \
#  \___/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/
# -----------------------------------------------------------------------                                              



settings = settings_core()
app = PageManager()



#   ___              _ _           _   _             
#  / _ \            | (_)         | | (_)            
# / /_\ \_ __  _ __ | |_  ___ __ _| |_ _  ___  _ __  
# |  _  | '_ \| '_ \| | |/ __/ _` | __| |/ _ \| '_ \ 
# | | | | |_) | |_) | | | (_| (_| | |_| | (_) | | | |
# \_| |_/ .__/| .__/|_|_|\___\__,_|\__|_|\___/|_| |_|
#       | |   | |                                    
#       |_|   |_|                                    
# ----------------------------------------------------------------------- 



st.set_page_config(page_title="Media Manager", page_icon=None, layout='centered', initial_sidebar_state='auto', menu_items={'Get help':None,'Report a Bug':"https://github.com/Visualistic-Studios/Media-Manager/issues",'About':"https://github.com/Visualistic-Studios/Media-Manager/",})
st.header("Media Manager")



########## ADD PAGES HERE
#####

##### First Time Setup
if check_first_time_setup():
    app.add_page("App Setup", app_setup.app)

##### Regular Application 
else:
    app.add_page("New Posts", new_posts.app)
    app.add_page("Settings", settings_page.app)



app.run()