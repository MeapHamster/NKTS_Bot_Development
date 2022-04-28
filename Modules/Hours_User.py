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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Hours <@!') == True:
        User_Data_Cards = Get_User_Data_Cards(Trello_Data)
        User_ID = message_txt.split('<@!')[1].split('>')[0]
        User_NAME = ''
        for Card in User_Data_Cards:
            if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == User_ID:
                User_NAME = Card['desc'].split('Account_Username:')[1].split('\n')[0]
        Hour_Logs_Cards = json.loads(
            requests.request(
                'GET',
                Trello_Data['Hour_Logs']['GET']['URL'],
                headers = Trello_Data['Hour_Logs']['GET']['HEADERS']
            ).text
        )
        if len(Hour_Logs_Cards) > 0:
            Found_Log_Card = False
            for Card in Hour_Logs_Cards:
                if Card['name'] == User_NAME:
                    Found_Log_Card = True
                    embed = discord.Embed(
                        title = 'NKTS Hour Logs',
                        description = '**Logged Hours for <@!' + User_ID + '>**\n' + Card['desc'].split('Hours Logged: ')[1],
                        colour = discord.Colour.gold()
                    )
                    embed.set_footer(text = '• NKTS Hour Logs')
                    await Channel.send(embed = embed)
            if Found_Log_Card == False:
                embed = discord.Embed(
                    title = 'NKTS Hour Logs',
                    description = 'No shift logs found for user <@!' + User_ID + '>!',
                    colour = discord.Colour.gold()
                )
                embed.set_footer(text = '• NKTS Hour Logs')
                await Channel.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'NKTS Hour Logs',
                description = 'No hours have been logged for any users!',
                colour = discord.Colour.gold()
            )
            embed.set_footer(text = '• NKTS Hour Logs')
            await Channel.send(embed = embed)