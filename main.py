import gspread
import pprint
from oauth2client.service_account import ServiceAccountCredentials
import apiaccessor
import credentials
from time import sleep
from json import loads
# variable declaration
focus_team = 'frc5735'
focus_district = '2019ne'
event_key = '2018marea'
# event_key = '2019mabos'
sheet_name = 'Scouting Data Test Sheet'
delay = 1
pp = pprint.PrettyPrinter()
KEY_NAME = 'X-TBA-Auth-Key'
KEY = credentials.key
URL = 'https://www.thebluealliance.com/api/v3/'

# google authorization
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(credentials)
pws = gc.open(sheet_name).get_worksheet(1)
sws = gc.open(sheet_name).get_worksheet(2)

print("init complete")

# program logic starts here
tba = apiaccessor.XAPIKey(URL, KEY_NAME, KEY)


# gets team numbers and nicknames from TBAreader
def get_event_participants(event):
    event_teams = loads(tba.reader("event/"+str(event)+"/teams/keys", '').text)
    participants = {}
    for i in range(len(event_teams)):
        participants[str(event_teams[i][3:])] = loads(tba.reader("team/"+event_teams[i], '').text)['nickname']
    return participants


# writes data to spreadsheet
def plabel_writer(event):
    participant_numbers = list(get_event_participants(event).keys())
    participant_names = list(get_event_participants(event).values())
    print('writing')
    for j in range(len(participant_numbers)):
        pws.update_cell(j + 3, 1, participant_numbers[j])
        pws.update_cell(j + 3, 2, participant_names[j])
        print(str(round(calc_percent(j, len(participant_numbers))))+'% complete', end='\r')
        sleep(delay)
    print()
    print('done')
    return True


def slabel_writer(event):
    matches = loads(tba.reader('event/'+event+'/matches/simple', '').text)
    all_participants = []
    for i in range(len(matches)):
        allianceb = matches[i]['alliances']['blue']['team_keys']
        alliancer = matches[i]['alliances']['red']['team_keys']
        for team in allianceb:
            all_participants.append(team)
        for team in alliancer:
            all_participants.append(team)
    print('writing')
    for j in range(len(all_participants)):
        sws.update_cell(j + 3, 2, all_participants[j][3:])
        print(str(round(calc_percent(j, len(all_participants))))+'% complete', end='\r')
        sleep(delay)
    print()
    print('done')
    return True


def calc_percent(part, whole):
    return part/whole*100


# plabel_writer(event_key)
# slabel_writer(event_key)
