import discord
import requests
import json

async def cmd_Driving_Test_Invoked(Variables):
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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Driving Test') == True:
        UserDataCards = Get_User_Data_Cards(Trello_Data)
        User_ID = message_txt.split('<@!')[1].split('>')[0]
        Found_Data_Card = False
        Username = ''
        for Card in UserDataCards:
            if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == User_ID:
                Username = Card['name']
                Found_Data_Card = True
        if Found_Data_Card == True:
            User_Driving_Tests = ''

            embed = discord.Embed(
                title = 'This could take some time',
                description = 'Please wait as I search for this user\'s certificate(s).',
                colour = discord.Colour.gold()
            )
            embed.set_footer(text = '• NKTS Employee Tracker')
            await Channel.send(embed = embed)

            Driving_Tests = json.loads(
                requests.request(
                    'GET',
                    Trello_Data['Employee_Tracker_Driving_Certificates']['GET']['URL'],
                    headers = Trello_Data['Employee_Tracker_Driving_Certificates']['GET']['HEADERS']
                ).text
            )
            for Card in Driving_Tests:
                response = json.loads(
                    requests.request(
                        "GET",
                        f"https://api.trello.com/1/cards/{Card['id']}/customFieldItems",
                        headers={
                            "Accept": "application/json"
                        }
                    ).text
                )

                if len(response) > 0:
                    if response[0]['value']['text'] == Username:
                        User_Driving_Tests = (f"{User_Driving_Tests}[{Card['name']}]({Card['shortUrl']})\n")
            
            if User_Driving_Tests != '':
                embed = discord.Embed(
                    title = 'Here\'s what I found',
                    description = User_Driving_Tests,
                    colour = discord.Colour.gold()
                )
                embed.set_footer(text = '• NKTS Employee Tracker')
                await Channel.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = 'I couldn\'t find a certificate for that user',
                    colour = discord.Colour.gold()
                )
                embed.set_footer(text = '• NKTS Employee Tracker')
                await Channel.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'NKTS Employee Tracker',
                description = 'This user has not verified their Roblox account!\nTry running `!Link Roblox` in <#865637391808724992>',
                colour = discord.Colour.red()
            )
            embed.set_footer(text = '• NKTS Employee Tracker')
            await Channel.send(embed = embed)