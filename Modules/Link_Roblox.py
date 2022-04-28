import requests
import json
import discord

async def cmd_Link_Account_Invoked(Variables):
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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Link Account') == True:
        User_Data_Cards = Get_User_Data_Cards(Trello_Data)
        Username = message.author.name
        if message.author.nick:
            Username = message.author.nick
        Found_Card = False
        for Card in User_Data_Cards:
            if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == str(message.author.id):
                Found_Card = True
        if Found_Card == False:
            Create_User_Data_Card = requests.request(
                'POST',
                Trello_Data['User_Data_Cards']['POST']['URL'],
                params = {
                    'key': Trello_Data['TRELLO_KEY'],
                    'token': Trello_Data['TRELLO_TOKEN'],
                    'idList': Trello_Data['User_Data_Cards']['POST']['IDLIST'],
                    'name': Username,
                    'desc': 'Discord_User_ID:' + str(message.author.id) + '\nAccount_Username:' + Username + '\nEmail_Address:\nPhone_Number:'
                }
            ).text
            if Create_User_Data_Card == '200':
                await Channel.send('Something went wrong! Please try again or contact support!')
            else:
                await Channel.send('Success!')
        else:
            await Channel.send('Data already exists for user!')