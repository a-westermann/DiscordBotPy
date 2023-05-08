from googlesearch import search
from datetime import datetime
import discord


users = { "Vierce":111 , "Naiyvara":879464051267223572,
    "ComradeGiraffe":159815678508007424 , "The Great Ratsby":157183377089363969 , "GoldForce":238467012399988738 }



# General functions
def google_search(search_term, num_results):
    for url in search(search_term, num_results=num_results):
        return url


def get_date_hour():
    today = datetime.today()
    # strip off the milliseconds then convert back to datetime
    simple_today = datetime.strptime(str(today).split('.')[0], "%Y-%m-%d %H:%M:%S")
    return simple_today


def check_user(interaction: discord.Interaction, allowed_users: []):
    try:  # creates a list of dictionary entries that match the allowed_users set
        allowed_ids = [id for key in allowed_users if key in users for id in users[key]]
    except  Exception as e:
        print("Error: " + str(e))  # key not in dict
        return false
    return interaction.author.id in allowed_ids
    # user_name = list(users.keys())[list(users.values()).index(interaction.author.id)]
