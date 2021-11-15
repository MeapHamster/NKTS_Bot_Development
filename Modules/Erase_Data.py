import requests
import json
import discord

async def cmd_Erase_Data_Invoked(Variables):
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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Erase Data') == True:
        User_Data_Cards = Get_User_Data_Cards(Trello_Data)
        Found_User_Data_Card = False
        for Card in User_Data_Cards:
            if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == str(message.author.id):
                Found_User_Data_Card = True
                Delete_User_Data_Card = requests.request(
                    'DELETE',
                    'https://api.trello.com/1/cards/' + Card['id'],
                    params = {
                        'key': Trello_Data['TRELLO_KEY'],
                        'token': Trello_Data['TRELLO_TOKEN']
                    }
                )
                Discord_User_ID_ARCHIVE = Card['desc'].split('Discord_User_ID:')[1].split('\n')[0]
                Roblox_Username_ARCHIVE = Card['desc'].split('Roblox_Username:')[1].split('\n')[0]
                Email_Address_ARCHIVE = Card['desc'].split('Email_Address:')[1].split('\n')[0]
                embed = discord.Embed(
                    title = 'User Data Erased',
                    description = '**Archive:**',
                    colour = discord.Colour.gold()
                )
                embed.set_footer(text = '• NKTS Secure Data')
                embed.add_field(name = 'Discord User ID', value = Discord_User_ID_ARCHIVE, inline = False)
                embed.add_field(name = 'Roblox Username', value = Roblox_Username_ARCHIVE, inline = False)
                embed.add_field(name = 'Email Address', value = Email_Address_ARCHIVE, inline = False)
                await Channel.send(embed = embed)
        if Found_User_Data_Card == False:
            embed = discord.Embed(
                title = 'You blew up the internet.',
                description = "We couldn't find a data card for you! Try running `!Link Roblox` in <#865637391808724992>",
                colour = discord.Colour.gold()
            )
            embed.set_footer(text = '• NKTS')
            await Channel.send(embed = embed)