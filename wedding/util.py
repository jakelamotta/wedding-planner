import os
import smtplib

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

        if ("SMTP_USERNAME" in os.environ):
            self.config["SMTP_USERNAME"] = os.environ['SMTP_USERNAME']
        else:
            self.config["SMTP_USERNAME"] = "test"

        if ("SMTP_PASSWORD" in os.environ):
            self.config["SMTP_PASSWORD"] = os.environ['SMTP_PASSWORD']
        else:
            self.config["SMTP_PASSWORD"] = "test"

        if ("SMTP_SERVER" in os.environ):
            self.config["SMTP_SERVER"] = os.environ['SMTP_SERVER']
        else:
            self.config["SMTP_SERVER"] = "test"

        if ("SECRET_KEY" in os.environ):
            self.config["SECRET_KEY"] = os.environ['SECRET_KEY']
        else:
            self.config["SECRET_KEY"] = "test"
        
    def getConfig():

        if (Config.config == None):
            Config.config = Config()

        return Config.config

class EmailHelper():

    def __init__(self):
        self.config = Config.getConfig().config
        self.smtpServer = self.config["SMTP_SERVER"]
        self.sender = "noreply@banaj-johansson.se"

    def sendEmail(self,recipient, message):
        try:
           username = self.config["SMTP_USERNAME"]
           if (username == "test"):
            print(message)
            return True

           smtpObj = smtplib.SMTP(self.smtpServer, port=587)
           smtpObj.starttls()
           smtpObj.login(username, self.config["SMTP_PASSWORD"])
           result = smtpObj.sendmail(self.sender, recipient, message.encode("utf-8"))
        except Exception as e:
           print(e)
           return False

        return True