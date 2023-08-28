from datetime import datetime as dt, timedelta
import datetime
import random
import helpers
from discord.ext import commands
from discord import app_commands
import discord.ext
import discord
import asyncio


class BabyStuff:
    def __init__(self, command_module):
        self.command_module = command_module
        # self.helpers = helpers()


    def read_file(self, path):
        file = open(path, "r")
        return file

    async def get_todays_name(self):
        # check date to see if gave one already
        today = helpers.get_date_hour()
        used_names_file = self.read_file("/home/andweste/Scripts/used_names.txt")
        last_date = str(used_names_file.readline().rstrip())
        print("today = " + str(today))
        print("last time = " + last_date)
        times_for_names = [00, 12, 17]  # midnight, noon, 5pm
        last_time = last_date.split(' ')[1].split(':')[0]
        # find the last time and get the next one
        last_time_index = times_for_names.index(list(filter(lambda t: t == int(last_time), times_for_names))[0])
        new_time = times_for_names[0] if last_time_index == 2 else times_for_names[(last_time_index + 1)]
        new_day = str((datetime.datetime.strptime(last_date, "%Y-%m-%d %H:%M:%S")
                      + timedelta(days=1))).split(' ')[0] if last_time_index == 2 else last_date.split(' ')[0]
        new_date = new_day + " " + str(new_time) + ":00:00"
        print("new date = " + new_date)
        got_new_name = None
        if today <= datetime.datetime.strptime(new_date, "%Y-%m-%d %H:%M:%S"):  # give last name
            line = ""
            for name in used_names_file:
                line = name
                pass
            last_name = line.split(';')[0]  # split on the score delimiter
            print("Already got a name today. Name =" + last_name)
            got_new_name = False
            return last_name, got_new_name
        else:  # if not, pull random name from file, remove it, and add to alt file
            names_list_file = open("/home/andweste/Scripts/girl_names.txt", "r")
            name_list = names_list_file.readlines()
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
            used_names_file.close()
            # build the next datetime based on TODAY's date, plus the last time that was eligible for a name
            # that way if you miss days you can't just do a bunch after missing
            if str(today).split(' ')[0] == new_date.split(' ')[0]:
                # last day recorded == today
                time_to_record = str(new_time)
            else:  # last day was from previous date. Grab today + last time limit
                current_time = int(str(today).split(' ')[1].split(':')[0])
                print(str(current_time) + "  current time")
                if times_for_names[1] > current_time > times_for_names[0]:
                    time_to_record = "00"
                elif times_for_names[2] > current_time > times_for_names[1]:
                    time_to_record = str(times_for_names[1])
                else:
                    time_to_record = str(times_for_names[2])
            # always use today's date as the last recorded time
            last_used_datetime = str(today).split(' ')[0] + " " + time_to_record + ":00:00"
            used_names_text = used_names_text.replace(last_date, last_used_datetime)
            used_names_file = open("/home/andweste/Scripts/used_names.txt", "w") # open in write, clear text
            used_names_file.writelines(used_names_text)  # write all names
            used_names_file.close()
            used_names_file = open("/home/andweste/Scripts/used_names.txt", "a")  # open in append mode to add name
            used_names_file.write(todays_name.strip() + ";0;0\n")
            used_names_file.close()
            got_new_name = True
            return todays_name, got_new_name


    async def submit_name_score(self, score: int, name: str, view: discord.Interaction, rater: str):
        print("submitting score for " + rater + ".... " + str(score))
        try:  # write score to the used_names.txt
            used_names_file = open("/home/andweste/Scripts/used_names.txt", "r")
            text = used_names_file.readlines()
            final_name_line = text[len(text) - 1].strip()
            final_name = final_name_line.split(';')[0]
            ashley_score = final_name_line.split(';')[1]
            andrew_score = final_name_line.split(';')[2]
            if rater == "Ashley":
                text[len(text) - 1] = final_name + ";" + str(score) + ";" + andrew_score + "\n"
            elif rater == "Andrew":
                text[len(text) - 1] = final_name + ";" + ashley_score + ";" + str(score) + "\n"
            used_names_file = open("/home/andweste/Scripts/used_names.txt", "w")
            used_names_file.writelines(text)
            used_names_file.close()
            await view.response.send_message(rater + "'s " + "score submitted for " + name + " : " + str(score))
            await view.message.delete()
        except Exception as e:
            await view.response.send_message("Unable to submit score. Please try again. Or don't, I don't know."\
                                             + "\n" + str(e))

    def backup_names(self, used_file: bool):
        file_to_backup = "used_names.txt" if used_file else "girl_names.txt"
        used_names_file = open(file_to_backup, "r").readlines()
        date_string = str(datetime.date.today())
        backup_path = "used_names_backups/used_names.txt.backup_" if used_file else \
                "girl_names_backups/girl_names.txt.backup_"
        backup_file = open(backup_path + date_string, "w")
        backup_file.writelines(used_names_file)

    async def submit_previous_name_score(self, score: int, name: str, view: discord.Interaction, rater: str):
        print("Updating score for name: " + name + " to " + str(score))
        used_names_file = open("/home/andweste/Scripts/used_names.txt", "r")
        text = used_names_file.read()
        used_names_file.close()
        # add 2 or 4 depending on who is rating
        score_index = 2 if rater == "Ashley" else 4
        print(f'finding {name};')
        char_to_replace = text.find(f'{name};') + len(name) + score_index
        print(f'chars to replace index = {char_to_replace}')
        next_char = '\n' if rater == "Andrew" else ';'
        text = text[:char_to_replace - 1] + str(score) + next_char + text[char_to_replace + 1:]
        used_names_file = open("/home/andweste/Scripts/used_names.txt", "w").write(text)
        await view.response.send_message(rater + "'s " + "score submitted for " + name + " : " + str(score))
        await view.message.delete()

    async def score_specific_name(self, name: str, score: int, interaction: discord.Interaction):
        rater = helpers.get_user_name(interaction)
        try:
            self.backup_names(used_file=False)
            girl_names = open("/home/andweste/Scripts/girl_names.txt", "r")
            text = girl_names.readlines()
            girl_names.close()
            after_edit_lines = []
            for line in text:
                if line.strip("\n").lower() != name.lower():
                    after_edit_lines.append(line)
            if len(after_edit_lines) == len(text):
                print(f"Name:{name} was not found on the list.")
            girl_names = open("/home/andweste/Scripts/girl_names.txt", "w")
            girl_names.writelines(after_edit_lines)
            girl_names.close()
        except:
            return False
        # now add the name to used_names
        try:
            self.backup_names(used_file=True)
            used_names_file = open("/home/andweste/Scripts/used_names.txt", "a")  # open in append mode to add name
            score_texts = f";{score};0\n" if rater == "Naiyvara" else f";0;{score}\n"
            formatted_name = name.capitalize().strip(' ')
            used_names_file.write(formatted_name + score_texts)
            used_names_file.close()
        except:
            return False
        return True

