from datetime import datetime
import random
import helpers


class BabyStuff:
    def __init__(self, command_module):
        self.command_module = command_module
        # self.helpers = helpers()


    def get_todays_name(self):
        # check date to see if gave one already
        today = helpers.get_date_hour()
        used_names_file = open("/home/andweste/Scripts/used_names.txt", "r")
        last_date = str(used_names_file.readline().rstrip())
        print("today = " + str(today))
        print("last time = " + last_date)
        times_for_names = [00, 12, 17]  # midnight, noon, 5pm
        last_time = last_date.split(' ')[1].split(':')[0]
        # find the last time and get the next one
        last_time_index = times_for_names.index(list(filter(lambda t: t == int(last_time), times_for_names))[0])
        new_time = times_for_names[0] if last_time_index == 2 else times_for_names[(last_time_index + 1)]
        new_date = last_date.split(' ')[0] + " " + str(new_time) + ":00:00"
        print("new date = " + new_date)
        if today <= datetime.strptime(new_date, "%Y-%m-%d %H:%M:%S"):  # give last name
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
            # build the next datetime based on TODAY's date, plus the new time
            # that way if you miss days you can't just do a bunch after missing
            new_date = str(today).split(' ')[0] + " " + str(new_date).split(' ')[1]
            used_names_text = used_names_text.replace(last_date, today)
            used_names_file = open("/home/andweste/Scripts/used_names.txt", "w") # open in write, clear text
            used_names_file.writelines(used_names_text)  # write all names
            used_names_file = open("/home/andweste/Scripts/used_names.txt", "a")  # open in append mode to add name
            used_names_file.write(todays_name)
        return todays_name
