Channels = {
    'General' : 714674118984990834,
    'Bot Commands' : 865637391808724992,
    'Inactivity Notices Channel' : 770844332055330907
}

Command_Channel_Whitelists = {
    'Inactivity Notice' : {
        'SERVER_CHANNEL': True, # If False, it is assumed that it is a DM command
        'CHANNELS': [
            Channels['Inactivity Notices Channel']
        ]
    },
    'Hour Reduction' : {
        'SERVER_CHANNEL': True,
        'CHANNELS': [
            Channels['Inactivity Notices Channel']
        ]
    },
    'Add Employee' : {
        'SERVER_CHANNEL': True,
        'CHANNELS': [
            Channels['General']
        ]
    },
    'Fire Employee' : {
        'SERVER_CHANNEL': True,
        'CHANNELS': [
            Channels['General']
        ]
    },
    'Employees' : {
        'SERVER_CHANNEL': True,
        'CHANNELS': [
            Channels['General']
        ]
    },
    'Driving Test' : {
        'SERVER_CHANNEL': True,
        'CHANNELS': [
            Channels['General']
        ]
    },
    'User Info' : {
        'SERVER_CHANNEL': True,
        'CHANNELS': [
            Channels['General']
        ]
    },
    'Hours All' : {
        'SERVER_CHANNEL': True,
        'CHANNELS': [
            Channels['General']
        ]
    },
    'Hours Clear' : {
        'SERVER_CHANNEL': True,
        'CHANNELS': [
            Channels['General']
        ]
    },
    'Hours Me' : {
        'SERVER_CHANNEL': True,
        'CHANNELS': [
            Channels['Bot Commands']
        ]
    },
    'Hours <@!' : {
        'SERVER_CHANNEL': True,
        'CHANNELS': [
            Channels['Bot Commands']
        ]
    },
    'Link' : {
        'SERVER_CHANNEL': True,
        'CHANNELS': [
            Channels['Bot Commands']
        ]
    },
    'Link Roblox' : {
        'SERVER_CHANNEL': True,
        'CHANNELS': [
            Channels['Bot Commands']
        ]
    },
    'Link Email' : {
        'SERVER_CHANNEL': False,
        'CHANNELS': [
            
        ]
    },
    'Email' : {
        'SERVER_CHANNEL': False,
        'CHANNELS': [
            
        ]
    },
    'Verify Code' : {
        'SERVER_CHANNEL': False,
        'CHANNELS': [
            
        ]
    },
    'View Data' : {
        'SERVER_CHANNEL': False,
        'CHANNELS': [
            
        ]
    },
    'Erase Data' : {
        'SERVER_CHANNEL': False,
        'CHANNELS': [
            
        ]
    },
}