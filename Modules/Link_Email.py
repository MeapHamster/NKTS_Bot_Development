import requests
import json
import discord

async def cmd_Link_Email_Invoked(Variables):
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
    message_txt = message.content
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Link Email') == True:
        Channel = await message.author.create_dm()
        User_Data_Cards = Get_User_Data_Cards(Trello_Data)
        Username = ''
        Found_Card = False
        for Card in User_Data_Cards:
            if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == str(message.author.id):
                Username = Card['desc'].split('Account_Username:')[1].split('\n')[0]
                Found_Card = True
        if Found_Card == True:
            embed = discord.Embed(
                title = "Email Linking Process",
                description = "• Use the command `!email [your email address]` in my DMs.\n• Check your inbox and retrieve the verification code.\n • Use the command `!Verify Code [Code]` in my DMs to complete the process.",
                colour = discord.Colour.gold()
            )
            embed.set_footer(text = 'Attention:\nVerification codes expire daily.\n\n• NKTS')
            await Channel.send(embed = embed)
        else:
            embed = discord.Embed(
                title = "Whoops!",
                description = "You must verify your Account account before adding an email address. Use the command `!Link Account` in <#865637391808724992>.",
                colour = discord.Colour.gold()
            )
            embed.set_footer(text = '• NKTS')
            await DM_Channel.send(embed = embed)