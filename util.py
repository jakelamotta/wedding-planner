import os
import smtplib
import logging

class Config():

    config = None

    def __init__(self):

        self.config = {}
        
    def getConfig():

        if (Config.config == None):
            Config.config = Config()

        return Config.config

class EmailHelper():

    def __init__(self, sSE = False):
        config = Config.getConfig()

        self.smtpServer = config.config["SMTP_SERVER_URL"]
        self.sender = "noreply@scila.se"
        self.shouldSendEmail = sSE

        if (not self.shouldSendEmail):
            logging.info("Mock email sender active")
            
    def sendEmail(self,recipient, message):

        if (not self.shouldSendEmail):
            logging.info("Mock sending email..")
            return True
        
        try:
           smtpObj = smtplib.SMTP(self.smtpServer)
           result = smtpObj.sendmail(self.sender, recipient, message)
           logging.info(result)
        except smtplib.SMTPException:
           return False

        return True

