import requests
import json

def Get_User_Data_Cards(Trello_Data):
    Data = json.loads(
        requests.request(
            'GET',
            Trello_Data['User_Data_Cards']['GET']['URL'],
            params = {
                'key': Trello_Data['TRELLO_KEY'],
                'token': Trello_Data['TRELLO_TOKEN']
            },
        ).text
    )
    return Data