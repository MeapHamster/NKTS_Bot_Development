import discord

def Check_Command(message, prefix, Channel_Whitelist, Command_Whitelists, command):
    message_txt = message.content.lower()
    command_txt = command.lower()

    if not message_txt:
        return False

    if message.author.bot:
        print('Bot sent message')
        return False

    Correct_Command = False

    if Command_Whitelists[command]['Exact Command'] == True:
        if message_txt == (prefix + command_txt):
            Correct_Command = True
    elif Command_Whitelists[command]['Exact Command'] == False:
        if message_txt.startswith(prefix + command_txt):
            Correct_Command = True
    
    if Correct_Command == True:

        Sent_In_Whitelisted_Channel = False
        Sent_By_Whitelisted_User    = False

        if Channel_Whitelist[command]['SERVER_CHANNEL'] == True:
            for channel_id in Channel_Whitelist[command]['CHANNELS']:
                if message.channel.id == channel_id:
                    Sent_In_Whitelisted_Channel = True
        else:
            if message.channel.type == discord.ChannelType.private:
                Sent_In_Whitelisted_Channel = True

        Role_Whitelist = Command_Whitelists[command]['Roles']
        User_Whitelist = Command_Whitelists[command]['Users']

        for Whitelisted_Role in Role_Whitelist:
            for Role in message.author.roles:
                if Role.id == Whitelisted_Role:
                    Sent_By_Whitelisted_User = True

        for Whitelisted_User in User_Whitelist:
            if message.author.id == Whitelisted_User:
                Sent_By_Whitelisted_User = True

        if Command_Whitelists[command]['All Users'] == True:
                Sent_By_Whitelisted_User = True
        
        if Sent_In_Whitelisted_Channel == False:
            print('Command invoked in unwhitelisted Channel')
            return False

        if Sent_By_Whitelisted_User == False:
            print('Command invoked by unwhitelisted user')
            return False

        if Sent_By_Whitelisted_User == True and Sent_In_Whitelisted_Channel == True:
            print('Command Invoked: ' + command)
            return True
    else:
        return False