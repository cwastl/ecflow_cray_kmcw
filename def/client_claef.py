#!/usr/bin/env python2.7
#
# LOAD or RELOAD (if already exists) the C-LAEF suite
#
# C. Wastl, 2019-01-15
###################################################

import ecflow

try:
    ci = ecflow.Client()
    ci.sync_local()      # get the defs from the server, and place on ci
    defs = ci.get_defs() # retrieve the defs from ci

    if defs == None:
        print("\n=> no definition in server, loading def from disk")
        ci.load("claef.def")

        print "\n=> restarting the server (this starts job scheduling)"
        ci.restart_server()
    else:
        print("\n=> reading def from disk and replacing into the server")
        ci.replace("/claef", "claef.def")

    print "\n=> begin the suite named 'claef' (in suspend mode)"
    ci.begin_suite("claef")
    ci.suspend("/claef")  # so that we can resume manually in ecflow_ui

except RuntimeError as e:
    print "(!) Failed:",   e
