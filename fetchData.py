#Imports
import urllib.request
import json
import time
import csv


myKey = "4fc4d9c8-66cf-471b-9051-a0d8c2f6b3c9"

# entity super class
class ENTITY:
    # initial variables
    name = ""
    url = ""
    tuples = list()
    tupleSize = 0
    numTuples = 0

    # methods
    def __init__(self, inName):
        self.name = inName
        self.url = ""
        self.tuples = list()
        tupleSize = 0
        numTuples = 0

    def numTuples(self):
        return self.numTuples

    def tupleSize(self):
        return self.tupleSize

    def addTuple(self, inData = []):
        self.tuples.append(inData)
        self.numTuples += 1

    def collectData(self):
        raise NotImplementedError("collectData() not yet implemented")

    def writeTuples(self):
        filePath = "C:/Python33/Doc/Databases/%s.csv" % self.name

        with open(filePath, 'w', newline = '') as outFile:
            writer = csv.writer(outFile, delimiter = ',')

            for i in self.tuples:
                writer.writerow(i)

        outFile.close
        
        
    def printTuples(self):
        for list in self.tuples:
            print(list)
        print("\n")

class ITEMS(ENTITY):
    def collectData(self):

        self.url = ("https://na.api.pvp.net/api/lol/static-data/na/v1.2/" +
                    "item?itemListData=consumed,depth,gold,groups&" +
                    "api_key=4fc4d9c8-66cf-471b-9051-a0d8c2f6b3c9")
        self.tupleSize = 5

        try:
            response = urllib.request.urlopen(self.url)
            webContent = response.read()
            data = json.loads(webContent.decode('utf8'))
        except:
            time.sleep(1)
            self.collectData()


        for key in data["data"]:
            thisTuple = list()
            thisTuple.append(str(key))
            item = data["data"][key]

            if data["data"] not in self.tuples:
                thisTuple.append("\"%s\"" %item["name"])
                thisTuple.append(item["gold"]["total"])
                if 'depth' in item.keys():
                    thisTuple.append(item["depth"])
                else:
                    thisTuple.append(1)
                    
                if 'consumed' in item.keys():
                    thisTuple.append(1)
                else:
                    thisTuple.append(0)
                    
                if 'group' in item.keys():
                    thisTuple.append(item["group"])
                else:
                    thisTuple.append("NULL")
                    
                self.tuples.append(thisTuple)
                
    super(ENTITY)


# NEW ATTRIBUTES
# attrange, mplvl, mp, attdmg, hp, hplvl, adlvl,
# arm, mprelvl, hpre, critlvl, spblvl, mpre
# attspdlvl, spd, mvsp, crit,
# hprelvl, armlvl
# Score:
# defense, magic, difficulty, attack
class CHAMPIONS(ENTITY):
    def collectData(self):
        
        self.url = ("https://na.api.pvp.net/api/lol/static-data/na/v1.2/" +
                    "champion?champData=info,stats&" +
                    "api_key=4fc4d9c8-66cf-471b-9051-a0d8c2f6b3c9")
        self.tupleSize = 23

        try:
            response = urllib.request.urlopen(self.url)
            webContent = response.read()
            data = json.loads(webContent.decode('utf8'))
        except:
            time.sleep(1)
            self.collectData()

        for key in data["data"]:
            thisTuple = list()
            champion = data["data"][key]

            # NAME
            thisTuple.append("\"%s\"" %key)

            #STATS
            thisTuple.append(champion["stats"]["attackrange"])
            thisTuple.append(champion["stats"]["mpperlevel"])
            thisTuple.append(champion["stats"]["mp"])
            thisTuple.append(champion["stats"]["attackdamage"])
            thisTuple.append(champion["stats"]["hp"])
            thisTuple.append(champion["stats"]["hpperlevel"])
            thisTuple.append(champion["stats"]["attackdamageperlevel"])
            thisTuple.append(champion["stats"]["armor"])
            thisTuple.append(champion["stats"]["mpregenperlevel"])
            thisTuple.append(champion["stats"]["hpregen"])
            thisTuple.append(champion["stats"]["critperlevel"])
            thisTuple.append(champion["stats"]["spellblockperlevel"])
            thisTuple.append(champion["stats"]["mpregen"])
            thisTuple.append(champion["stats"]["attackspeedperlevel"])
            thisTuple.append(champion["stats"]["spellblock"])
            thisTuple.append(champion["stats"]["movespeed"])
            thisTuple.append(champion["stats"]["crit"])
            thisTuple.append(champion["stats"]["hpregenperlevel"])
            thisTuple.append(champion["stats"]["armorperlevel"])

            # INFO
            thisTuple.append(champion["info"]["defense"])
            thisTuple.append(champion["info"]["magic"])
            thisTuple.append(champion["info"]["difficulty"])
            thisTuple.append(champion["info"]["attack"])
                     
            self.tuples.append(thisTuple)
    super(ENTITY)

# MID, time, teamWon
# CANT DO WINNER
class MATCHES(ENTITY):
    def collectData(self):
        numGames = 0
        gameLimit = 10
        
        # GET PLAYERS FROM CHALLENGER LEAGUE
        challengerUrl = ("https://na.api.pvp.net/api/lol/na/v2.5/" +
                         "league/challenger?type=RANKED_SOLO_5x5" +
                         "&api_key=4fc4d9c8-66cf-471b-9051-a0d8c2f6b3c9")

        try:
            response = urllib.request.urlopen(challengerUrl)
            webContent = response.read()
            topPlayerData = json.loads(webContent.decode('utf8'))
        except:
            time.sleep(10)
            self.collectData()

        playerIDs = list()
        
        for key in topPlayerData["entries"]:
            playerIDs.append(key["playerOrTeamId"])


        # GET FULL MATCH IDs FROM THOSE PLAYERS
        urlHead = ("https://na.api.pvp.net/api/lol/na/v2.2/matchhistory/")
        urlTail = ("?rankedQueues=RANKED_SOLO_5x5" +
                   "&api_key=4fc4d9c8-66cf-471b-9051-a0d8c2f6b3c9")

        playerMatches = list()

        for pID in playerIDs:
            fullUrl = (urlHead + pID + urlTail)

            flag = 0
            while flag == 0:
                try:
                    response = urllib.request.urlopen(fullUrl)
                    webContent = response.read()
                    pHistoryData = json.loads(webContent.decode('utf8'))
                    flag = 1
                except Exception as ex:
                    time.sleep(1)
                    continue

            for key in pHistoryData["matches"]:
                if key not in playerMatches:
                    playerMatches.append(key["matchId"])
                    numGames += 1
                    
            if numGames == gameLimit:
                break
            
        # GET MATCH INFO
        urlHead = ("https://na.api.pvp.net/api/lol/na/v2.2/match/")
        urlTail = ("?api_key=4fc4d9c8-66cf-471b-9051-a0d8c2f6b3c9")

        for mID in playerMatches:
            thisTuple = list()
            fullUrl = (urlHead + str(mID) + urlTail)

            flag = 0
            while flag == 0:
                try:
                    response = urllib.request.urlopen(fullUrl)
                    webContent = response.read()
                    matchData = json.loads(webContent.decode('utf8'))
                    flag = 1
                except Exception as ex:
                    print(ex)
                    time.sleep(1)
                    continue

            #MID
            thisTuple.append(matchData["matchId"])
            #time
            thisTuple.append(matchData["matchDuration"])

            self._tuples.append(thisTuple)

        filePath = "C:/Python33/Doc/Databases/%s.csv" % self.name

        with open(filePath, 'w', newline = '') as outFile:
            writer = csv.writer(outFile, delimiter = ',')

            for i in self._tuples:
                writer.writerow(i)

        outFile.close
        
    super(ENTITY)

items = ITEMS("Items")
items.collectData()
items.printTuples()
items.writeTuples()


championBase = CHAMPIONS("ChampionBaseStats")
championBase.collectData()
championBase.printTuples()
championBase.writeTuples()

#matches = MATCHES("matches")
#matches.collectData()
#matches.printTuples()
#matches.writeTuples()

# CNAME, MID, kills, dths, asst, crp, goldE, pD, mD, tD, dmgT, lCrit, team
#WHAT ARE THESE: bsrp, trDmg, tKills
def compileMatchChampsTuples():
    return 0

# CNAME, MID, type, freq
def compileMatchChampStreaksTuples():
    return 0

# CNAME, MID, ItemName, quant
def compileMatchChampItemsTuples():
    return 0
    
# CNAME, MID
def compileBannedData():
    return 0




