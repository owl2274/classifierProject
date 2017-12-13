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

    def test(self):
        url = self.base_url + "/platform/v3/champions" + "?api_key=" + self.key
        getUrl = requests.get(url)

        page = getUrl.json()
        print(page)
        error = None
        try:
            if page["status"] != None:
                raise ValueError
        except KeyError:
            pass




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

if __name__ == "__main__":
    api = LOLApi("RGAPI-4926c32e-4eb2-4488-989e-d98cca818c4d")
    api.test()
    api = LOLApi("RGAPI-e43bd3e5-af3c-4c9e-8743-f11a0b2e59f5")
    api.test()