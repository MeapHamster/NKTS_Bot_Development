import requests
import json
import discord

async def Error(Channel, Error_Message):
    embed = discord.Embed(
        title = Error_Message,
        colour = discord.Colour.red()
    )
    await Channel.send(embed = embed)

async def Create_Trello_Card(Channel, Username, Start, End, Reason, Trello_Data):
    Trello_Cards = json.loads(
        requests.request(
            'GET',
            Trello_Data['Inactivity_Notice']['GET']['URL'],
            headers = Trello_Data['Inactivity_Notice']['GET']['HEADERS']
        ).text
    )
    Found_Card = False
    for Card in Trello_Cards:
        if Card['name'] == Username:
            Found_Card = True
            embed = discord.Embed(
                title = 'You already have an active inactivity notice!',
                description = Card['url'],
                colour = discord.Colour.red()
            )
            await Channel.send(embed = embed)
            return False
    if Found_Card == False:
        Create_Card = requests.request(
            'POST',
            Trello_Data['Inactivity_Notice']['POST']['URL'],
            params = {
                'key': Trello_Data['TRELLO_KEY'],
                'token': Trello_Data['TRELLO_TOKEN'],
                'idList': Trello_Data['Inactivity_Notice']['POST']['IDLIST'],
                'name': Username,
                'desc': 'Reason: \n----------------\n' + Reason + '\nStart: \n----------------\n' + Start + '\nEnd: \n----------------\n' + End,
                'due': End + ' 9:00 AM'
            }
        )
    return True

async def Send_Message_Reply(Channel, Username, Start, End, Reason, Avatar_Url, Trello_Data):
    Trello_Cards = json.loads(
        requests.request(
            'GET',
            Trello_Data['Inactivity_Notice']['GET']['URL'],
            headers = Trello_Data['Inactivity_Notice']['GET']['HEADERS']
        ).text
    )
    Trello_Card_URL = 'google.com'
    for Card in Trello_Cards:
        if Card['name'] == Username:
            Trello_Card_URL = Card['url']
    embed = discord.Embed(
        title = Username,
        description = Trello_Card_URL,
        colour = discord.Colour.gold()
    )
    embed.set_footer(text = '• NKTS Inactivity Notice')
    embed.set_thumbnail(url = Avatar_Url)
    embed.add_field(name = 'Reason', value = Reason, inline=False)
    embed.add_field(name = 'Start Date', value = Start, inline=True)
    embed.add_field(name = 'End Date', value = End, inline=True)
    await Channel.send(embed = embed)

async def cmd_Inactivity_Notice_Invoked(Variables):
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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Inactivity Notice') == True:
        User_Data_Cards = Get_User_Data_Cards(Trello_Data)
        if message_txt.find('\nStart:') != -1 and message_txt.find('\nEnd:') != -1 and message_txt.find('\nReason:') != -1:
            if message_txt.split('Reason:')[1]:
                Username = ''
                Data_Card_Found = False
                for Card in User_Data_Cards:
                    if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == str(message.author.id):
                        Data_Card_Found = True
                        Username = Card['desc'].split('Account_Username:')[1].split('\n')[0]
                if Data_Card_Found == True:
                    Start = message_txt.split('\nStart:')[1].split('\nEnd:')[0]
                    End = message_txt.split('\nEnd:')[1].split('\nReason:')[0]
                    Reason = message_txt.split('\nReason:')[1]
                    if Start.find('/') != -1:
                        StartDateArray = Start.split('/')
                        if len(StartDateArray) == 3:
                            if int(StartDateArray[0]) > 12:
                                await Error(Channel, 'Invalid date provided.')
                                return
                            if int(StartDateArray[1]) > 31:
                                await Error(Channel, 'Invalid date provided.')
                                return
                    else:
                        await Error(Channel, 'Invalid date provided.')
                    
                    if End.find('/') != -1:
                        EndDateArray = End.split('/')
                        if len(EndDateArray) == 3:
                            if int(EndDateArray[0]) > 12:
                                await Error(Channel, 'Invalid date provided.')
                                return
                            if int(EndDateArray[1]) > 31:
                                await Error(Channel, 'Invalid date provided.')
                                return

                        Create_Card = await Create_Trello_Card(Channel, Username, Start, End, Reason, Trello_Data)
                        if Create_Card == True:
                            await Send_Message_Reply(Channel, Username, Start, End, Reason, message.author.avatar, Trello_Data)
                            await message.author.add_roles(discord.utils.get(message.guild.roles, name = "LOA"))
                    else:
                        await Error(Channel, 'Invalid date provided.')
                else:
                    await Error(Channel, 'Data Card not found. Please run !Link Account in the bot commands channel.')
            else:
                await Error(Channel, 'Command may be incorrectly formatted.')
        else:
            await Error(Channel, 'Command may be incorrectly formatted.')