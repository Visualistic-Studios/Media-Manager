import streamlit as st



from resources.config import settings_core

settings = settings_core()

class PageManager:

    ########## INIT
    #####
    def __init__(self):
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []
    

    ########## ADD PAGE 
    #####
    #@st.cache (ttl=settings.page_cache_time, suppress_st_warning=True)
    def add_page(self, title, func): 
        self.pages.append({"title": title, "function": func})


    ########## RUN PAGE 
    #####

    def run(self):
        ##### DROPDOWN 
        page = st.sidebar.selectbox('App Navigation', self.pages, format_func=lambda page: page['title'])

        ##### RUN PAGE FUNC
        page['function']()