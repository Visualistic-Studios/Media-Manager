from datetime import datetime


##### CONVERT STRING TO DATETIME OBJECT
def convert_strings_to_datetime(date, time):
    return datetime.strptime(str(date) + ' ' + str(time), '%Y-%m-%d %H:%M:%S')





#string representation of list into list object
def string_to_list(string):
    string = string.strip("[]").split(', ')
    return string