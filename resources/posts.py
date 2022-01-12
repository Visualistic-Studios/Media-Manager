
import os
import streamlit as st

from datetime import datetime, date
from resources.config import settings_core
from resources.utility import string_to_list, convert_strings_to_datetime
settings = settings_core()






########## POST CLASS 
#####
class post:

    ##### INIT
    """
    Post class
    Will Automatically handle replacing '|__NEWLINE__|' with '\n'
    Functionality for saving posts to file
    Can remove itself from a file    
    """
    def __init__(self, title, description, link, date_to_post, time_to_post, medias_to_post_on, attachments=None):
        self.title = title
        self.description = description.replace('|__NEWLINE__|', '\n')
        self.link = link
        self.date_to_post = date_to_post
        self.time_to_post = time_to_post
        self.attachments = attachments 

        ## create datetime object from date object and time object
        self.datetime_to_post = convert_strings_to_datetime(self.date_to_post, self.time_to_post)
        self.medias_to_post_on = medias_to_post_on
    

    ##### DATA TO LIST
    def data_to_list(self):
        """Returns a list of post data"""
        if self.attachments:
            return f"{self.title}|-|{self.description}|-|{self.link}|-|{self.datetime_to_post}|-|{self.medias_to_post_on}|-|{self.attachments}"
        else:
            return f"{self.title}|-|{self.description}|-|{self.link}|-|{self.datetime_to_post}|-|{self.medias_to_post_on}|-|"


    ##### CREATES FILE LIST
    ## 
    def create_file_list(self, file_paths):
        """
        Creates a list of file object from a list of paths
        """
        file_list = []
        for path in file_paths:
            # Read Binary File
            file_list.append(open(path, 'rb'))
        return file_list

    ##### GET ATTACHMENT PATH
    """
    Gets a full attachment path from a file name
    """
    def get_attachment_path(self, attachment_name):
        attachment_path = settings.full_uploaded_media_dir + "/" + attachment_name
        attachment_path = attachment_path.replace("'", "")
        attachment_path = attachment_path.strip("\n")
        attachment_path = attachment_path.strip("][")
        return attachment_path
    


    ## load attachments
    def load_attachments(self):
                ## check if attachments exist
        if self.attachments:
            ## load attachments
            attachment_list = []
            print(len(self.attachments))
            for attachment in self.attachments:
                if not attachment == "[]" or not attachment == "['']" or not attachment == "['\\n']" or not attachment == "\n" or not attachment == "":
                    attachment_clean = attachment.replace("'", "")
                    attachment_clean = attachment_clean.strip("\n")
                    attachment_clean = attachment_clean.strip("][")
                    print (attachment_clean)
                    if not attachment_clean == "[]" or not attachment_clean == "['']" or not attachment_clean == "['\\n']" or not str(attachment_clean) == "\n":
                        attachment_path = settings.full_uploaded_media_dir + "/" + attachment_clean
                        ## I hate this code replace it.
                        if not attachment_path == settings.full_uploaded_media_dir + "/":
                            attachment_list.append(open(attachment_path, 'rb'))
            return attachment_list
        else:
            return None



    def get_all_image_attachments(self):
        """
        Returns a list of image attachments
        """
        image_attachments = []
        if self.attachments:
            for attachment in self.attachments:
                attachment_path = self.get_attachment_path(attachment)
                if os.path.isfile(attachment_path):
                    attachment_type = attachment_path.split('.')[-1]
                    if attachment_type in settings.supported_image_types:
                        image_attachments.append(attachment_path)
        return image_attachments


    def get_all_video_attachments(self):
        """
        Returns a list of video attachments
        """
        video_attachments = []
        if self.attachments:
            for attachment in self.attachments:
                attachment_path = self.get_attachment_path(attachment)
                if os.path.isfile(attachment_path):
                    attachment_type = attachment_path.split('.')[-1]
                    if attachment_type in settings.supported_video_types:
                        video_attachments.append(attachment_path)
        return video_attachments


    ##### SAVE AS SCHEDULED
    def save_as_scheduled(self):
        if self.datetime_to_post > datetime.now():
            try:
                localfile = open(settings.scheduled_posts_file_location_full, 'a+')
                if localfile:
                    localfile.write(str(self.data_to_list()).replace('\n', '|__NEWLINE__|') + '\n')
                    localfile.close()
            except Exception as e:
                print(e)      
            return None


    ##### SAVE AS PUBLISHED
    def save_as_published(self):
        try:
            localfile = open(settings.published_posts_file_location_full, 'a+')
            if localfile:
                localfile.write(str(self.data_to_list()) + '\n')
                localfile.close()
                print('logged post')
        except Exception as e:
            print(e)      
        return None


    ##### REMOVE FROM SCHEDULED FILE
    def remove_from_scheduled(self):
        print("attempting self removal")
        try:
            localfile = open(settings.scheduled_posts_file_location_full, 'r')
            if localfile:
                lines = localfile.readlines()
                localfile.close()
                for line in lines:

                    line_title = line.split('|-|')[0]
                    line_description = line.split('|-|')[1].replace('|__NEWLINE__|', '\n')
                    line_link = line.split('|-|')[2]
                    line_datetime = line.split('|-|')[3]
                    line_date = line.split('|-|')[3].split(' ')[0]
                    line_time = line.split('|-|')[3].split(' ')[1]
                    line_medias = string_to_list(line.split('|-|')[4])

                    ##### IF DATA MATCHES
                    if line_title == self.title and line_description == self.description and line_link == self.link and line_date == self.date_to_post and line_time == self.time_to_post and line_date == self.date_to_post and line_time == self.time_to_post and line_medias == self.medias_to_post_on:
                 
                        lines.remove(line)
                        localfile = open(settings.scheduled_posts_file_location_full, 'w')
                        localfile.writelines(lines)
                        localfile.close()
                        return True
                    else:
                        continue

        except Exception as e:
            print(e)
            return None



########## CREATE POST OBJECT FROM STRING
#####
def create_post_object_from_string(line):

    ##### SPLIT LINE INTO LIST
    line = line.split('|-|')
    date_time_array = line[3].split(' ')


    ##### CREATE TIME OBJECT
    if date_time_array:
        date = date_time_array[0]
        time = date_time_array[1]
    else:
        date = None
        time = None

    ##### CREATE MEDIA / ATTACHMENT OBJECT
    ##### CREATE SCHEDULED POST
    try: 
        if line[5]:
            attachments = string_to_list(line[5])
            post_object = post(line[0], line[1], line[2], date, time, string_to_list(line[4]),attachments)
    except:
        attachments = None
        post_object = post(line[0], line[1], line[2], date, time, string_to_list(line[4]))

    return post_object



########## GET ALL POSTS
#####
def get_all_published_posts():
    post_data = []
    try:
        if os.path.exists(settings.published_posts_file_location_full):
            localfile = open(settings.published_posts_file_location_full, 'r')
            if localfile:
                for line in localfile:
                    post_data.append(str(line) + "\n")
            else:
                print('no posts found')
                return None
    except:
        print(e)
        return None
    return post_data



########## GET ALL SCHEDULED POSTS
#####
#@st.cache (ttl=settings.posts_cache_time)
def get_all_scheduled_posts():
    post_data = []
    try:
        if os.path.exists(settings.scheduled_posts_file_location_full):
            localfile = open(settings.scheduled_posts_file_location_full, 'r+')
            if localfile:
                for line in localfile:
                    temp_post = create_post_object_from_string(line)
                    post_data.append(temp_post)
            else:
                print(e)
                return None
        else:
            print(e)
            return None
    except Exception as e:
        print(e)
        return None
    return post_data

