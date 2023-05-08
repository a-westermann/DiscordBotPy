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
    user = None
    try:  # creates a list of dictionary entries that match the allowed_users set
        for key, value in users.items():
            if interaction.user.id == value:
                user = key
    except  Exception as e:
        print("Error: " + str(e))
    # user and user in allowed_users will be None if not found
    return user and user in allowed_users is True
