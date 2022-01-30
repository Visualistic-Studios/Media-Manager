
import os
import streamlit as st

from datetime import datetime, date
from resources.config import settings_core
from resources.utility import string_to_list, convert_strings_to_datetime
import resources.crypt as crypt
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
    def __init__(self, title, description, link, date_to_post, time_to_post, time_zone_to_post, locations_to_post, attachments=None):
        self.title = title
        self.description = description.replace('|__NEWLINE__|', '\n')
        self.link = link
        self.date_to_post = date_to_post

        ## Remove any timezone information so it can be manually added
        try:
            if "+" in time_to_post:
                self.time_to_post = time_to_post.split("+")[0]
            else:
                self.time_to_post = time_to_post.split("-")[0]
        except:
            self.time_to_post = time_to_post
        
        self.attachments = attachments 
        self.time_zone_to_post = time_zone_to_post

        ## 
        self.datetime_to_post = convert_strings_to_datetime(self.date_to_post, self.time_to_post, self.time_zone_to_post)

        self.locations_to_post = locations_to_post


        
    

    ##### DATA TO LIST
    def data_to_list(self):
        """Returns a list of post data"""

        posting_locations_string = ""

        if self.locations_to_post[-1].strip(" ") == "":
            del self.locations_to_post[-1]

        for index, loc in enumerate(self.locations_to_post):
            if index == len(self.locations_to_post) - 1 and not loc.strip(" ")=="":
                posting_locations_string += loc
            elif not loc.strip(" ")=="":
                posting_locations_string += loc + "|_|"

        if self.attachments:
            return f"{self.title}|-|{self.description}|-|{self.link}|-|{self.date_to_post} {self.time_to_post} {self.time_zone_to_post}|-|{posting_locations_string}|-|{self.attachments}"
        else:
            return f"{self.title}|-|{self.description}|-|{self.link}|-|{self.date_to_post} {self.time_to_post} {self.time_zone_to_post}|-|{posting_locations_string}|-|"


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
            for attachment in self.attachments:
                if not attachment == "[]" or not attachment == "['']" or not attachment == "['\\n']" or not attachment == "\n" or not attachment == "":
                    attachment_clean = attachment.replace("'", "")
                    attachment_clean = attachment_clean.strip("\n")
                    attachment_clean = attachment_clean.strip("][")
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
        try:
            current_time = datetime.now(datetime.strptime(self.time_zone_to_post, '%z').tzinfo)
            if self.datetime_to_post > current_time:
                localfile = open(settings.scheduled_posts_file_location_full, 'a+')
                if localfile:
                    value_to_write = str(self.data_to_list()).replace('\n', '|__NEWLINE__|')
                    key = settings.encryption_key
                    fernet = crypt.get_fernet(key)
                    value_to_write = crypt.encrypt(fernet, str(value_to_write).encode())
                    localfile.write(value_to_write.decode() + '\n')
                    localfile.close()
                return None
        except Exception as e:
            print("Exception while running save as scheduled: ", e)


    ##### SAVE AS PUBLISHED
    def save_as_published(self):
        try:
            localfile = open(settings.published_posts_file_location_full, 'a+')
            if localfile:
                localfile.write(str(self.data_to_list()) + '\n')
                localfile.close()
        except Exception as e:
            print("Exception while running save as published: ", e)      
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
                    
                    ## Clean & Decrypt Line
                    line_clean = line.replace('\n', '')
                    line_clean = line_clean.encode()
                    key = settings.encryption_key
                    fernet = crypt.get_fernet(key)
                    line_clean = crypt.decrypt(fernet, line_clean)

                    ## Parse into Data
                    line_clean_title = line_clean.split('|-|')[0]
                    line_clean_description = line_clean.split('|-|')[1].replace('|__NEWLINE__|', '\n')
                    line_clean_link = line_clean.split('|-|')[2]
                    line_clean_datetime = line_clean.split('|-|')[3]
                    line_clean_date = line_clean.split('|-|')[3].split(' ')[0]
                    line_clean_time = line_clean.split('|-|')[3].split(' ')[1]
                    line_clean_medias = string_to_list(line_clean.split('|-|')[4])

                    ## If you find a match in the file, remove it
                    if line_clean_title == self.title and line_clean_description == self.description and line_clean_link == self.link and line_clean_date == self.date_to_post and line_clean_time == self.time_to_post and line_clean_date == self.date_to_post and line_clean_time == self.time_to_post and line_clean_medias == self.locations_to_post:
                        print('removing line: ', line)
                        lines.remove(line)
                        localfile = open(settings.scheduled_posts_file_location_full, 'w')
                        localfile.writelines(lines)
                        localfile.close()
                        return True
                    else:
                        continue

        except Exception as e:
            print("Exception while running remove from scheduled: ", e)
            return None



########## CREATE POST OBJECT FROM STRING
#####
def create_post_object_from_string(line):

    value = line.encode()
    key = settings.encryption_key
    fernet = crypt.get_fernet(key)
    
    decrypted_line = crypt.decrypt(fernet, value)

    line = decrypted_line

    ##### CREATE DATA FROM LIST
    line = line.split('|-|')
    title = line[0]
    description = line[1]
    link = line[2]
    date_time_array = line[3].split(' ')
    locations_to_post = line[4]
    locations_to_post = locations_to_post.split("|_|")


    ##### CREATE TIME OBJECT
    if date_time_array:
        date = date_time_array[0]
        time = date_time_array[1]
        timezone = date_time_array[2]

    else:
        date = None
        time = None
        timezone = None

    


    ##### CREATE MEDIA / ATTACHMENT OBJECT
    ##### CREATE SCHEDULED POST
    post_object = None
    try: 
        if line[5]:
            attachments = string_to_list(line[5])
            post_object = post(line[0], line[1], line[2], date, time, timezone, locations_to_post,attachments)
        else:
            post_object = post(line[0], line[1], line[2], date, time, timezone, locations_to_post)
    except:
        attachments = None
        post_object = post(line[0], line[1], line[2], date, time, timezone, locations_to_post)

    return post_object



########## GET ALL POSTS
##### (not currently working with encryption)
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
    except Exception as e:
        print("Exception while running get all published: ", e)
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
                    if temp_post:
                        post_data.append(temp_post)
                    else:
                        print('invalid post found')
            else:
                print("Local file not found")
                return None
        else:
            # create scheduled file
            localfile = open(settings.scheduled_posts_file_location_full, 'w')
            print('Created scheduled file')
            return None
    except Exception as e:
        print("Exception while running get all scheduled: ", e)
        return None
    return post_data

