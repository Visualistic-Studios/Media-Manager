import streamlit as st
import numpy as np
import pandas as pd
import time
import os

from resources.page_manager import PageManager
from resources.config import settings_core
from pages import new_posts, settings_page


settings = settings_core()
app = PageManager()



def initialize_app():

    ##### SAVED PATH
    if not os.path.exists(settings.saved_path):
        os.mkdir(settings.saved_path)

    ##### UPLOADED MEDIA PATH
    if not os.path.exists(settings.uploaded_media_dir):
        os.mkdir(settings.uploaded_media_dir)

    ##### SCHEDULED POST PATH
    if not os.path.exists(settings.scheduled_posts_file_location_full):
        open(settings.scheduled_posts_file_location_full, 'a+').close()

    ##### PUBLISHED POST PATH
    if not os.path.exists(settings.published_posts_file_location_full):
        open(settings.published_posts_file_location_full, 'a+').close()




initialize_app()


st.set_page_config(page_title="Media Manager", page_icon=None, layout='centered', initial_sidebar_state='auto', menu_items={'Get help':None,'Report a Bug':"https://github.com/Visualistic-Studios/Media-Manager/issues",'About':"https://github.com/Visualistic-Studios/Media-Manager/",})
st.header("Media Manager")


########## ADD PAGES HERE
#####
app.add_page("New Posts", new_posts.app)
app.add_page("Settings", settings_page.app)

app.run()