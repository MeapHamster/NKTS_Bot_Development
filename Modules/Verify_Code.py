import requests
import json
import discord
import datetime as DT

async def Error(Channel, Error_Message):
    embed = discord.Embed(
        title = 'Whoops!',
        description = Error_Message,
        colour = discord.Colour.gold()
    )
    await Channel.send(embed = embed)

async def cmd_Verify_Code_Invoked(Variables):
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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Verify Code') == True:
        if message_txt.lower().startswith(MAIN_VARIABLES['PREFIX'] + 'verify code '):
            if message_txt.lower().split(MAIN_VARIABLES['PREFIX'] + 'verify code ')[1] != '':
                Code = message_txt.lower().split(MAIN_VARIABLES['PREFIX'] + 'verify code ')[1]
                User_Data_Cards = Get_User_Data_Cards(Trello_Data)
                Channel = await message.author.create_dm()

                Card_ID = False
                Card_Desc = False

                for Card in User_Data_Cards:
                    if Card['desc'].split('Discord_User_ID:')[1].split('\n')[0] == str(message.author.id):
                        Card_ID = Card['id']
                        Card_Desc = Card['desc']

                if Card_ID != False and Card_Desc != False:
                    Get_Verification_Code_Cards = json.loads(
                        requests.request(
                            'GET',
                            Trello_Data['Verification_Code_Cards']['GET']['URL'],
                            params = {
                                'key': Trello_Data['TRELLO_KEY'],
                                'token': Trello_Data['TRELLO_TOKEN']
                            }
                        ).text
                    )
                    for Verifiction_Card in Get_Verification_Code_Cards:
                        if Verifiction_Card['desc'].split('Creation_Date:')[1].split('\n')[0] == str(DT.date.today()):
                            if Verifiction_Card['desc'].split('Verification_Code:')[1] == Code:
                                Update_User_Data_Card = requests.request(
                                    'PUT',
                                    'https://api.trello.com/1/cards/' + Card_ID,
                                    headers = Trello_Data['Verification_Code_Cards']['GET']['HEADERS'],
                                    params = {
                                        'key': Trello_Data['TRELLO_KEY'],
                                        'token': Trello_Data['TRELLO_TOKEN'],
                                        'desc': Card_Desc.split('Email_Address')[0] + 'Email_Address:' + Verifiction_Card['desc'].split('Email_Address:')[1].split('\n')[0] + Card_Desc.split('Email_Address:')[1]
                                    }
                                )
                                Delete_Card = requests.request(
                                    'DELETE',
                                    'https://api.trello.com/1/cards/' + Verifiction_Card['id'],
                                    params = {
                                        'key': Trello_Data['TRELLO_KEY'],
                                        'token': Trello_Data['TRELLO_TOKEN']
                                    }
                                )
                                embed = discord.Embed(
                                    title = "Successfully linked your email!",
                                    description = "You will receive weekly reports of your logged hours!",
                                    colour = discord.Colour.gold()
                                )
                                embed.set_footer(text = '• NKTS')
                                await Channel.send(embed = embed)
                        else:
                            # await Error(Channel, 'That verification code is either invalid, or expired!')
                            Delete_Card = requests.request(
                                'DELETE',
                                'https://api.trello.com/1/cards/' + Verifiction_Card['id'],
                                params = {
                                    'key': Trello_Data['TRELLO_KEY'],
                                    'token': Trello_Data['TRELLO_TOKEN']
                                }
                            )