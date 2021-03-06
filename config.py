import json

#Load config from config.json
class config:
    def __init__(self):
        #Dictionart
        self.configDict = self.loadConfig("config/config.json")

        #Four Vars
        self.owner = self.configDict['bot-owner']
        self.admins = self.configDict['admins'] 
        self.botToken = self.configDict['bot-token']
        #I can count

    #Load dict from file
    def loadConfig(self, configFile):
        with open(configFile) as json_file:
            return json.load(json_file)
        #json_file = open(configFile)
        #json_string = json_file.read()
        

    #Assign all
    def assignConfig(self):
        self.owner = self.configDict['bot-owner']
        self.admins = self.configDict['admins']   
        self.botToken = self.configDict['bot-token']

    #Method for reloading the config
    def reloadConfig(self):
        self.configDict = self.loadConfig("config/config.json")
        self.assignConfig()

    def editConfig(self, admins=None, cmdCh=None, rollChange=None, messageChange=None):
        if (admins != None):
            self.configDict['admins'] = admins

        self.saveConfig()
        self.reloadConfig()
        
    def saveConfig(self):
        with open('config/config.json', 'w') as outfile:
            json.dump(self.configDict, outfile, indent=4, ensure_ascii=False)

