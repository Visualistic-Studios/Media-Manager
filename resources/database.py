#  _____                           _       
# |_   _|                         | |      
#   | | _ __ ___  _ __   ___  _ __| |_ ___ 
#   | || '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| || | | | | | |_) | (_) | |  | |_\__ \
#  \___/_| |_| |_| .__/ \___/|_|   \__|___/
#                | |                       
#                |_|                       
# -----------------------------------------------------------------------   



import s3fs



#  _____ _                         
# /  __ \ |                        
# | /  \/ | __ _ ___ ___  ___  ___ 
# | |   | |/ _` / __/ __|/ _ \/ __|
# | \__/\ | (_| \__ \__ \  __/\__ \
#  \____/_|\__,_|___/___/\___||___/
# -----------------------------------------------------------------------        



########## GENERIC STORAGE CLASS
#####
class Storage:


    ##### INIT
    def __init__(self, s3_access, s3_secret, s3_endpoint, bucket_name):
        self.bucket_name = bucket_name
        self.s3_access = s3_access
        self.s3_secret = s3_secret
        self.s3_endpoint = s3_endpoint
        
        ## Create a connection to the bucket
        if self.s3_access and self.s3_secret and self.s3_endpoint:
            self.connection = s3fs.S3FileSystem(
                anon=False,
                key=self.s3_access,
                secret=self.s3_secret,
                client_kwargs={'endpoint_url': self.s3_endpoint}
            )
        else: 
            self.connection = None


    ##### GET BUCKET
    def get_bucket(self):
        if self.connection:
            return self.connection.get_bucket(self.bucket_name)


    ##### OPEN FILE
    def open_file(self, file_name, mode):
        if self.connection:
            return self.connection.open(self.bucket_name + '/' + file_name, mode)


    ##### GET FILE SIZE
    def get_file_size(self, file_name):
        if self.connection:
            return self.connection.info(self.bucket_name + '/' + file_name)['ContentLength']


    ##### GET FILE LIST
    def get_file_list(self):
        if self.connection:
            return self.connection.ls(self.bucket_name)


    ##### GET FILE LIST WITH SIZE
    def get_file_list_with_size(self):
        if self.connection:
            return self.connection.ls(self.bucket_name, detail=True)


    ##### GET FFILE LIST WITH SIZE AND TIME
    def get_file_list_with_size_and_time(self):
        if self.connection:
            return self.connection.ls(self.bucket_name, detail=True, headers=True)



    ##### DOES FILE EXIST
    def does_file_exist(self, file):
        try: 
            check = self.open_file(file, 'r')
            if check:
                return True
        except:
            return False  

