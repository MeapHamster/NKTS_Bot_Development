import discord
import requests
import json

async def cmd_Fire_Employee_Invoked(Variables):
    # Variables #
    client              = Variables['client']
    message             = Variables['message']
    MAIN_VARIABLES      = Variables['MAIN_VARIABLES']
    Channel_Whitelist   = Variables['Channel_Whitelist']
    Command_Whitelists  = Variables['Command_Whitelists']
    Check_Command       = Variables['Check_Command']
    Get_User_Data_Cards = Variables['Get_User_Data_Cards']
    Trello_Data         = Variables['Trello_Data']
    # Variables #
    Channel = client.get_channel(message.channel.id)
    message_txt = message.content
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Fire Employee') == True:
        UserDataCards = Get_User_Data_Cards(Trello_Data)
        User_ID = message_txt.split('<@!')[1].split('>')[0]
        Found_Data_Card = False
        Already_Employee = False
        Username = ''
        for Card in UserDataCards:
            if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == User_ID:
                Username = Card['name']
                Found_Data_Card = True
        if Found_Data_Card == True:
            Employee_Cards = json.loads(
                requests.request(
                    'GET',
                    Trello_Data['Employee_Tracker_Employees']['GET']['URL'],
                    headers = Trello_Data['Employee_Tracker_Employees']['GET']['HEADERS']
                ).text
            )
            Management_Cards = json.loads(
                requests.request(
                    'GET',
                    Trello_Data['Employee_Tracker_Management']['GET']['URL'],
                    headers = Trello_Data['Employee_Tracker_Management']['GET']['HEADERS']
                ).text
            )
            Training_Cards = json.loads(
                requests.request(
                    'GET',
                    Trello_Data['Employee_Tracker_Training']['GET']['URL'],
                    headers = Trello_Data['Employee_Tracker_Training']['GET']['HEADERS']
                ).text
            )
            Employee_Card = ''
            for Card in Employee_Cards:
                if Card['name'] == Username:
                    Employee_Card = Card['id']
            if Employee_Card == '':
                for Card in Management_Cards:
                    if Card['name'] == Username:
                        Employee_Card = Card['id']
            if Employee_Card == '':
                for Card in Training_Cards:
                    if Card['name'] == Username:
                        Employee_Card = Card['id']
            if Employee_Card != '':
                Delete_Employee_Card = requests.request(
                    'DELETE',
                    'https://api.trello.com/1/cards/' + Employee_Card,
                    params = {
                        'key': Trello_Data['TRELLO_KEY'],
                        'token': Trello_Data['TRELLO_TOKEN']
                    }
                )
                embed = discord.Embed(
                    title = 'Employee Fired',
                    description = 'Employee: ' + Username,
                    colour = discord.Colour.red()
                )
                await Channel.send(embed = embed)
                Roles = [
                    discord.utils.get(message.guild.roles, name = 'Supervisor'),
                    discord.utils.get(message.guild.roles, name = 'Division Manager'),
                    discord.utils.get(message.guild.roles, name = 'Head Driving Instructor'),
                    discord.utils.get(message.guild.roles, name = 'Training Manager'),
                    discord.utils.get(message.guild.roles, name = 'Driving Instructor'),
                    discord.utils.get(message.guild.roles, name = 'Classroom Instructor'),
                    discord.utils.get(message.guild.roles, name = 'Head of Piloting'),
                    discord.utils.get(message.guild.roles, name = 'Taxi Pilot'),
                    discord.utils.get(message.guild.roles, name = 'Head of Boating'),
                    discord.utils.get(message.guild.roles, name = 'Ferry Captain'),
                    discord.utils.get(message.guild.roles, name = 'Ferry Crew'),
                    discord.utils.get(message.guild.roles, name = 'Taxi Driver'),
                    discord.utils.get(message.guild.roles, name = 'Custodial Manager'),
                    discord.utils.get(message.guild.roles, name = 'Custodian'),
                    discord.utils.get(message.guild.roles, name = 'Front Desk Manager'),
                    discord.utils.get(message.guild.roles, name = 'Front Desk'),
                    discord.utils.get(message.guild.roles, name = 'Marketing Manager'),
                    discord.utils.get(message.guild.roles, name = 'Employee'),
                    discord.utils.get(message.guild.roles, name = '[T] Taxi Driver'),
                    discord.utils.get(message.guild.roles, name = '[T] Front Desk'),
                    discord.utils.get(message.guild.roles, name = '[T] Custodian'),
                    discord.utils.get(message.guild.roles, name = 'Employee in Training'),
                    discord.utils.get(message.guild.roles, name = 'Pilot in Training'),
                    discord.utils.get(message.guild.roles, name = 'Uncertified Driver'),
                    discord.utils.get(message.guild.roles, name = 'Classroom Needed'),
                ]
                await message.author.remove_roles(*Roles)
            else:
                embed = discord.Embed(
                    title = 'Bruh... that guy isn\'t employed',
                    description = 'User: ' + Username,
                    colour = discord.Colour.red()
                )
                await Channel.send(embed = embed)