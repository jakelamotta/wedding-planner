import os

class Config():

    config = None

    def __init__(self):

        self.config = {}

        if ("DB_PASSWORD" in os.environ):
            self.config["DB_PASSWORD"] = os.environ['DB_PASSWORD']
        else:
            self.config["DB_PASSWORD"] = "password"


        if ("DB_HOST" in os.environ):
            self.config["DB_HOST"] = os.environ['DB_HOST']
        else:
            self.config["DB_HOST"] = "localhost"

        if ("DB_PORT" in os.environ):
            self.config["DB_PORT"] = os.environ['DB_PORT']
        else:
            self.config["DB_PORT"] = "3306"
        
    def getConfig():

        if (Config.config == None):
            Config.config = Config()

        return Config.config
