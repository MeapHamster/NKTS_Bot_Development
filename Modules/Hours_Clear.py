import requests
import json
import discord

async def cmd_Hours_Clear_Invoked(Variables):
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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Hours Clear') == True:
        Hour_Logs_Cards = json.loads(
            requests.request(
                'GET',
                Trello_Data['Hour_Logs']['GET']['URL'],
                headers = Trello_Data['Hour_Logs']['GET']['HEADERS']
            ).text
        )
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
        
        EMPLOYEES = []

        EMPLOYEES_LOGGED = []
        EMPLOYEES_FAILED = []
        EMPLOYEES_TO_PAY = []

        for User in Employee_Cards:
            EMPLOYEES.append(User['name'])
        for User in Management_Cards:
            EMPLOYEES.append(User['name'])
        print(EMPLOYEES)
        for Card in Hour_Logs_Cards:
            EMPLOYEES_LOGGED.append(Card['name'] + ' - ' + Card['desc'].split('Hours Logged: ')[1]) # ADD EMPLOYEE TO LIST OF USERS WHO LOGGED
            for User in EMPLOYEES:
                if Card['name'] == User:
                    TIME_LOGGED = Card['desc']
                    LOGGED_ENOUGH_TIME = False
                    TIME = TIME_LOGGED.split('Hours Logged: ')[1].split(':')
                    if int(TIME[0]) >= MAIN_VARIABLES['MINIMUM_HOURS']:
                        LOGGED_ENOUGH_TIME = True
                    if LOGGED_ENOUGH_TIME == True:
                        EMPLOYEES_TO_PAY.append(Card['name'] + ' - ' + Card['desc'].split('Hours Logged: ')[1]) # ADD EMPLOYEE TO LIST OF USERS WHO GET PAID FOR THE WEEK
        for Employee in EMPLOYEES:
            LOGGED = False
            for User in EMPLOYEES_LOGGED:
                if User.split(' - ')[0] == Employee:
                    LOGGED = True
            if LOGGED == False:
                EMPLOYEES_FAILED.append(Employee)

        EMPLOYEES_LOGGED_STRING = 'None'
        EMPLOYEES_FAILED_STRING = 'None'
        EMPLOYEES_TO_PAY_STRING = 'None'

        for User in EMPLOYEES_LOGGED:
            if EMPLOYEES_LOGGED_STRING == 'None':  
                EMPLOYEES_LOGGED_STRING = ''
            EMPLOYEES_LOGGED_STRING = EMPLOYEES_LOGGED_STRING + '\n' + User

        for User in EMPLOYEES_FAILED:
            if EMPLOYEES_FAILED_STRING == 'None':  
                EMPLOYEES_FAILED_STRING = ''
            EMPLOYEES_FAILED_STRING = EMPLOYEES_FAILED_STRING + '\n' + User

        for User in EMPLOYEES_TO_PAY:
            if EMPLOYEES_TO_PAY_STRING == 'None':  
                EMPLOYEES_TO_PAY_STRING = ''
            EMPLOYEES_TO_PAY_STRING = EMPLOYEES_TO_PAY_STRING + '\n' + User

        embed = discord.Embed(
            title = 'NKTS Hour Logs',
            colour = discord.Colour.gold()
        )
        embed.set_footer(text = '• NKTS Hour Logs')
        embed.add_field(name = 'Logged Hours', value = EMPLOYEES_LOGGED_STRING, inline = False)
        embed.add_field(name = 'Failed to Log Hours', value = EMPLOYEES_FAILED_STRING, inline = False)
        embed.add_field(name = 'Meets Weekly Quota', value = EMPLOYEES_TO_PAY_STRING, inline = False)
        await client.get_channel(904465317055590480).send(embed = embed)

        # Duplicate cards to a new list

        Delete_Cards = requests.request(
            'POST',
            'https://api.trello.com/1/lists',
            params = {
                'key': Trello_Data['TRELLO_KEY'],
                'token': Trello_Data['TRELLO_TOKEN'],
                'name': 'Archive [00/00/00- 00/00/00]',
                'idBoard': '6064bcbe4eba3a37e533f49c',
                'idListSource': Trello_Data['Hour_Logs']['POST']['IDLIST']
            }
        )

        # Delete cards from current list

        for Hour_Log in Hour_Logs_Cards:
            Delete_Hour_Log_Card = requests.request(
                'DELETE',
                'https://api.trello.com/1/cards/' + Hour_Log['id'],
                params = {
                    'key': Trello_Data['TRELLO_KEY'],
                    'token': Trello_Data['TRELLO_TOKEN']
                }
            )

        embed = discord.Embed(
            title = "Successfully cleared shift logs!",
            colour = discord.Colour.gold()
        )
        embed.set_footer(text = '• NKTS')
        await Channel.send(embed=embed)