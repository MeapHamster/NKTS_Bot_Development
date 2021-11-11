import requests
import json
import discord

async def Error(Channel, Error_Message):
    embed = discord.Embed(
        title = Error_Message,
        colour = discord.Colour.red()
    )
    await Channel.send(embed = embed)

async def cmd_Hours_User_Invoked(Variables):
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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Hours') == True:
        User_Data_Cards = Get_User_Data_Cards(Trello_Data)
        User_ID = message_txt.split('<@')[1].split('>')[0]
        User_NAME
        for Card in User_Data_Cards:
            if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == User_ID:
                User_NAME = Card['desc'].split('Roblox_Username:')[1].split('\n')[0]
        Hour_Logs_Cards = json.loads(
            requests.request(
                'GET',
                Trello_Data['Hour_Logs']['GET']['URL'],
                headers = Trello_Data['Hour_Logs']['GET']['HEADERS']
            ).text
        )
        for Card in Hour_Logs_Cards:
            if Card['name'] == User_NAME:
                embed = discord.Embed(
                    title = 'NKTS Hour Logs',
                    colour = discord.Colour.gold()
                )
                embed.set_footer(text = '• NKTS Hour Logs')
                embed.add_field(name = 'Logged Hours', value = Card['desc'].split('Hours Logged: ')[1], inline = False)
                await Channel.send(embed = embed)