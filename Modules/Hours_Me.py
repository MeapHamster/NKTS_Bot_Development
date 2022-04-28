import requests
import json
import discord

async def Error(Channel, Error_Message):
    embed = discord.Embed(
        title = Error_Message,
        colour = discord.Colour.red()
    )
    await Channel.send(embed = embed)

async def cmd_Hours_Me_Invoked(Variables):
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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Hours Me') == True:
        User_Data_Cards = Get_User_Data_Cards(Trello_Data)
        Username = ''
        Data_Card_Found = False
        for Card in User_Data_Cards:
            if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == str(message.author.id):
                Data_Card_Found = True
                Username = Card['desc'].split('Account_Username:')[1].split('\n')[0]
        if Data_Card_Found == True:
            Hour_Logs_Cards = json.loads(
                requests.request(
                    'GET',
                    Trello_Data['Hour_Logs']['GET']['URL'],
                    headers = Trello_Data['Hour_Logs']['GET']['HEADERS']
                ).text
            )
            HOURS_LOGGED = False
            LOGGED = 'Error'
            for Log in Hour_Logs_Cards:
                if Log['name'] == Username:
                    HOURS_LOGGED = True
                    LOGGED = Log['desc'].split('Hours Logged: ')[1]
            if HOURS_LOGGED == True:
                embed = discord.Embed(
                    title = 'NKTS Hour Logs',
                    description = '**Hours Logged for:**\n' + Username + '\n' + LOGGED,
                    colour = discord.Colour.gold()
                )
                embed.set_footer(text = '• NKTS Hour Logs')
                await Channel.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = 'No hours have been logged!',
                    description = 'User: ' + Username,
                    colour = discord.Colour.gold()
                )
                embed.set_footer(text = '• NKTS Hour Logs')
                await Channel.send(embed = embed)
        else:
            await Error(Channel, 'Data Card not found. Please run !Link Account in the bot commands channel.')