#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VisualPresencia_Process.py: Library that hay the processes of VisualPresencia.
"""
__author__          = "Robert Rijnbeek"
__version__         = "1.0.1"
__maintainer__      = "Robert Rijnbeek"
__email__           = "robert270384@gmail.com"
__status__          = "Development"

__creation_date__   = '07/02/2022'
__last_update__     = '09/02/2022'

# =============== IMPORTS ===============

#IMPORT OF THE Dinsa_API Class 
from .Main_Api import Main_API

# =============== CODE ===============

class Hello_World(Main_API):
    """
    DESCRIPTION: Class Method That is subclass of 'Process' class and is superclass of 'Main_API' And is used for the process that write an python script(Codec/code.py) that include all the custom furmulation process registered in the database and is used in the 'VisualPresencia _Process.py' 
    INPUT: None
    OUTPUT: None
    """
    def __init__(self):
        """
        DESCRIPTTION: Is the initialization function of the Class 'Formula_Parser' that include the instance variables and methods of 'Main_API' and his own variables: 'self.codec_string' and 'self.variable_list_for_each_company'
        INPUT: None
        OUTPUT: None
        """
        #INCLUDE THE Dinsa_API FUNCTIONALITY IN THE Formula_Parser CLASS
        Main_API.__init__(self)
        # DEFINING OF CLASS VARIABLES
        self.message = ""


# ========= VALIDATION OF INPUTDATA =========

    def Valid_Argument_Q1(self):
        """
        INFORMATION: Validating function that parse all the argumenst from the "self.argument_object" and it the validating process pased satisfactully. It will redefine also the "self.argument_object" with valid parsed Python values (Datetime, list,...)
        INPUT: None
        OUTPUT:
            - STATUS: NO ERROR
                - BOOLEAN => True, Validating process passed withou errors
            - STATUS: ERROR
                - BOOLEAN => False
        """
        try:
            self.InfoEvent("\tINFO: VALIDATING OF THE ARGUMENT FROM URL.")
            parsed_argumen_object = {}
            for key, value in self.argument_object.items(): 

                if ( key == "NAME" ) and ( isinstance(value, str) ):
                    #parsed_argumen_object[key] = json.loads(value)
                    parsed_argumen_object[key] = value
                    self.InfoEvent("\tINFO: The Argument object'" + str(self.argument_object)+ "' has past the validating process")
                    self.argument_object = parsed_argumen_object
                    return True
                else:
                    self.ErrorEvent("\tERROR: Wrong input value")
                    return False
        except Exception as inst:
            self.ErrorEvent(f"\tERROR: UNESPECTED ERROR: {inst}")
            return False

# ========= Build Message =========

    def BuildMessage(self):
        try:
            argument = self.argument_object['NAME'];
            if isinstance(self.argument_object['NAME'],str):
                self.InfoEvent(f"\tINFO: The message is build with the argurment: {argument}")
                self.message = f"Hello World {argument}";
                self.request_status = True
                self.request = {"message": self.message }
                return True
            else:
                self.ErrorEvent("\tERROR: Problems building the message")
                return False
        except Exception as inst:
            self.ErrorEvent(f"\tERROR: UNESPECTED ERROR: {inst}")
            return False


#================ PROCESS =====================

    def HelloWorldProcess(self):
        if self.Valid_Argument_Q1():
            if self.BuildMessage():
                return True
        return False


if __name__ == "__main__":
    pass