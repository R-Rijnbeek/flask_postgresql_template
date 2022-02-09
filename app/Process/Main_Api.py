#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main_Api.py: Libreria con funcionalidades basicas que se puede usar como base de cualquier proyecto en Python
"""
__author__          = "Robert Rijnbeek"
__version__         = "1.0.1"
__maintainer__      = "Robert Rijnbeek"
__email__           = "robert270384@gmail.com"
__status__          = "Development"

__creation_date__   = '07/02/2022'
__last_update__     = '09/02/2022'

# =============== IMPORTS ===============

# IMPORT OF STANDARD OS LIBRARIES
from os import path, getcwd

# IMPORT OF STANDARD DATE/TIME LIBRARIES
from datetime import datetime
import time

#IMPORT OF THE NUMPY LIBRARY
import numpy as np

# IMPORT OF FLASK AND FLASK LIBRARIES
from flask import request, copy_current_request_context
from flask_mail import Message

# LIBRARY TO MAKE IT POSSIBLE TO SEND EMAIL ASYNCHRONNOUSLY
import threading

# IMPORT OF THE deque LIBRARY FROM 'collections' FORR TEXT FILE MAANAGENMENT
from collections import deque

#IMPORT OF JSON LABRARY
import json

# ============= DECORATOR ==========

def argument_check(*types_args,**types_kwargs):
    """
    INFORMATION: Standard decorator with arguments that is used to verify the agument (arg) or opttion arguments (kwargs) 
                 of linked function. If the decorator see an not valid argument or kwarg in the funcion. 
                 There will be generate an exception with the explanation with the argument that is not correct.
    INPUT: 
        - *types_args: Tuple of arguments where eatch argument can will be a a type (simple object type) or types of 
                       object types (when you define a tuple of objects). Or if it is defined as an list. Those values of the list 
                       are the option of the values thay those arguments can will be.
        - **types_kwargs: dict of kwargs where eatch argument can will be a a type (simple object type) or types of object types 
                          (when you define a tuple of objects). Or if it is defined as an list for a key of a dict. The keyvalue of a
                          dict must be in the defined list liked to that veyvalue.
    OUTPUT:
        - ERROR: EXECUTION OF THE LINKED FUNCTION
        - NO ERROR: A DEFINED EXCEPTION
    """
    def check_accepts(f):
        def function_wrapper(*args, **kwargs):
            if len(args) is not  len(types_args):
                assert isinstance(args, types_args), f"In function '{f.__name__}{args}' and option values: {kwargs}, lenght of argumnets {args} is not the same as types_args {types_args}"
            for (arg, type_arg) in zip(args, types_args):
                if isinstance(type_arg,list):
                    assert arg in type_arg, f"In function '{f.__name__}{args}' and option values: {kwargs}, argument {arg} is not in list {type_arg}" 
                else:
                    assert isinstance(arg, type_arg), f"In function '{f.__name__}{args}' and option values: {kwargs}, arg {arg} does not match {type_arg}" 
            for kwarg,value in kwargs.items():
                assert kwarg in types_kwargs , f"In function '{f.__name__}{args}' and option values: {kwargs}, the kwarg ('{kwarg}':{value}) is not a valid option value" 
                espected_format = types_kwargs[kwarg]
                if isinstance(espected_format,list): 
                    assert value in espected_format, f"In function '{f.__name__}{args}' and option values: {kwargs}, the kwarg value ('{kwarg}':{value}) is not in list {espected_format}" 
                else:
                    assert isinstance(value, espected_format), f"In function '{f.__name__}{args}' and option values: {kwargs}, kwarg value ('{kwarg}':{value}) does not match with {espected_format}" 
            return f(*args, **kwargs)
        function_wrapper.__name__ = f.__name__
        return function_wrapper
    return check_accepts

# =============== CLASES =============

class Main_API:
    def __init__(self):
        self.Errors = 0
        self.Warnings = 0
        # DATABASE CONNECTION:
        self.database_connection = None
        # DATABASE SELECT RESULT:
        self.database_result = None
        # DATABASE SCRIPT:
        self.database_script = None
        #TIME
        self.epochtime=time.time()
        self.actual_datetime_tuple = self.GetActualDateTime_Tuple()
        # APLICATION CONFIGURATION FILE
        self.process_configuration_file = None
        # WEBSERVICE ARGUMENTS
        self.method = None
        self.argument_list = []
        self.argument_object = {}
        # REQUEST
        self.request={}
        self.request_status=False
        # MAIL 
        self.mail = None
        self.mail_sender = None

    #=============== EMAIL MANAGENMENT ===============

    @argument_check(object,str, str, RECIPIENTS_LIST = (list,type(None)), SENDER =(str,type(None)), BODY_TYPE = ["txt","html"], SYNCHRONE = bool)
    def SendMail(self,SUBJECT,BODY,RECIPIENTS_LIST = None,SENDER = None, BODY_TYPE = "txt",SYNCHRONE = True):
        """
        INFORMATION: Standard method to send e-mails where you must define an subject and an body of the email.
        INPUT:
            - SUBJECT: STRING => Is the subject text of the email
            - BODY: (STRING) => is the body of the mail
            - RECIPIENTS_LIST (LIST) => (OPTIONAL) Is a list of the email addresses to send the email. If it is not defined
                                        it will be send with the global var: 'self.mail_sender' defined when the webservice is activated
            - SENDER (STRING) => (OPTIONAL) Is the senders email adres. If it is not defined it will me seded by: 'self.mail_sender'
                                 defined when the webservice is activated
            - BODY_TYPE (STRING) => (OPTIONAL) Is the type of body that will be include in the email body. There are two choices: 'txt' (default) or 'html'
            - SYNCHRONE (BOOLEAN) => (OPTIONAL) Is the option to send the email. There are two options:
                    - SYNCHRONE = True: When this protocol will wait to get the responce when you send an email 
                    - SYNCHRONE = False: When this protocol will not wait to get the responce when you send an email.
        OUTPUT:
            - STATUS: ERROR => False
            - STATUS: NO ERROR => BOOLEAN => True 
        """
        try:
            if RECIPIENTS_LIST is None:
                RECIPIENTS_LIST = [self.mail_sender]
            if SENDER is None:
                SENDER = self.mail_sender
            msg = Message(SUBJECT, sender=SENDER, recipients=RECIPIENTS_LIST)
            if BODY_TYPE == "txt":
                msg.body = BODY
            elif BODY_TYPE == "html":
                msg.html = BODY
            else:
                self.WarningEvent(f"\tWarning: BODY_TYPE kwark is not on of the following options: 'txt' or 'html' the BODY_TYPE kwark is setted as 'txt'")
                msg.body = BODY
            if SYNCHRONE:
                self.mail.send(msg)
            else:
                @copy_current_request_context
                def send_message(message):
                    self.mail.send(message)
                sender = threading.Thread(name='mail_sender', target=send_message, args=(msg,))
                sender.start()
            return True
        except Exception as Exc:
            self.ErrorEvent(f"\tERROR: Unespected error in sending email: {Exc}",SEND_EMAIL=False)
            return False

    #=============== PROCESS MANAGENMENT ===============


    def Valid_Method_Q(self):
        """
        INFORMATION:    Validating Process that see if the class variable 'self.method' is an valid method. 
                        Those Method must bi in the list 'self.method_list'
        INPUT: None 
        OUTPUT:
            STATUS: ERROR
                - BOOLEAN => False
            STATUS: NO ERROR
                - BOOLEAN => True
        """
        self.InfoEvent("\tINFO: VALIDATING OF THE METHOD FROM URL.")
        METHOD = self.method
        if METHOD in self.process_configuration_file:
            self.InfoEvent("\tINFO: The method '" + str(self.method)+ "' is a valid method")
            return True
        else:
            self.WarningEvent("\tINFO: "+self.method + " is not a valid Method")
            #self.EXIT()
            return False

    @argument_check(object,str)
    def DefineVariableListByMethod(self, METHOD):
        try:
            self.argument_list = self.process_configuration_file[METHOD]
            return True
        except:
            return False

    @argument_check(object,str)
    def GetArgumentFromURL(self,ARGUMENT_NAME):
        """
        INFORMATION: Gat the value of an selected ARGUMENT_NAME from the URL
        INPUT: 
            - ARGUMENT_NAME (STRING): This is the argument those this function get the value
        OUTPUT:
            - STRING: Is the Value of the selected ARGUMENT_NAME from the URL
        """
        return request.args.get(ARGUMENT_NAME)
    
    
    def DefineArgumentObjectFromURL(self):
        """
        INFORMATION: Function that create a DICT (self.argument_object) with all the selected ARGUMENTS and Values from the URL In the form as: {"<ARGUMENT_NAME>":<ARGUMENT_VALUE>,.....}
        INPUT: None
        OUTPUT: BOOLEAN => True
        """
        for argument in self.argument_list:
            value = self.GetArgumentFromURL(argument)
            self.argument_object[argument] = value
        return True
    
    @argument_check(object,str)
    def DefineMethodFromURL(self, METHOD):
        """
        INFORMATION: Setter that define de Class variable: self.method
        INPUT: 
            - METHOD: (STRING), Is the method that is catch from the URL
        OUTPUT:
            - BOOLEAN => True
        """
        self.method = METHOD
        return True

    #=============== SQL MANAGEMENT ====================
   
    @argument_check(object,str)
    def SQL_Select(self,SQL_STRING):
        """
        INFORMATION: Function that execute an MySQL database query with the 'self.database_connection' and archive the result under the class variable: self.database_result
        INPUT: 
            - SQL_STRING (STRING): The query text string
        OUTPUT:
            - STATUS: NO ERROR
                - BOOLEAN => True
            - STATUS: ERROR
                - BOOLEAN => False
        """
        try:
            self.database_result=self.database_connection.engine.execute(SQL_STRING).fetchall()
            return True
        except:
            self.ErrorEvent("\tERROR: Database querry error")
            return False
        

    def SQL_Select_GetRequest(self):
        """
        INFORMATION: Getter function that get as result the variable 'self.database_result' That is the result of the lastdatabase querry
        
        INPUT: None
        OUTPUT:
            - TABLE: (lIST OF lIST): Is the result of the database query [[row1],[row2]......]
        """
        return self.database_result

    def SQL_Disconnect(self):
        """
        INFORMATION: Function That disconnect the database connection archived under tthe class variable: self.database_connection 
        
        INPUT: None
            
        OUTPUT:
            - STATUS: NO ERROR
                - BOOLEAN => True
            - STATUS: ERROR
                - BOOLEAN => False
        """
        try:
            if self.database_connection is not None:
                self.database_connection.close()
                return True
            else:
                return True
        except:
            self.ErrorEvent("\tWARNING: Database connection error")
            return False

    @argument_check(object,list)
    def Make_SQL_List(self, LIST):
        """
        INFORMATION: Function that create an valid SQL list string from the argument LIST
        
        INPUT: 
            - LIST (LIST): An valid Python list    
        OUTPUT:
            - STRING: A valid SQL list string
        """
        return str(LIST).replace("[","(").replace("]",")")

    def Filter_By_List_String(self, ARG, LIST):
        """
        INFORMATION: function that create an valid SQL statement of if the Argument (ARG) is in list (LIST)
        
        INPUT:
            - ARG (STRING): the argument if the statment
            - LIST (LIST): An valid Python list  
        OUTPUT:
            - STRING: A valid SQL statement string
        """
        if len(LIST)==0:
            return  ""
        else:
            return "and "+ARG+" in " + self.Make_SQL_List(LIST)

    # ================== IMPORT SQL SCRIPT ============

    @argument_check(object,str)
    def ImportSQLScript(self,SCRIPT_NAME):
        """
        INFORMATION: This function import a SQL script located in the directory ./Script/ with the name: SCRIPT_NAME. When the import process is succesfull. Those text is archived onder the class variable: self.database_script
        INPUT:
            -  SCRIPT_NAME (STRING): This is the name of the SQL script file
        OUTPUT:
            - STATUS: NO ERROR
                - BOOLEAN => True
            - STATUS: ERROR
                - BOOLEAN => False
        """ 
        try:
            with open(path.join(getcwd() + '\Script\\' + SCRIPT_NAME ), 'r', encoding="utf8") as content_file:
                try:
                    database_script = content_file.read()
                    self.database_script = database_script
                    return True
                except:
                    self.ErrorEvent("\tERROR: Content of'" + SCRIPT_NAME + "' has a wrong data format")
                    return False
        except:
            self.ErrorEvent("\tERROR: SQL script '" + SCRIPT_NAME + "' dous not exist")
            return False

    def GetSQLScript(self):
        """
        INFORMATION: Getter function that get as result the variable 'self.database_script' That is the result of the last import of the SQL script
        
        INPUT: None
        OUTPUT:
            - STRING: Is the text of the imported SQL query
        """
        return self.database_script


    # ================== LOG MANAGEMENT =================

    def LOG_Header(self):
        """
        INFORMATION: Write an standard header on the Log file located in the folder: ./LogFile/ 
        """
        self.log = open(self.log_file_path,'a+')
        current_time = time.strftime("%d/%b/%Y %H:%M:%S",time.localtime())
        self.InfoEvent(f"EXECUTING the webservice on  {current_time} ")

    def LOG_BeginLoops(self):
        """
        INFORMATION: Write an standard Line on the Log file located in the folder: ./LogFile/ for eatch time the instance is executing an folder
        """
        self.InfoEvent("\n#######################################################\nEXECUTINT THE ORDER:\n")

    def LOG_EndOfLoop(self):
        """
        INFORMATION: Write an standard Line on the Log file located in the folder: ./LogFile/ for eatch time the instance finich an order
        """
        self.InfoEvent("\n#######################################################\n")

    def LOG_Footer(self):
        """
        INFORMATION: Write an standard FOOTER on the Log file located in the folder: ./LogFile/ for eatch time the log file is finiched writing the basic information: ERRORS, WARNINGS, Total execiting time
        """
        self.InfoEvent("RESUME: NUMBER OF ERRORS: " + str(self.Errors)+ ", NUMBER OF WARNINGS: " + str(self.Warnings) + ", WAIT TIME: " + str(self.ElapsedInstanceTime()))
        self.log.close()
        #self.apiErrors.close()

    @argument_check(object,str,MAX_LOG_LINES=int)
    def ErrorLogEmail(self,STRING,MAX_LOG_LINES = 50):
        """
        INFORMATION: Automated protocol to send an email with the error information when there is an error that will be sended to the administrator
        INPUT:
            - STRING (STRING): Is the error masage that activate this error and this value will be included in the SUBJECT of the email.
            - MAX_LOG_LINES (OPTIONAL:INTEGER): Are the count of lines of the log that will be included inthe boduy of the email
        OUTPUT (BOOLEAN):
            - STATUS: NO ERROR => True
            - STATUS: ERROR => False
        """
        try:
            self.log.close()
            log_file = open(self.log_file_path,'r')
            body_string = f"ERROR REGISTERED IN LOG FILE: {self.log_file_path}\n\n"
            body_string += "...\n" + ' '.join(deque(log_file, MAX_LOG_LINES))
            actual_timestamp = time.strftime("%d %b %Y %H:%M:%S",time.localtime())
            self.SendMail(f"{actual_timestamp}: {STRING}",body_string,SYNCHRONE=False)
            self.log = open(self.log_file_path,'a+')
            return True
        except Exception as exc:
            self.log = open(self.log_file_path,'a+')
            self.ErrorEvent(f"\tERROR: Problems sending email: {exc}",SEND_EMAIL = False)
            return False

    @argument_check(object,str,SEND_EMAIL=bool)
    def ErrorEvent(self,STRING,SEND_EMAIL = True):
        """
        INFORMATION: Write an standard Line (ARGUMENT: string) on the log file (self.log) located in the folder: ./LogFile/ and increment the totL errors by 1. 
                     There is also an option to send a email with this error to the administrator defining the BOOLEAN argument: SEND_EMAIL
        """
        self.log.write(str(STRING)+"\n")
        print(str(STRING))
        self.Errors+=1
        if SEND_EMAIL:
            self.ErrorLogEmail(STRING)

    @argument_check(object,str,SEND_EMAIL=bool)
    def WarningEvent(self,STRING,SEND_EMAIL = False):
        """
        INFORMATION: Write an standard Line (ARGUMENT: string) on the log file (self.log) located in the folder: ./LogFile/ and increment the total warnings by 1
        """
        self.log.write(str(STRING)+"\n")
        print(str(STRING))
        self.Warnings+=1
        if SEND_EMAIL:
            self.ErrorLogEmail(STRING)
    
    @argument_check(object,str,SEND_EMAIL=bool)
    def InfoEvent(self,STRING,SEND_EMAIL = False):
        """
        INFORMATION: Write an standard Line (ARGUMENT: string) on the log file (self.log) located in the folder: ./LogFile/ and increment the total warnings by 1
        """
        self.log.write(str(STRING)+"\n")
        print(str(STRING))
        if SEND_EMAIL:
            self.ErrorLogEmail(STRING)

    #===== DATE / TIME MANAGEMENT

    @argument_check(object,int)
    def HourCalculation(self,MINUTES):
        """
        INFORMATION: Function that return an subset of hours and minutes for an given total of minutes (ARGUMENT: MINUTES)
        INPUT:
            - MINUTES (INTEGER): Total of minutes that must be convert to a subser of hours and minutes
        OUTPUT: (Tuple with lenght 2)
            - hour (INTEGER)
            - minute (INTEGER)
        """
        hour=MINUTES//60
        minute=MINUTES%60
        return hour, minute

    @argument_check(object,int,int)
    def TimeString(self,HOUR,MINUTE):
        """
        INFORMATION: Function that return an standard timestring '<HOUR>:<MINUTE>'
        INPUT:
            - HOUR (INTEGER)
            - MINUTES (INTEGER)
        OUTPUT: 
            - STRING: standard time string '<HOUR>:<MINUTE>'
        """
        hour_str=("0"+str(HOUR)) if HOUR < 10 else str(HOUR)
        minute_str=("0"+str(MINUTE)) if MINUTE < 10 else str(MINUTE)
        return str(hour_str)+":"+str(minute_str)

    def GetActualDateTime_Tuple(self):
        """
        INFORMATION: Function that return the current Time-Tuple
        INPUT: None
        OUTPUT: 
            - TIMETUPLE: (Object of  "datetime library)
        """
        return datetime.now().timetuple()

    @argument_check(object,tuple)
    def GetDayOfYear(self,DATETIME_TUPLE):
        """
        INFORMATION: Function that return the day of the year for an given TimeTuple
        INPUT:
            - DATETIME_TUPLE: A given TimeTuple
        OUTPUT: 
            - INTEGER: Day of the year
        """
        return DATETIME_TUPLE.tm_yday

    def GetActualDatOfYear(self):
        """
        INFORMATION: Function that return the current day of the year
        INPUT: None
            
        OUTPUT: 
            - INTEGER: Day of the year
        """
        return self.GetDayOfYear(self.GetActualDateTime_Tuple())

    @argument_check(object,int,int)
    def GetMinutesOfDay(self,HOUR,MINUTE):
        """
        INFORMATION: Function that return a total min¡utes for the given arguments: HOUR, MINUTE
        INPUT:
            - HOUR: INTEGER
            - MINUTE: INTEGER  
        OUTPUT: 
            - INTEGER: Total minutes for the given argument (HOUR, MINUTE)
        """
        return 60*HOUR + MINUTE 

    @argument_check(object,np.ndarray)
    def SumOfMinutes(self, LIST):
        """
        INFORMATION: Function that return a total minutes for the given arguments array list (LIST)
        INPUT:
            - LIST: ARRAY of integers 0 OR 1
        OUTPUT: 
            - INTEGER: Total Minutes for an given Array (Sum of al the active minutes (1) of a day)
        """
        return np.int16(np.sum(LIST)).item()

    @argument_check(object,int,np.ndarray,list)
    def IntervalReplacer(self, VALUE,LIST,INTERVALS):
        """
        INFORMATION: Function that replace on the list of intervals (INTERVALS) of a array list (LIST) with the value (VALUE)
        INPUT:
            - VALUE: INTEGER
            - LIST: ARRAY of integers 0 OR 1
            - INTERVALS: List of list with lenght 1
        OUTPUT: 
            - ARRAY: The new redefined array
        """
        for interval in INTERVALS:
            LIST[interval[0]:interval[1]]=VALUE
        return LIST

    @argument_check(object,datetime)
    def CreateDateDict(self,DATETIME):
        """
        INFORMATION: Function that return a date dict defined by: {"y": <YEAR>,"m" :<MONTH>,"d":<DAY>}, By a given DATETIME
        INPUT:
            - DATETIME: datetime instance
        OUTPUT: 
            - DICT: defined by: {"y": <YEAR>,"m" :<MONTH>,"d":<DAY>}
        """
        return {"y": DATETIME.year,"m" :DATETIME.month,"d":DATETIME.day}


    #===== APLICATION TIME MANAGENMENT ======

    def ElapsedInstanceTime(self):
        """
        INFORMATION: Function that return the elapsed time when the instance is active.
        INPUT:None
        OUTPUT: 
            - FLOAT: Total of elapsed seconds whenthe instance was ectivates when you execute this function
        """
        return time.time() - self.epochtime

    #====== EXIT OF INSTANCE ===============

    def EXIT(self):
        """
        INFORMATION: Function that is activated when you finich the instance process writing the footer of the Log file.
        """
        self.LOG_Footer()

    #====== INPUT VALIDATION CHECK ===========

    @argument_check(object,str)
    def ValidDateQ(self,DATE_TEXT):
        """
        INFORMATION: Validating proces if the 'DATE_TEXT' argument has an good date format as : self.datestring_format
        INPUT:
            - DATE_TEXT (STRING): datestring that is must parsed 
        OUTPUT:
            - STATUS: NO ERROR
                - BOOLEAN => True, Validating process passed withou errors
            - STATUS: ERROR
                - BOOLEAN => False, Wrong date format
        """
        try:
            datetime.strptime(DATE_TEXT, self.datestring_format)
            return True
        except Exception as inst:
            self.ErrorEvent(f"\tERROR: Argumnt '{DATE_TEXT}' has wrong datetime format (YYYY-MM-DD): {inst}")
            return False
    
    @argument_check(object,str)
    def ValidListQ(self,LIST_STRING):
        """
        INFORMATION: Validating process that parse the argument "LIST_STRING" as an valid List with only Integers as arguments
        INPUT: 
            - LIST_STRING (STRING):  STRING That is validate as an list odf integers or as an empty list.
        OUTPUT:
            - STATUS: NO ERROR
                - BOOLEAN => True, Validating process passed withou errors
            - STATUS: ERROR
                - BOOLEAN => False, Wrong LIST format
        """
        try:
            list_to_validate=json.loads(LIST_STRING)
            #print(list_to_validate)
            if len(list_to_validate)==0:
                return True
            else:
                for value in list_to_validate:
                    if isinstance(value,int):
                        continue
                    else:
                        self.ErrorEvent(f"\tERROR: Not all the argument of the list ({LIST_STRING}) are integers")
                        return False
                return True
        except Exception as inst:
            self.ErrorEvent(f"\tERROR: Argumnt '{LIST_STRING}' has wrong format to parse to list: {inst}")
            return False 

# =============== EXECUTE OF THE CODE ===============

if __name__ == "__main__":

    pass