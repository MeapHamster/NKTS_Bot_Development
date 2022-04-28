import requests
import json
import discord
import datetime as DT

async def Error(Channel, Error_Message):
    embed = discord.Embed(
        title = Error_Message,
        colour = discord.Colour.red()
    )
    await Channel.send(embed = embed)

async def cmd_Hour_Reduction_Invoked(Variables):
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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Hour Reduction') == True:
        Username = ''
        Data_Card_Found = False
        User_Data_Cards = Get_User_Data_Cards(Trello_Data)
        for Card in User_Data_Cards:
            if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == str(message.author.id):
                Data_Card_Found = True
                Username = Card['desc'].split('Account_Username:')[1].split('\n')[0]
        if Data_Card_Found == True:
            Hour_Reduction_Cards = json.loads(
                requests.request(
                    'GET',
                    Trello_Data['Hour_Reduction']['GET']['URL'],
                    headers = Trello_Data['Hour_Reduction']['GET']['HEADERS']
                ).text
            )
            for Card in Hour_Reduction_Cards:
                if Card['name'] == Username:
                    await Error(Channel, 'You alread have an active hour reduction!')
                    return
            today = str(DT.date.today() + DT.timedelta(days=7))
            new_format = today.split('-')
            Start_Date = str(DT.date.today()).split('-')[1]+'/'+str(DT.date.today()).split('-')[2]+'/'+str(DT.date.today()).split('-')[0]
            End_Date = new_format[1]+'/'+new_format[2]+'/'+new_format[0]
            Create_Card = requests.request(
                'POST',
                Trello_Data['Hour_Reduction']['POST']['URL'],
                params = {
                    'key': Trello_Data['TRELLO_KEY'],
                    'token': Trello_Data['TRELLO_TOKEN'],
                    'idList': Trello_Data['Hour_Reduction']['POST']['IDLIST'],
                    'name': Username,
                    'desc': 'Start: \n----------------\n' + Start_Date + '\nEnd: \n----------------\n' + End_Date,
                    'due': End_Date + ' 9:00 AM'
                }
            )
            embed = discord.Embed(
                title = Username,
                colour = discord.Colour.gold()
            )
            embed.set_footer(text = '• NKTS Hour Reduction')
            embed.set_thumbnail(url = message.author.avatar)
            embed.add_field(name = 'Start Date', value = Start_Date, inline=True)
            embed.add_field(name = 'End Date', value = End_Date, inline=True)
            await message.author.add_roles(discord.utils.get(message.guild.roles, name = "Reduced Hours"))
            await Channel.send(embed = embed)
        else:
            await Error(Channel, 'Data Card not found. Please run !Link Account in the bot commands channel.')