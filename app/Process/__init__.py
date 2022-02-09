#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__init__.py (Process): In this module is defined the 'Process' class that is used in the VisualWebService class instance
"""
__author__          = "Robert Rijnbeek"
__version__         = "1.0.1"
__maintainer__      = "Robert Rijnbeek"
__email__           = "robert270384@gmail.com"
__status__          = "Development"

__creation_date__   = '07/02/2022'
__last_update__     = '09/02/2022'


# IMPORT OF THE Formula_Parse CLASS 
from .hello_world import Hello_World

class Process( Hello_World ):
    """
    DESCRIPTION: Class Method That is subclass of 'Hello_World'. And is used ans generic method calller for the differents webservices
    INPUT: None
    OUTPUT: None
    """
    def __init__(self):
        """
        DESCRIPTTION: Is the initialization function of the Class 'Process' that include the instance variables and methods of 'Hello_World'
        INPUT: None
        OUTPUT: None
        """
        #INCLUDE THE Hello_World Class process
        Hello_World.__init__(self)

    def Process(self):
        """
        DESCRIPTION: Is the generic Method that calls link the generic methods processes with the differents Webservices
        INPUT:None
        OUTPUT: BOOLEAN
            STATUS: error => return False
            STATUS NO ERROR => return True
        """
        self.InfoEvent("\tINFO: SELECTING METHOD")
        if  self.method == "hello_world":
            self.InfoEvent("\tINFO: executing the 'hello world()'")
            return self.HelloWorldProcess()
        else:
            self.WarningEvent("\tWARNING: method '"+ str(self.method)+"' is not a valid method.")
            return False

# =============== EXECUTE OF THE TEST CODE ===============

if __name__ == "__main__":
    pass