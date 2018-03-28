print("program start")
#program init
import requests
import gspread
import json
import pprint
from oauth2client.service_account import ServiceAccountCredentials
#variable declaration
focusTeam='frc5735'
focusDistrict='2018ne'
eventKey='2018marea'
pp=pprint.PrettyPrinter()

#google autherization
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(credentials)
sh=gc.open('Scouting Data Test Sheet').get_worksheet(1)

print("init complete")

#program logic starts here
class TBA:
  def __init__(self):
    self.data = []
    self.TBAurl='https://www.thebluealliance.com/api/v3/'
    self.headers={'X-TBA-Auth-Key' : "uSAyrK7Xsxf7mSCSY6ivVy4KHM8CpyVISV9EM96d8ZS9ZLCY4oFsyAWPcSaByD2U"}
    self.timeout=1
    #Reads from data from TBA API
  def reader(self, path):
    output=json.loads(requests.get(self.TBAurl+path, params=self.headers).text)
    return output
  #gets team numbers and nicknames from TBAreader  
  def getEventParticipants(self, event):
    eventTeams=self.reader("event/"+str(event)+"/teams/keys")
    participants={}
    for i in range(0,len(eventTeams)):
      participants[str(eventTeams[i][3:])]=(self.reader("team/"+eventTeams[i]))['nickname']
    return participants
tba=TBA()
  
#searches a dictionary for a key Or Value; returns the index
#fix this its broken
class searchDistrictRankings:
  def __init__(self, district):
    self.data = []
    self.rankings=tba.reader("district/"+district+"/rankings")
    
  def rankingsKeys(self, query):
    for i in range(0,len(self.rankings)):
      if self.rankings[i]==query:
        return i
        
  def indexByKey(self, query, key):
    for i in range(0,len(self.rankings)):
      if self.rankings[i]==key:
        for j in range(0,len(self.rankings[i])):
          if self.rankings[i][j]==query:
            return i
s=searchDistrictRankings("2018ne")

class advancementPrediction:
  def __init__(self):
    self.data = []
  #uses the keenan advancement prediction algorithm
  def advancementPredictor(self, estimation, district, team):
    rankings=tba.reader("district/"+district+"/rankings")
    for k in range(0,len(rankings)):
      passingTeams={}
      if rankings[k]['team_key']==team:
        print("baseline team found")
        focusTeamRank=rankings[k]['rank']
        focusTeamRP=rankings[k]['point_total']
        passingThreshold=k+estimation
        for l in range(k, passingThreshold):
          if focusTeamRP>rankings[l]['point_total']:
            passingTeams[rankings[l]['team_key']]=(rankings[l]['point_total'])
            return(len(passingTeams)+focusTeamRank+1)
          
  def keenanFunction(self, futile):
    futile=False
    return futile
a=advancementPrediction()

#writes data to spreadsheet
def sheetDataWriter(event):
  participantNumbers=list(tba.getEventParticipants(event).keys())
  participantNames=list(tba.getEventParticipants(event).values())
  print('writing')
  for j in range(0, len(participantNumbers)):
    sh.update_cell(j+2, 1, participantNumbers[j])
    sh.update_cell(j+2, 2, participantNames[j])
  return True
