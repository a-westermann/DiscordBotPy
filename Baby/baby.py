import datetime
import random


class BabyStuff:
    def __init__(self, command_module):
        self.command_module = command_module


    def get_todays_name(self):
        # check date to see if gave one already
        today = str(datetime.date.today())
        used_names_file = open("/home/andweste/Scripts/used_names.txt", "r")
        last_date = str(used_names_file.readline().rstrip())
        print("prev date = " + last_date)
        print("today = " + today)
        if today == last_date:
            # if so, give bottom name from used_names file
            line = ""
            for name in used_names_file:
                line = name
                pass
            last_name = line
            print("Already got a name today. Name =" + last_name)
            return last_name
        else:  # if not, pull random name from file, remove it, and add to alt file
            names_list_file = open("/home/andweste/Scripts/girl_names.txt", "r")
            name_list = names_list_file.readlines()
            # read().split("\n")
            todays_name = random.choice(name_list)
            print("today's name = " + todays_name)
            # now remove the name from list and write to the file
            name_list.remove(todays_name)
            names_list_file = open("/home/andweste/Scripts/girl_names.txt", "w")  # opening in write mode clears file
            for name in name_list:
                names_list_file.write(f"{name}")
            # finally, add the new name to the bottom of the used_names file
            used_names_file = open("/home/andweste/Scripts/used_names.txt", "r")  # open in read
            used_names_text = used_names_file.read()
            used_names_text = used_names_text.replace(last_date, today)
            used_names_file = open("/home/andweste/Scripts/used_names.txt", "w") # open in write, clear text
            used_names_file.writelines(used_names_text)  # write all names
            used_names_file = open("/home/andweste/Scripts/used_names.txt", "a")  # open in append mode to add name
            used_names_file.write(todays_name)
        return todays_name
