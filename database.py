import sqlite3
import json
import time
    
import QueryGenerator as generateQuery
from entry import Entry


defaultTable = {
    "ID": ["INTEGER", "PRIMARY KEY", "AUTOINCREMENT"],
    "time": "INTEGER", # time (duration) measured in minutes
    "date": "INTEGER", # UNIX time string the entry was created at
    "description": "TEXT", # optional description to entry
    }

defaultConfig = {
    "tags": [],
    "tagDescriptions": {}
    }

defaultTagArgs = ("INT", "DEFAULT 0")

areYouSure = False

class Database:

    def __init__(self, start=True):
        if start:
            self.start()


    def start(self, checkDB=True):
        self.loadConfig()
        self.loadDB()

        if checkDB: self.checkDB()


    def loadConfig(self):
        with open("./config.json", "r") as file:
            self.config = json.load(file)


    def saveConfig(self):
        with open("./config.json", "w") as file:
            json.dump(self.config, file, indent=2)

            
    def loadDB(self):
        self.db = sqlite3.connect("time.db")
        self.db.isolation_level = None


    def checkDB(self, createNew=True):
        try:
            self.db.execute("SELECT * FROM Time LIMIT 0;")
            return True
            
        except sqlite3.OperationalError:
            if not createNew: return False

            query = generateQuery.createTable("Time", defaultTable)
            return self.db.execute(query)


    @property
    def tags(self):
        return self.config["tags"]


    def createTag(self, tagName):
        if tagName in self.config["tags"]:
            print("That tag already exists.")
            return
        
        query = generateQuery.addColumn("Time", tagName, ["INT", "DEFAULT 0"])

        self.db.execute(query)
        self.config["tags"].append(tagName)


    def getTags(self):
        query = generateQuery.getColumns("Time")
        columns = self.db.execute(query).fetchall()
        # ^ returns a tuple of the following information:
        # column number, column name, column type, bool that signifies whether it can
        # be "null", the default value, bool that signifies if it's a primary key
        
        tags = [column[1] for column in columns[4:]]
        # skip ID, time, date and description columns
        
        return tags


    def newTag(self, tag, description=None):
        query = generateQuery.addColumn("Time", tag, defaultTagArgs)
        self.db.execute(query)
        
        self.config["tags"].append(tag)
        
        if description:
            self.config["tagDescriptions"][tag] = description
        
        self.saveConfig()


    def getTagDiff(self):
        dbTags = self.getTags()
        if dbTags == self.config["tags"]: return "No diff"
        
        dbTags = set(dbTags)
        confTags = set(self.config["tags"])

        diffTags = dbTags.symmetric_difference(confTags)

        if not diffTags: return "Wrong order" # they are the same

        missingDbTags = diffTags - dbTags
        missingConfTags = diffTags - confTags

        return missingDbTags, missingConfTags


    def loadTagsFromDB(self):
        self.config["tags"] = self.getTags()
        self.saveConfig()


    def newEntry(self, hours, tags: tuple, description=""):
        args = {}
        args["time"] = int(hours*60)
        args["date"] = int(time.time())
        
        if description: args["description"] = description

        args.update( {tag: 1 for tag in tags} )
        
        self.db.execute(generateQuery.insert("Time", args))


    def setTagDescription(self, tag, description, updatedb=True):
        if not tag in self.tags: return "Tag does not exist"
        self.config["tagDescriptions"][tag] = description
        if updatedb: self.saveConfig()


    def tagDescription(tag):
        return self.config["tagDescriptions"][tag]


    def getLatest(self):
        query = generateQuery.select("Time", orderBy="ID DESC", limit=1)
        return Entry(self.db.execute(query).fetchone(), self)


    def getAll(self, raw=False):
        if raw: return self.db.execute(generateQuery.select("Time")).fetchall()
        return [Entry(x, self) for x in self.db.execute(generateQuery.select("Time")).fetchall()]


    def printAll(self):
        for entry in self.getAll():
            print(entry)


    def getMatching(self, include=None, exclude=None, raw=False):
        conditions = []
        
        if generateQuery.isIter(include):
            conditions = conditions + [f"Time.'{tag}'=1" for tag in include]
        
        if generateQuery.isIter(exclude):
            conditions = conditions + [f"Time.'{tag}'=0" for tag in exclude]
            
        query = generateQuery.select("Time", conditions)

        if raw: return self.db.execute(query).fetchall()
        
        matching = [Entry(x, self) for x in self.db.execute(query).fetchall()]
        if len(matching) == 1: return matching[0]
        return matching


    def disconnect(self):
        self.db.close()
            


    def factoryReset(self, *, force=False):
        global areYouSure

        if force or areYouSure:
            self.config = defaultConfig
            self.saveConfig()

            import os
            self.disconnect()
            os.remove("./time.db")

            print("Factory reset complete. Please restart the program.")

        else:
            areYouSure = True
            
            from threading import Thread

            def setBack():
                time.sleep(10)
                global areYouSure
                areYouSure = False
            
            Thread(target=setBack).start()

            print("Are you sure? Execute the command again within the next 30 seconds to confirm")
    
db = Database()


























































































# end
