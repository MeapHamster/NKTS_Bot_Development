import discord
import requests
import json

async def cmd_User_Info_Invoked(Variables):
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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Info') == True:
        UserDataCards = Get_User_Data_Cards(Trello_Data)
        User_ID = message_txt.split('<@!')[1].split('>')[0]
        Found_Data_Card = False
        Username = ''
        for Card in UserDataCards:
            if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == User_ID:
                Username = Card['name']
                Found_Data_Card = True
        if Found_Data_Card == True:
            print('Command Invoked')