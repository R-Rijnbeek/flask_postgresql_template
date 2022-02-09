# -*- coding: utf-8 -*-
"""
__init__.py: This module define the the webservice function build with Flask
"""
__author__          = "Robert Rijnbeek"
__version__         = "1.0.1"
__maintainer__      = "Robert Rijnbeek"
__email__           = "robert270384@gmail.com"
__status__          = "Development"

__creation_date__   = '07/02/2022'
__last_update__     = '09/02/2022'

# =============== IMPORTS ===============

# IMPORT OF FLASK AND FLASK LIBRARIES
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# DIRECTORY MANAGENMENT LIBRARIES
from os import path, getcwd, makedirs

# TIME MANAGENMENT LIBRARIES
import time

# IMPORT THE WEBSERVICE MANAGENMENT LIBRARIES
from .webservice import VisualWebService, MiniJSONEncoder



def OpenWebservice():
    """
    INFORMATION: Fuction that activate the webservice with the selected configuration values of url, Port and debug mode and SQL configuration defined in "dev_config.cfg"
    INPUT: None
    OUTPUT:None
    """
    try:
        # BUILD Logfiles Directory IF IT DOES NOT EXISTS
        if not path.exists('Logfiles'):
            makedirs('Logfiles')
        # BUILDING THE log file path name. 
        LOG_FILE_PATH = path.join(getcwd() +'/Logfiles/log_'+time.strftime("%d_%b_%Y_%H_%M_%S",time.localtime())+'.txt')
        # BUILDING THE MAIL INSTANCE TO WILL BE EMBEDDED IN FLASK
        MAIL = Mail()
        # BUILDING THE SQLALCHEMY INSTANCE TO WILL BE EMBEDDED IN FLASK
        DB = SQLAlchemy()
        # DEFINING OF THE FLASK OBJECT
        app = Flask(__name__)
        # CONFIGURE THE FLASK OBJECT with the 'dev_config.cfg' configuration file
        app.config.from_pyfile("dev_config.cfg")
        #REDEFINE THE MAIL INSTANCE WITH THE NEW MAIL CONFIGURATION OF FLASK
        MAIL.init_app(app)
        # GET THE EMAIL ADRESS FROM THE FLASK INSTANCE CONFIGURATION
        MAIL_SENDER = app.config["MAIL_USERNAME"]
        #REDEFINE THE SQLALCHEMY INSTANCE WITH THE NEW SQL CONFIGURATION OF FLASK
        DB.init_app(app)
        # GET THE DATABASE NAME FROM THE FLASK INSTANCE CONFIGURATION
        DB_NAME = app.config["SQLALCHEMY_DATABASE_NAME"]
        # GET THE APLICATION CONFIGURATION INFO:
        PROCESS_CONFIGURATION_FILE = app.config["APLICATION_CONFIGURATION"]
        #DEFINING THE API OBJECT FROM FLASK RESTFULL TO MAKE IT POSSIBLKE TO INCLUDE IN EATCH REQUEST A GENERIC CLASS INSTANCE WITH VARIABLES
        api = Api(app)
        # ADD A LINK TO A SPECIFIC WEB REQUEST WITH A CLASS METHOD WITH ARGUMENTS
        api.add_resource(VisualWebService, '/<METHOD>',resource_class_kwargs={'DATABASE_CONNECTION': DB,"DATABASE_NAME":DB_NAME,"MAIL":MAIL,"MAIL_SENDER":MAIL_SENDER,"LOG_PATH":LOG_FILE_PATH,"PROCESS_CONFIGURATION_FILE":PROCESS_CONFIGURATION_FILE})
        # CHANGE THE JSON ENCODER OF THE FLASK OBJECT TO SAVE SPACE OF THE JSON AOUTPUT
        app.json_encoder = MiniJSONEncoder
        #EXECUTE THE FLASK INSTANCE TO MAKE THE WEBSERVICE ACTIVE
        app.run()
        return True
    except Exception as exc:
        print(f"ERROR: unexpected error activting the webservice process: {exc}")
        return False

# =============== EXECUTE TEST CODE ===============

if __name__ == "__main__":
    pass