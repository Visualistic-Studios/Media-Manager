from datetime import datetime


##### CONVERT STRING TO DATETIME OBJECT
def convert_strings_to_datetime(date, time, timezone):
    return datetime.strptime(str(date) + ' ' + str(time) + ' ' + str(timezone), '%Y-%m-%d %H:%M:%S %z')



#string representation of list into list object
def string_to_list(string):
    string = string.strip("[]").split(', ')
    return string



# string to list of dictionaries
def string_to_list_of_dictionaries(string):


    # split string into list of dictionaries
    string = string.replace("},", "}|--|")
    list = string.split("|--|")

    list_of_dictionaries = []

    # make dictionary string a dictionary object
    for string_dict in list:
        string_dict = string_dict.replace("[", "") # remove [
        string_dict = string_dict.replace("]", "") # remove ]
        list_of_dictionaries.append(eval(string_dict))

    return list_of_dictionaries