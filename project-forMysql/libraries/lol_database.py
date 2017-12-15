import pymysql

settingCommands = ["CREATE DATABASE leagueoflegend",
                   "USE leagueoflegend",
                   "CREATE TABLE summoner("
                         "name VARCHAR(16),"
                         "profileIconId INT(11),"
                         "summonerLevel BIGINT(20),"
                         "revisionDate BIGINT(20),"
                         "id BIGINT(20),"
                         "accountId BIGINT(20),"
                         "PRIMARY KEY(accountId)"
                         ")DEFAULT CHARSET=utf8",
                   "CREATE TABLE matchreference("
                         "gameId BIGINT(20),"
                         "lane VARCHAR(16),"
                         "champion INT(11),"
                         "platformId VARCHAR(8),"
                         "season INT(11),"
                         "queue INT(11),"
                         "role VARCHAR(16),"
                         "timestamp BIGINT(20),"
                         "PRIMARY KEY(gameId)"
                         ")DEFAULT CHARSET=utf8",
                   "CREATE TABLE individualGamer("
                         "gamerid BIGINT(20),"
                         "gameid BIGINT(20) NOT NULL,"
                         "accountId BIGINT(20) NOT NULL,"
                         "championId INT(11) NOT NULL,"
                         "kills INT(11) NOT NULL,"
                         "deaths INT(11) NOT NULL,"
                         "assists INT(11) NOT NULL,"
                         "totalMinionsKilled INT(11) NOT NULL,"
                         "goldEarned INT(11) NOT NULL,"
                         "timeCCingOthers INT(11) NOT NULL,"
                         "totalDamageDealtToChampions INT(11) NOT NULL,"
                         "totalDamageTaken INT(11) NOT NULL,"
                         "visionScore INT(11) NOT NULL,"
                         "spell1Id INT(11) NOT NULL,"
                         "spell2Id INT(11) NOT NULL,"
                         "win TINYINT(1) NOT NULL,"
                         "gameDuration INT(11) NOT NULL,"
                         "PRIMARY KEY(gamerid)"
                         ")DEFAULT CHARSET=utf8",
                   "CREATE TABLE champion("
                         "championId INT(11),"
                         "championName VARCHAR(16),"
                         "PRIMARY KEY(championId)"
                         ")DEFAULT CHARSET=utf8",
                   "CREATE TABLE spell("
                         "spellId INT(11),"
                         "spellName VARCHAR(32),"
                         "PRIMARY KEY(spellId)"
                         ")DEFAULT CHARSET=utf8",
                   "CREATE TABLE championaverage("
                         "championId INT(11),"
                         "kills FLOAT NOT NULL,"
                         "deaths FLOAT NOT NULL,"
                         "assists FLOAT NOT NULL,"
                         "totalMinionsKilled FLOAT NOT NULL,"
                         "goldEarned FLOAT NOT NULL,"
                         "timeCCingOthers FLOAT NOT NULL,"
                         "totalDamageDealtToChampions FLOAT NOT NULL,"
                         "totalDamageTaken FLOAT NOT NULL,"
                         "visionScore FLOAT NOT NULL,"
                         "mostUsableSpell INT(11) NOT NULL,"
                         "secondUsableSpell INT(11) NOT NULL,"
                         "thirdUsableSpell INT(11) NOT NULL,"
                         "PRIMARY KEY(championId)"
                         ")DEFAULT CHARSET=utf8"
                   ]

class LOLDatabase:
    def __init__(self,user, passwd,host='127.0.0.1',  db='mysql', charset='utf8'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db,charset=self.charset)
        self.cur = self.conn.cursor()
        self.cur.connection.autocommit(True)

        for command in settingCommands:
            try:
                self.cur.execute(command)
                self.cur.connection.commit()

            except pymysql.err.InternalError as e:
                if e.args[0] == 1050:
                    pass
                    #print("command is already conducted: \n{}".format(command))

                else:
                    raise e
            except pymysql.err.ProgrammingError as e:
                if e.args[0] == 1007:
                    #print("command is already conducted: \n{}".format(command))
                    pass
                else:
                    raise e

    def useDatabase(self):
        self.cur.execute("USE LeagueOfLegend")

    def insertSummoner(self,json):
        try:
            self.cur.execute("INSERT INTO summoner (name,profileIconId,summonerLevel,revisionDate,id,accountId) VALUES (\"{}\",{},{},{},{},{})".format(json["name"],json["profileIconId"],json["summonerLevel"],json["revisionDate"],json["id"],json["accountId"]))
            print("INSERT INTO summoner (name,profileIconId,summonerLevel,revisionDate,id,accountId) VALUES (\"{}\",{},{},{},{},{})".format(json["name"],json["profileIconId"],json["summonerLevel"],json["revisionDate"],json["id"],json["accountId"]))
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062: #중복일시 패스
                print(e)
            else:
                raise e
    def showSummoner(self,name=None,profileIconId=None,summonerLevel=None,revisionDate=None,id=None,accountId=None,choosedata="*"):
        sql = "SELECT "+choosedata+" from summoner"
        condition = ""
        param_list = [name,profileIconId,summonerLevel,revisionDate,id,accountId]
        param_strings= [" name=\"{}\""," profileIconId={}"," summonerLevel={}"," revisionDate={}"," id={}"," accountId={}"]
        for string,param in zip(param_strings,param_list):
            if param != None:
                if condition != "":
                    condition += " and"
                condition += string.format(param)

        if condition != "":
            sql += " WHERE" + condition
        self.cur.execute(sql)

        return self.cur.fetchall()

    def insertMatchID(self,jsonlist):
        for i,json in enumerate(jsonlist):
            try:
                self.cur.execute("INSERT INTO matchreference (gameId,lane,champion,platformId,season,queue,role,timestamp)"
                                 "VALUES ({},\"{}\",{},\"{}\",{},{},\"{}\",{})"
                                 .format(json["gameId"],json["lane"],json["champion"],json["platformId"],json["season"],json["queue"],json["role"],json["timestamp"]))
                print(
                    "INSERT INTO matchreference (gameId,lane,champion,platformId,season,queue,role,timestamp)"
                    "VALUES ({},\"{}\",{},\"{}\",{},{},\"{}\",{})"
                    .format(json["gameId"], json["lane"], json["champion"], json["platformId"], json["season"],
                            json["queue"], json["role"], json["timestamp"]))

                self.cur.connection.commit()

            except pymysql.err.IntegrityError as e:
                if e.args[0] == 1062:#중복 제외
                    print(e)
                else:
                    raise e
            
    def showMatchID(self,gameId=None,lane=None,champion=None,platformId=None,season=None,queue=None,role=None,timestamp=None,choosedata='*'):
        sql = "SELECT " + choosedata + " from matchreference"
        condition = ""
        param_list = [gameId, lane, champion, platformId, season, queue,role,timestamp]
        param_strings = [" gameId={}", " lane=\"{}\"", " champion={}", " platformId=\"{}\"", " season={}",
                         " queue={}","role=\"{}\"","timestamp={}"]
        for string, param in zip(param_strings, param_list):
            if param != None:
                if condition != "":
                    condition += " and"
                condition += string.format(param)

        if condition != "":
            sql += " WHERE" + condition
        self.cur.execute(sql)
        return self.cur.fetchall()

    def insertIndividualGamer(self,matchJson):
        for i,(identity,participant) in enumerate(zip(matchJson["participantIdentities"],matchJson["participants"])):
            try:
                self.cur.execute(
                "INSERT INTO individualGamer (gamerid,gameid,accountId,championId,kills,deaths,assists,totalMinionsKilled,goldEarned,timeCCingOthers,totalDamageDealtToChampions,totalDamageTaken,visionScore,spell1Id,spell2Id,win,gameDuration)"
                "VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})"
                .format(int(str(matchJson["gameId"])+str(identity["player"]["accountId"])),matchJson["gameId"], identity["player"]["accountId"], participant["championId"],
                        participant["stats"]["kills"], participant["stats"]["deaths"], participant["stats"]["assists"],
                        participant["stats"]["totalMinionsKilled"], participant["stats"]["goldEarned"],
                        participant["stats"]["timeCCingOthers"], participant["stats"]["totalDamageDealtToChampions"],
                        participant["stats"]["totalDamageTaken"], participant["stats"]["visionScore"],
                        participant["spell1Id"], participant["spell2Id"], participant["stats"]["win"],
                        matchJson["gameDuration"]))
                self.cur.connection.commit()
            except pymysql.err.IntegrityError as e:
                if e.args[0] == 1062:
                    print(e)
                else:
                    raise e

    def showIndividualGamer(self,gameid=None,accountId=None,championId=None,win=None,choosedata='*'):
        sql = "SELECT " + choosedata + " from individualGamer"
        condition = ""
        param_list = [gameid, accountId, championId, win]
        param_strings = [" gameid={}", " accountId={}", " championId={}", " win={}"]
        for string, param in zip(param_strings, param_list):
            if param != None:
                if condition != "":
                    condition += " and"
                condition += string.format(param)

        if condition != "":
            sql += " WHERE" + condition
        self.cur.execute(sql)
        return self.cur.fetchall()

    def insertChampionId(self,championIdList):
        for championId in championIdList:
            try:
                self.cur.execute("INSERT INTO champion (championId,championName) VALUES({},\"{}\")".format(championId,championIdList[championId]))
                self.cur.connection.commit()
            except pymysql.err.IntegrityError as e:
                if e.args[0] == 1062:
                    print(e)
                else:
                    raise e
    def showChampionId(self,championId=None,championName=None,choosedata='*'):
        sql = "SELECT " + choosedata + " from champion"
        condition = ""
        param_list = [championId, championName]
        param_strings = [" championId={}", " championName=\"{}\""]
        for string, param in zip(param_strings, param_list):
            if param != None:
                if condition != "":
                    condition += " and"
                condition += string.format(param)

        if condition != "":
            sql += " WHERE" + condition
        self.cur.execute(sql)
        return self.cur.fetchall()
    def insertSummonerSpell(self,spellList):
        for key in spellList:
            try:
                self.cur.execute("INSERT INTO spell (spellId,spellName) VALUES({},\"{}\")".format(spellList[key]["id"],spellList[key]["name"]))
                self.cur.connection.commit()
            except pymysql.err.IntegrityError as e:
                if e.args[0]==1062:
                    print(e)
                else:
                    raise e
    def showSummonerSpell(self,spellId=None,spellName=None,choosedata='*'):
        sql = "SELECT " + choosedata + " from spell"
        condition = ""
        param_list = [spellId,spellName]
        param_strings = [" spellId={}", " spellName={}"]
        for string, param in zip(param_strings, param_list):
            if param != None:
                if condition != "":
                    condition += " and"
                condition += string.format(param)

        if condition != "":
            sql += " WHERE" + condition
        self.cur.execute(sql)

        return self.cur.fetchall()

    def insertChampionAverage(self,championId,championdata):
        a=championdata
        self.cur.execute("INSERT INTO championAverage "
                         "(championId,kills,deaths,assists,totalMinionsKilled,goldEarned,timeCCingOthers,totalDamageDealtToChampions,totalDamageTaken,visionScore,mostUsableSpell,secondUsableSpell,thirdUsableSpell) "
                         "VALUES({},{},{},{},{},{},{},{},{},{},{},{},{})".format(championId,a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11]))
        self.cur.connection.commit()
    def removeChampionAverage(self):
        self.cur.execute("DELETE FROM championAverage")
        self.cur.connection.commit()
    def showChmpionAverage(self,championId=None,mostUsableSpell=None,secondUsableSpell=None,thirdUsableSpell=None,choosedata='*'):
        sql = "SELECT " + choosedata + " from championaverage"
        condition = ""
        param_list = [championId,mostUsableSpell,secondUsableSpell,thirdUsableSpell]
        param_strings = [" championId={}", " mostUsableSpell={}"," secondUsableSpell={}"," thirdUsableSpell={}"]
        for string, param in zip(param_strings, param_list):
            if param != None:
                if condition != "":
                    condition += " and"
                condition += string.format(param)

        if condition != "":
            sql += " WHERE" + condition
        self.cur.execute(sql)
        return self.cur.fetchall()

    def fetchone(self):
        self.cur.fetchone()
    def fetchall(self):
        self.cur.fetchall()
    def close(self):
        self.cur.close()
        self.conn.close()

