import requests
import json
import discord

async def cmd_Link_Invoked(Variables):
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
    if Check_Command(message, MAIN_VARIABLES['PREFIX'], Channel_Whitelist, Command_Whitelists, 'Link') == True:
        DM_Channel = await message.author.create_dm()
        DM_Alert_Message = discord.Embed(
            title = "Message sent to DMs!",
            description = "",
            colour = discord.Colour.gold()
        )
        await Channel.send(embed = DM_Alert_Message)
        embed = discord.Embed(
            title = "Link to Discord Account",
            description = "",
            colour = discord.Colour.gold()
        )
        embed.add_field(name = 'Roblox Username', value = "Use the `!Link Roblox` command in <#865637391808724992> to link your Roblox username to your Discord account", inline=False)
        embed.add_field(name = 'Email Address', value = "Use the command `!Link Email` in my DMs to link your email address to your account", inline=False)
        embed.set_footer(text = 'Viewing Data:\nTo view your data, use the command !View Data in my DMs\nUpdating Data:\nTo update data, contact an administrator\nErasing Data:\nTo erase your data, use the command !Erase Data in my DMs\n\n• NKTS')
        await DM_Channel.send(embed = embed)