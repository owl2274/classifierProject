from urllib.request import urlopen
from urllib.parse import urlencode
import json,urllib
import urllib
import requests



#get accountid from name
class LOLApi:
    def __init__(self,key,server="kr",base_url = "https://{}.api.riotgames.com/lol"):
        self.key = key
        self.base_url = base_url.format(server)


    def getSummoner(self,name):
        url = self.base_url + "/summoner/v3/summoners/by-name/" + name + "?api_key=" + self.key

        return requests.get(url).json()





# gets all match ID from summoner ID
    def getMatchIDs(self,summoner_ID):
        url = self.base_url + "/match/v3/matchlists/by-account/" + str(summoner_ID) + "/recent" + "?api_key=" + self.key

        getUrl = requests.get(url)

        page = getUrl.json()


        return page["matches"]

    def getMatchDetail(self,matchId):
        url = self.base_url + "/match/v3/matches/" + str(matchId) + "?api_key=" + self.key
        print(url)
        getUrl = requests.get(url)
        page = getUrl.json()

        return page

    def getChampionId(self):
        url = self.base_url +  "/static-data/v3/champions?locale=en_US&tags=keys&dataById=false&" + "api_key=" + self.key
        page = requests.get(url).json()
        print(page)
        return page["keys"]

    def getSummonerSpell(self):
        url = self.base_url + "/static-data/v3/summoner-spells?locale=en_US&dataById=false&tags=key&" + "api_key=" + self.key
        page = requests.get(url).json()
        print(page)
        return page["data"]
