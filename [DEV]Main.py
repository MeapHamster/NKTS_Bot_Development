#  Main Variables
MAIN_VARIABLES = {
    'PREFIX' : '%',
    'MINIMUM_HOURS' : 1
}

import discord

#  Data Storage
from Data_Storage.Command_Channel_Whitelist import Command_Channel_Whitelists
from Data_Storage.Command_Whitelists import Command_Whitelists
from Data_Storage.Trello_Data import Trello_Data

#  Functions
from Functions.Check_Command import Check_Command
from Functions.GetUserDataCards import Get_User_Data_Cards
from Functions.Online_Status_Changed import Online_Status_Changed

#  Modules
from Modules.Inactivity_Notice import cmd_Inactivity_Notice_Invoked
from Modules.Hour_Reduction import cmd_Hour_Reduction_Invoked
from Modules.Hours_All import cmd_Hours_All_Invoked
from Modules.Hours_Clear import cmd_Hours_Clear_Invoked
from Modules.Hours_Me import cmd_Hours_Me_Invoked
from Modules.Hours_User import cmd_Hours_User_Invoked
from Modules.Link import cmd_Link_Invoked
from Modules.Link_Roblox import cmd_Link_Roblox_Invoked
from Modules.Link_Email import cmd_Link_Email_Invoked
from Modules.Email import cmd_Email_Invoked
from Modules.Verify_Code import cmd_Verify_Code_Invoked

intents = discord.Intents.default()
intents.members = True

#  Client Connect
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    Variables = {
        'client': client,
        'message': message,
        'MAIN_VARIABLES': MAIN_VARIABLES,
        'Channel_Whitelist': Command_Channel_Whitelists,
        'Command_Whitelists': Command_Whitelists,
        'Check_Command': Check_Command,
        'Get_User_Data_Cards': Get_User_Data_Cards,
        'Trello_Data': Trello_Data
    }
    await cmd_Inactivity_Notice_Invoked(Variables)
    await cmd_Hour_Reduction_Invoked(Variables )
    await cmd_Hours_All_Invoked(Variables)
    await cmd_Hours_Clear_Invoked(Variables)
    await cmd_Hours_Me_Invoked(Variables)
    await cmd_Link_Invoked(Variables)
    await cmd_Link_Roblox_Invoked(Variables)
    await cmd_Link_Email_Invoked(Variables)
    await cmd_Email_Invoked(Variables)
    await cmd_Verify_Code_Invoked(Variables)
    await cmd_Hours_User_Invoked(Variables)

client.run('ODI5NDc5MTI3MTg1NzUyMDk0.YG4uog.Uwl00sM0g1mKYVbT-iMVN1inaL0')