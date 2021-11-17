import requests
import json
import discord
import datetime as DT
import random
import smtplib, ssl

port = 465
context = ssl.create_default_context() # Creates a secure SSL context
email = 'newkemptontaxiservice@gmail.com'
password = 'nkts$2005'

async def Error(Channel, Error_Message):
    embed = discord.Embed(
        title = 'Whoops!',
        description = Error_Message,
        colour = discord.Colour.gold()
    )
    await Channel.send(embed = embed)

async def cmd_Email_Invoked(Variables):
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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Email') == True:
        if message_txt.lower().startswith(MAIN_VARIABLES['PREFIX'] + 'email '):
            if message_txt.lower().split(MAIN_VARIABLES['PREFIX'] + 'email ')[1] != '':
                User_Data_Cards = Get_User_Data_Cards(Trello_Data)
                Channel = await message.author.create_dm()
                Username = ''
                User_Data_Card = ''
                Found_Card = False
                for Card in User_Data_Cards:
                    if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == str(message.author.id):
                        Username = Card['desc'].split('Roblox_Username:')[1].split('\n')[0]
                        User_Data_Card = Card
                        Found_Card = True
                if Found_Card == True:
                    if User_Data_Card['desc'].split('Email_Address:')[1].split('\n')[0] == '':
                        Email_Address = message_txt.lower().split(MAIN_VARIABLES['PREFIX'] + 'email ')[1]

                        Random_Verification_Code = str(random.randint(1111111111, 9999999999))

                        Create_Verification_Code_Card = requests.request(
                            'POST',
                            Trello_Data['Verification_Code_Cards']['POST']['URL'],
                            params = {
                                'key': Trello_Data['TRELLO_KEY'],
                                'token': Trello_Data['TRELLO_TOKEN'],
                                'idList': Trello_Data['Verification_Code_Cards']['POST']['IDLIST'],
                                'name': Username,
                                'desc': 'Discord_User_ID:' + str(message.author.id) + '\nCreation_Date:' + str(DT.date.today()) + '\nEmail_Address:' + Email_Address + '\nVerification_Code:' + Random_Verification_Code
                            }
                        ).text

                        if Create_Verification_Code_Card != '200':
                            with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
                                server.login(email, password)
                                Email = server.sendmail(email, Email_Address, 'Use the code below to verify that the email address you provided is yours!\n\n' + Random_Verification_Code)
                                if len(Email) == 0:
                                    embed = discord.Embed(
                                        title = 'Verification email sent!',
                                        description = 'Retrieve the code from the inbox of ' + Email_Address + '\n\nUse the command `!Verify Code [Code]` in my DMs to complete the process.',
                                        colour = discord.Colour.gold()
                                    )
                                    embed.set_footer(text = '• NKTS')
                                    await Channel.send(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        title = 'Hmm... something doesn\'t look right',
                                        description = 'The address you provided isn\'t working! Try another email address or contact support.',
                                        colour = discord.Colour.gold()
                                    )
                                    await Channel.send(embed = embed)

                        else:
                            embed = discord.Embed(
                                title = 'Oops!',
                                description = 'You blew up the internet.\n\nSomething didn\'t process correctly. Try again.',
                                colour = discord.Colour.gold()
                            )
                            await Channel.send(embed = embed)
                    else:
                        embed = discord.Embed(
                            title = 'Oh no! An error message!',
                            description = 'You already have an email address linked! Contact an administrator for helP!',
                            colour = discord.Colour.gold()
                        )
                        embed.set_footer(text = '• NKTS')
                        await DM_Channel.send(embed = embed)
                else:
                    embed = discord.Embed(
                        title = 'Whoops!',
                        description = 'You must verify your Roblox account before adding an email address. Use the command `!Link Roblox` in <#865637391808724992>.',
                        colour = discord.Colour.gold()
                    )
                    embed.set_footer(text = '• NKTS')
                    await DM_Channel.send(embed = embed)