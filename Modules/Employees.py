import discord
import requests
import json

async def cmd_Employees_Invoked(Variables):
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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Employees') == True:
        UserDataCards = Get_User_Data_Cards(Trello_Data)
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
        EmployeeList = []
        TrainingList = []
        for Card in Employee_Cards:
            EmployeeList.append(Card['name'])
        for Card in Management_Cards:
            EmployeeList.append(Card['name'])
        for Card in Training_Cards:
            TrainingList.append(Card['name'])

        for User in Training:
            print(User)
                
            Employees_String = ''
            Training_String = ''

            for User in EmployeeList:
                Employee_String = Employee_String + User + '/n'

            for User in TrainingList:
                Training_String = Training_String + User + '/n'

            embed = discord.Embed(
                title = 'NKTS Employee Tracker',
                description = '**Employees:**\n<@!' + Employee_String + '\n\nTraining' + Training_String,
                colour = discord.Colour.gold()
            )
                
            embed.set_footer(text = '• NKTS Employee Tracker')
            await Channel.send(embed = embed)