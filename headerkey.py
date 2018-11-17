import requests
import json


class HeaderKey:
    def __init__(self, url, key_name, key):
        self.data = []
        self.url = url
        self.headers = {key_name: key}
        self.timeout = 1

        # Reads from data from TBA API
    def reader(self, path):
        output = json.loads(requests.get(self.url + path, params=self.headers).text)
        return output

    # gets team numbers and nicknames from TBAreader
    def get_event_participants(self, event):
        event_teams = self.reader("event/"+str(event)+"/teams/keys")
        participants = {}
        for i in range(0, len(event_teams)):
            participants[str(event_teams[i][3:])] = self.reader("team/"+event_teams[i])['nickname']
        return participants
