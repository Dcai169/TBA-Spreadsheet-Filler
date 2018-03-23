print("program start")
#program init
import requests
import gspread
import json
import pprint
from oauth2client.service_account import ServiceAccountCredentials
#variable declaration
TBA='https://www.thebluealliance.com/api/v3/'
focusTeam='frc5735'
focusDistrict='2018ne'
eventKey='2018marea'
TBAauthKey="uSAyrK7Xsxf7mSCSY6ivVy4KHM8CpyVISV9EM96d8ZS9ZLCY4oFsyAWPcSaByD2U"
pp=pprint.PrettyPrinter()
#google autherization
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(credentials)
sh=gc.open('Reading Scouting Data Test').get_worksheet(1)
headers={'X-TBA-Auth-Key' : TBAauthKey}
print("init complete")

#program logic starts here

#Reads from data from TBA API
def TBAreader(path):
  output=json.loads(requests.get(TBA+path, params=headers).text)
  return output
"""
#gets team numbers and nicknames from TBAreader  
def TBAeventParticipantsReader(event):
  eventTeams=TBAreader("event/"+str(event)+"/teams/keys")
  participants={}
  for i in range(0,len(eventTeams)):
    participants[str(eventTeams[i][3:])]=(TBAreader("team/"+eventTeams[i]))['nickname']
  return participants

participantNumbers=list(TBAeventParticipantsReader(eventKey).keys())
participantNames=list(TBAeventParticipantsReader(eventKey).values())
print('writing')
for j in range(0, len(participantNumbers)):
  sh.update_cell(j+2, 1, participantNumbers[j])
  sh.update_cell(j+2, 2, participantNames[j])
"""
rankings=TBAreader("district/"+focusDistrict+"/rankings")

pp.pprint(rankings[20]['team_key'])

#for k in range(0,len(rankings):
#  if rankings[i][