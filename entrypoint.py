#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
entrypoint.py: This script execute the OpenWebservice() function that activate the flask webservice
"""
__author__          = "Robert Rijnbeek"
__version__         = "1.0.1"
__maintainer__      = "Robert Rijnbeek"
__email__           = "r.rijnbeek@dinsa.es"
__status__          = "Development"

__creation_date__   = '12/12/2019'
__last_update__     = '10/02/2020'

# =============== IMPORTS ==============

from app import OpenWebservice

# ==== ACTIVATION OF THE WEBSERVICE ====

OpenWebservice()