
#  _____                           _       
# |_   _|                         | |      
#   | | _ __ ___  _ __   ___  _ __| |_ ___ 
#   | || '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| || | | | | | |_) | (_) | |  | |_\__ \
#  \___/_| |_| |_| .__/ \___/|_|   \__|___/
#                | |                       
#                |_|                       
# -----------------------------------------------------------------------     



import os


from datetime import datetime
from resources.config import settings_core
from resources.utility import string_to_list, convert_strings_to_datetime



#  _   _            _       _     _           
# | | | |          (_)     | |   | |          
# | | | | __ _ _ __ _  __ _| |__ | | ___  ___ 
# | | | |/ _` | '__| |/ _` | '_ \| |/ _ \/ __|
# \ \_/ / (_| | |  | | (_| | |_) | |  __/\__ \
#  \___/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/
# -----------------------------------------------------------------------     



settings = settings_core()



# ______                _   _                 
# |  ___|              | | (_)                
# | |_ _   _ _ __   ___| |_ _  ___  _ __  ___ 
# |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | | | |_| | | | | (__| |_| | (_) | | | \__ \
# \_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
# -----------------------------------------------------------------------     



########## CREATE POST OBJECT FROM STRING
#####
def create_post_object_from_string(line):

    value = line.encode()
    
    decrypted_line = settings.crypt.decrypt(value).decode()

    line = decrypted_line

    ##### CREATE DATA FROM LIST
    line = line.split('|-|')

    if len(line) > 0:
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
    else:
        print('invalid line')
        return None


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
##### (not currently working with encryption or S3)
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
    """
    Retrieves all scheduled posts from the file
    """
    post_data = []

    ##### OPEN AND READ FILE
    try:
        with settings.storage.open_file(settings.scheduled_posts_file_location, 'rb') as localfile:
            for line in localfile:
                temp_post = create_post_object_from_string(line.decode())
                if temp_post:
                    post_data.append(temp_post)
                else:
                    print('invalid post found')
                    continue


    ##### FAILURE
    except Exception as e:
        print("Exception while running get all scheduled: ", e)
        return None

    ##### SUCCESS
    return post_data



#  _____ _                         
# /  __ \ |                        
# | /  \/ | __ _ ___ ___  ___  ___ 
# | |   | |/ _` / __/ __|/ _ \/ __|
# | \__/\ | (_| \__ \__ \  __/\__ \
#  \____/_|\__,_|___/___/\___||___/
# -----------------------------------------------------------------------        
                                 


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

        self.accounts_to_post_to = []

        ## Get all unique account names for self.accounts_to_post_to
        for location in self.locations_to_post:
            location_account = location.split('://')[0]
            if location_account not in self.accounts_to_post_to:
                self.accounts_to_post_to.append(location_account)
                
 


        
    

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




    ##### GET ATTACHMENT PATH
    """
    Gets a full attachment path from a file name
    """
    def get_attachment_path(self, attachment_name):
        #attachment_path = settings.full_uploaded_media_dir + "/" + attachment_name
        attachment_path = attachment_name.replace("'", "")
        attachment_path = attachment_path.strip("\n")
        attachment_path = attachment_path.strip("][")
        return attachment_path
    


    ##### LOAD ATTACHMENTS
    def load_attachments(self):
        """
        Loads all attachment paths from the post file
        """
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
                        if not attachment_path == attachment_clean + "/":
                            attachment_list.append(settings.storage.open_file(attachment_clean, 'rb'))
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
                #if os.path.isfile(attachment_path):
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
                #if os.path.isfile(attachment_path):
                attachment_type = attachment_path.split('.')[-1]
                if attachment_type in settings.supported_video_types:
                    video_attachments.append(attachment_path)
        return video_attachments



    ########## GET ALL AUDIO ATTACHMENTS
    #####
    def get_all_audio_attachments(self):
        """
        Returns a list of audio attachments
        """
        audio_attachments = []
        if self.attachments:
            for attachment in self.attachments:
                attachment_path = self.get_attachment_path(attachment)
                #if os.path.isfile(attachment_path):
                attachment_type = attachment_path.split('.')[-1]
                if attachment_type in settings.supported_audio_types:
                    audio_attachments.append(attachment_path)
        return audio_attachments



    ########## SAVE AS SCHEDULED
    #####
    def save_as_scheduled(self):
        try:
            current_time = datetime.now(datetime.strptime(self.time_zone_to_post, '%z').tzinfo)
            if self.datetime_to_post > current_time:
                with settings.storage.open_file(settings.scheduled_posts_file_location, 'ab') as localfile:
                    value_to_write = str(self.data_to_list()).replace('\n', '|__NEWLINE__|')
                    value_to_write = settings.crypt.encrypt(str(value_to_write).encode())
                    localfile.write(value_to_write)
                    localfile.write(b'\n')
                    
                return None
        except Exception as e:
            print("Exception while running save as scheduled: ", e)





    ########## SAVE AS PUBLISHED
    #####
    def save_as_published(self):
        try:
            ## probably need to implement a check to see if the post is already published
            with settings.storage.open_file(settings.published_posts_file_location, 'ab') as localfile:
                value_to_write = str(self.data_to_list()).replace('\n', '|__NEWLINE__|')
                value_to_write = settings.crypt.encrypt(str(value_to_write).encode())
                localfile.write(value_to_write)
                localfile.write(b'\n')
                    
                return True
        except Exception as e:
            print("Exception while running save as published: ", e)




    ########## GET CURRENT TIME IN TIMEZONE
    #####
    def get_current_time_in_timezone(self):
        """
        Returns the post time in UTC
        """
        try:
            current_time = datetime.now(datetime.strptime(self.time_zone_to_post, '%z').tzinfo) ## Gets time in the selected time zone
            return current_time
        except Exception as e:
            print(e)

        

    ########## REMOVE FROM SCHEDULED FILE
    #####
    def remove_from_scheduled(self):
        """
        Removes a post from the scheduled file 
        """
        try:
            lines = None
            lines_original_length = 0
            
            localfile = settings.storage.open_file(settings.scheduled_posts_file_location, 'rb')
            lines = localfile.readlines()
            lines_original_length = len(lines)
            localfile.close()


            for line in lines:
                
                ## Clean & Decrypt Line
                line_clean = line.replace(b'\n', b'')
                line_clean = settings.crypt.decrypt(line_clean).decode()

                ## Parse into Data
                line_clean_title = line_clean.split('|-|')[0]
                line_clean_description = line_clean.split('|-|')[1].replace('|__NEWLINE__|', '\n')
                line_clean_link = line_clean.split('|-|')[2]
                line_clean_datetime = line_clean.split('|-|')[3]
                line_clean_date = line_clean.split('|-|')[3].split(' ')[0]
                line_clean_time = line_clean.split('|-|')[3].split(' ')[1]
                line_clean_medias = string_to_list(line_clean.split('|-|')[4])


                # print('line clean title: ', type(line_clean_title))
                # print('self title: ', type(self.title))
                # print('line clean description: ', line_clean_description)
                # print('self description: ', self.description)
                # print('line clean link: ', line_clean_link)
                # print('self link: ', self.link)
                # print('line clean datetime: ', line_clean_datetime)
                # print('self datetime: ', self.datetime_to_post)
                # print('line clean date: ', line_clean_date)
                # print('self date: ', self.date_to_post)
                # print('line clean time: ', line_clean_time)
                # print('self time: ', self.time_to_post)
                # print('line clean medias: ', line_clean_medias)
                # print('self medias: ', self.attachments)


                ## If you find a match in the file, remove it
                if line_clean_title == self.title and line_clean_date == self.date_to_post and line_clean_time == self.time_to_post: # | This is temporary. Posts need a new data element; ID
                    print('removing line: ', line)
                    lines.remove(line)
                    break
                else:
                    continue
            

            ##### IF CHANGES WERE MADE, WRITE BACK TO FILE
            if lines:
                if lines_original_length != len(lines):
                    with settings.storage.open_file(settings.scheduled_posts_file_location, 'wb') as localfile:
                        localfile.writelines(lines)
                        localfile.close()
                        return True
                else:
                    return False
            else:
                with settings.storage.open_file(settings.scheduled_posts_file_location, 'wb') as localfile:
                        localfile.writelines(lines)
                        localfile.close()
                        return True

        except Exception as e:
            print("Exception while running remove from scheduled: ", e)
            return None



    ########## PUBLISH
    #####
    def publish(self):
        """
        Publishes the post to the desired social media
        """
        try:

            ## TODO: Actually publish this to the social media here. Currently just saves to the published file
            was_published = True ## HERE
            was_saved_as_published = self.save_as_published()
            
            if was_published and was_saved_as_published:
                self.remove_from_scheduled()
                print('Post published')
                return True
            else:
                print('Post not published')
                return False
            
        except Exception as e:
            print("Exception while running publish: ", e)
            return None


    def get_social_media_unique_names(self):
        """
        Returns the unique name of each social media to be used in the post
        """
        try:
            
            names = []

            for location in self.locations_to_post:
                names.append(location.split('://')[0])

        except Exception as e:
            print("Exception while running get social media unique name: ", e)
            return None


    def get_posting_locations(self):
        """
        Returns the locations to post to
        """
        try:
            locations = []

            for location in self.locations_to_post:
                locations.append(location.split('://')[-1])

            return locations

        except Exception as e:
            print("Exception while running get posting locations: ", e)
            return None

        
    def get_locations_for_account(self, account_name):
        """
        Returns the locations to post to on a specific platform.
        """
        try:
            locations = []

            for location in self.locations_to_post:
                if str(account_name.lower())==location.split('://')[0].lower():
                    locations.append(location)

            return locations

        except Exception as e:
            print("Exception while running get locations on platform: ", e)
            return None
