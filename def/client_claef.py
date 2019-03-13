#!/usr/bin/env python2.7
#
# LOAD or RELOAD (if already exists) the C-LAEF suite
#
# C. Wastl, 2019-01-15
###################################################

import ecflow

try:
    ci = ecflow.Client()
    ci.suspend("/claef")  # so that we can resume manually in ecflow_ui
    ci.replace("/claef", "claef.def")

except RuntimeError as e:
    print "(!) Failed:",   e
