
import streamlit as st
from resources.posts import get_all_scheduled_posts, post
from resources.config import settings_core
import os
from typing import Dict


from widgets import media_post, new_post_form

settings = settings_core()

def app():    

    new_post_form.app()
    
    ########## POSTS LIST
    #####

    ## GET ALL SCHEDULED POSTS
    scheduled_posts = get_all_scheduled_posts()

    ## CREATE WIDGET FOR EACH POST
    if scheduled_posts:
        for index, entry in enumerate(scheduled_posts):
            media_post.app(entry, index)
    ## IF NO POSTS SHOW NO POSTS DESCRIPTION  
    else:
        with st.sidebar.expander(settings.no_posts_title):
            st.write(settings.no_posts_description)

