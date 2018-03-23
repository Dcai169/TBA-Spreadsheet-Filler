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
estimatedPerformance=40
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

#gets team numbers and nicknames from TBAreader  
def TBAeventParticipantsReader(event):
  eventTeams=TBAreader("event/"+str(event)+"/teams/keys")
  participants={}
  for i in range(0,len(eventTeams)):
    participants[str(eventTeams[i][3:])]=(TBAreader("team/"+eventTeams[i]))['nickname']
  return participants
#writes data to spreadsheet
def sheetDataWriter(event):
  participantNumbers=list(TBAeventParticipantsReader(event).keys())
  participantNames=list(TBAeventParticipantsReader(event).values())
  print('writing')
  for j in range(0, len(participantNumbers)):
    sh.update_cell(j+2, 1, participantNumbers[j])
    sh.update_cell(j+2, 2, participantNames[j])
  return True
#uses the keenan advancement prediction algorithm
def advancementPredictor(team, district, estimation):
  rankings=TBAreader("district/"+district+"/rankings")
  for k in range(0,len(rankings)):
    passingTeams={}
    if rankings[k]['team_key']==team:
      print("baseline team found")
      focusTeamRank=rankings[k]['rank']
      focusTeamRP=rankings[k]['point_total']
      passingThreshold=k+estimation
      #print(k, focusTeamRank, estimation, passingThreshold)
      for l in range(k, passingThreshold):
        if focusTeamRP>rankings[l]['point_total']:
          passingTeams[rankings[l]['team_key']]=(rankings[l]['point_total'])
      return(len(passingTeams)+focusTeamRank+1)
      
sheetDataWriter("2018marea")
print(advancementPredictor(focusTeam, focusDistrict, estimatedPerformance))
