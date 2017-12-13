
import csv


class LOLDatabase:

    def useDatabase(self):
        average = open("libraries/dataOfAverage.csv", "rt")
        self.csvOfAverage = csv.DictReader(average)

        spellids = open("libraries/spellids.csv", "rt")
        self.csvOfSpellids = csv.DictReader(spellids)

        champion =  open("libraries/champion.csv", 'rt')
        self.csvOfChampion = csv.DictReader(champion)

    def insertChampionId(self, championIdList):
        pass

    def showChampionId(self, choosedata='*'):
        championIdData = []
        for row in self.csvOfChampion:
            if len(row) != 0:
                championIdData.append(row)

        return championIdData[1:]



    def insertSummonerSpell(self, spellList):
        pass

    def insertChampionAverage(self, championId, championdata):
       pass

    def showChmpionAverage(self, championId=None, mostUsableSpell=None, secondUsableSpell=None, thirdUsableSpell=None,
                           choosedata='*'):
        pass

    def close(self):
        self.cur.close()
        self.conn.close()
