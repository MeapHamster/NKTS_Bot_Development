import requests
import json
import discord

async def cmd_View_Data_Invoked(Variables):
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
    DM_Channel = await message.author.create_dm()
    message_txt = message.content
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'View Data') == True:
        User_Data_Cards = Get_User_Data_Cards(Trello_Data)
        Found_User_Data_Card = False
        for Card in User_Data_Cards:
            if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == str(message.author.id):
                Found_User_Data_Card = True
                embed = discord.Embed(
                    title = 'View User Data',
                    colour = discord.Colour.gold()
                )
                embed.set_footer(text = '• NKTS Secure Data')
                embed.add_field(name = 'Discord User ID', value = Card['desc'].split('Discord_User_ID:')[1].split('\n')[0], inline = False)
                embed.add_field(name = 'Roblox Username', value = Card['desc'].split('Roblox_Username:')[1].split('\n')[0], inline = False)
                embed.add_field(name = 'Email Address', value = Card['desc'].split('Email_Address:')[1].split('\n')[0], inline = False)
                await DM_Channel.send(embed = embed)
        if Found_User_Data_Card == False:
            embed = discord.Embed(
                title = 'You blew up the internet.',
                description = "We couldn't find a data card for you! Try running `!Link Roblox` in <#865637391808724992>",
                colour = discord.Colour.gold()
            )
            embed.set_footer(text = '• NKTS')
            await DM_Channel.send(embed = embed)