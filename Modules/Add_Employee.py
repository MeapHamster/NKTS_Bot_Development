import discord
import requests
import json

async def cmd_Add_Employee_Invoked(Variables):
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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Add Employee') == True:
        UserDataCards = Get_User_Data_Cards(Trello_Data)
        User_ID = message_txt.split('<@!')[1].split('>')[0]
        User = None
        for Member in message.guild.members:
            if str(Member.id) == User_ID:
                User = Member
        if User != None:
            Found_Data_Card = False
            Already_Employee = False
            Username = ''
            for Card in UserDataCards:
                if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == User_ID:
                    Username = Card['name']
                    Found_Data_Card = True
            print(Username)
            if Found_Data_Card == True:
                Employee_Cards = json.loads(
                    requests.request(
                        'GET',
                        Trello_Data['Employee_Tracker_Employees']['GET']['URL'],
                        headers = Trello_Data['Employee_Tracker_Employees']['GET']['HEADERS']
                    ).text
                )
                Management_Cards = json.loads(
                    requests.request(
                        'GET',
                        Trello_Data['Employee_Tracker_Management']['GET']['URL'],
                        headers = Trello_Data['Employee_Tracker_Management']['GET']['HEADERS']
                    ).text
                )
                Training_Cards = json.loads(
                    requests.request(
                        'GET',
                        Trello_Data['Employee_Tracker_Training']['GET']['URL'],
                        headers = Trello_Data['Employee_Tracker_Training']['GET']['HEADERS']
                    ).text
                )
                for Card in Employee_Cards:
                    if Card['name'] == Username:
                        Already_Employee = True
                for Card in Management_Cards:
                    if Card['name'] == Username:
                        Already_Employee = True
                for Card in Training_Cards:
                    if Card['name'] == Username:
                        Already_Employee = True
                if Already_Employee == False:
                    Create_Training_Card = requests.request(
                        'POST',
                        Trello_Data['Employee_Tracker_Training']['POST']['URL'],
                        params = {
                            'key': Trello_Data['TRELLO_KEY'],
                            'token': Trello_Data['TRELLO_TOKEN'],
                            'idList': Trello_Data['Employee_Tracker_Training']['POST']['IDLIST'],
                            'name': Username,
                            'idLabels': '605e95d37d3ebf2f40c50142,6028841286c6bc9cc51892a6',
                            'desc': 'Driving Test\n---'
                        }
                    ).text
                    JsonDecoded = json.loads(Create_Training_Card)
                    embed = discord.Embed(
                        title = 'NKTS Employee Tracker',
                        description = '**Employee Added:**\n<@!' + str(User_ID) + '>\n' + JsonDecoded['url'],
                        colour = discord.Colour.gold()
                    )
                    embed.set_footer(text = '• NKTS Employee Tracker')
                    await Channel.send(embed = embed)
                    Roles = [
                        discord.utils.get(message.guild.roles, name = '[T] Taxi Driver'),
                        discord.utils.get(message.guild.roles, name = 'Employee in Training'),
                        discord.utils.get(message.guild.roles, name = 'Classroom Needed'),
                        discord.utils.get(message.guild.roles, name = 'Uncertified Driver')
                    ]
                    await message.author.add_roles(*Roles)
                else:
                    embed = discord.Embed(
                        title = 'NKTS Employee Tracker',
                        description = 'Looks like this user already has an employee card!',
                        colour = discord.Colour.red()
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
        else:
            embed = discord.Embed(
                title = 'NKTS Employee Tracker',
                description = 'Doesn\'t look like this user is a member of this server!',
                colour = discord.Colour.red()
            )
            embed.set_footer(text = '• NKTS Employee Tracker')
            await Channel.send(embed = embed)