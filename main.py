print("program start")
# program init
import requests
import gspread
import json
import pprint
from oauth2client.service_account import ServiceAccountCredentials
# variable declaration
focusTeam = 'frc5735'
focusDistrict = '2018ne'
eventKey = '2018marea'
pp = pprint.PrettyPrinter()

# google authorization
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open('Scouting Data Test Sheet').get_worksheet(1)

print("init complete")

# program logic starts here


class X_Header:
    def __init__(self):
        self.data = []
        self.TBAurl = 'https://www.thebluealliance.com/api/v3/'
        self.headers = {'X-TBA-Auth-Key': "uSAyrK7Xsxf7mSCSY6ivVy4KHM8CpyVISV9EM96d8ZS9ZLCY4oFsyAWPcSaByD2U"}
        self.timeout = 1

        # Reads from data from TBA API
    def reader(self, path):
        output = json.loads(requests.get(self.TBAurl+path, params=self.headers).text)
        return output
    
    # gets team numbers and nicknames from TBAreader
    def get_event_participants(self, event):
        event_teams = self.reader("event/"+str(event)+"/teams/keys")
        participants = {}
        for i in range(0, len(event_teams)):
            participants[str(event_teams[i][3:])] = self.reader("team/"+event_teams[i])['nickname']
        return participants


tba = X_Header()


# writes data to spreadsheet
def sheet_data_writer(event):
    participant_numbers=list(tba.get_event_participants(event).keys())
    participant_names=list(tba.get_event_participants(event).values())
    print('writing')
    for j in range(0, len(participant_numbers)):
        sh.update_cell(j+2, 1, participant_numbers[j])
        sh.update_cell(j+2, 2, participant_names[j])
    return True

