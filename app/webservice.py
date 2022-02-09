#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
api.py: This module create an webservice process dedicated for the VisualPresencia Calculator
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
from flask import jsonify
from flask.json import JSONEncoder
from flask_restful import Resource

# IMPORT OF THE PROCESS CLASS 
from .Process import Process

# =============== CODE ===============

class MiniJSONEncoder(JSONEncoder):
    """Minify JSON output."""
    item_separator = ','
    key_separator = ':'

class VisualWebService(Resource, Process):
    def __init__(self,DATABASE_CONNECTION,DATABASE_NAME,MAIL,MAIL_SENDER,LOG_PATH,PROCESS_CONFIGURATION_FILE):
        # INIT OF SUBCLASS VisualPresencia_PROCESS
        Process.__init__(self)
        # GET INITIAL DATABASE CONNECTION
        self.database_connection = DATABASE_CONNECTION
        self.database_name  = DATABASE_NAME
        # DEFINE THE LOGGING FILE VARIABLE
        self.log_file_path = LOG_PATH
        self.log = open(self.log_file_path,'a+')
        # DEFINE THE MAIL OBJECT
        self.mail = MAIL 
        self.mail_sender = MAIL_SENDER
        # DEFINE THE PROCESS CONFIGURATION FILE
        self.process_configuration_file = PROCESS_CONFIGURATION_FILE
  
    def get(self, METHOD):
        """
        INFORMATION: This function the webpage host on the defined URL. Where 'METHOD' is the requested method in the URL.
        INPUT: 
            - METHOD: (STRING) 
        OUTPUT:
            - The output of the  'GetResponce() function. Whos is an JSON object that is posted in the webpage as result
        """
        if METHOD == "favicon.ico":
            pass
        else:
            self.LOG_Header()
            #self.LOG_BeginLoops()
            self.DefineMethodFromURL(METHOD)
            if self.Valid_Method_Q():
                if self.DefineVariableListByMethod(METHOD):
                    if self.DefineArgumentObjectFromURL():
                        self.Process()
            return self.GetResponse()

    def GetResponse(self):
        """
        INFORMATION: This function build the responce that is printed in the webpage. 
        INPUT: 
            - None
        OUTPUT:
            - DICT in the form as: {"SUCCES":<STATUS>,"DATA":<REQUEST>} Those have two variables:
                - ERROR => True, Process() had errors
                    - <STATUS>: (BOOLEAN) True, defined by class variable: self.request_status
                    - <REQUEST>: empty dict, {}, defined by class variable: self.request
                - ERROR => False, Process() without errors
                    - <STATUS>: (BOOLEAN) False, defined by class variable: self.request_status
                    - <REQUEST>:dict, defined by class variable: self.request THad is build with the process: Process().
                                That has the form as: self.OutputTemplate()
        """
        self.InfoEvent("\tINFO: WRITING WEBREQUEST RESPONSE OUTPUT:")
        try:
            output=jsonify({"SUCCES":self.request_status,"DATA":self.request})
            self.InfoEvent("\tINFO: Output is an valid JSON object")
            self.EXIT()
            return output
        except:
            self.ErrorEvent("\tERROR: Output is not an valid JSON.")
            self.EXIT()
            return jsonify({"SUCCES":False,"DATA":{}})

# =============== EXECUTE OF THE TEST CODE ===============

if __name__ == "__main__":
    pass