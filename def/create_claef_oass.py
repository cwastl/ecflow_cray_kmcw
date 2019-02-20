#!/usr/bin/env python2.7
#
#CREATE C-LAEF SUITE (without assimilation) DEFINITION FILE
#
#OUTPUT: claef.def and *.job0 - task files
#
#CREATED: 2019-01-14
#
#AUTHOR: C. Wastl
###########################################################

#load modules
import os
from ecflow import *

# ecFlow home and include paths
home = os.path.join(os.getenv("HOME"),"ecf");
incl = os.path.join(os.getenv("HOME"),"ecf/include");

# to submit jobs remotely
schedule = "/usr/local/apps/schedule/1.4/bin/schedule";

################################
### top level suite settings ###
################################

#ensemble members
#members = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
members = [1,2,3]

# max forecast length
max_range = 30;

# output file frequency
step_range = 1;

# coupling frequency
couplf = 3

# assimilation yes/no
assimi = False

# assimilation cycle in hours
assimc = 6

# input file (CC=canari assim cycle)
file_src = "CC";

# number of CPUs pre task (canari, blending, laeff)
np = 288;

# SBU account, cluster and user name, logport
account = "atlaef";
host    = "cca";
user    = "kmcw";
logport = 36652;

# main runs time schedule
timing = {
  '00' : '02:30',
  '06' : '08:30',
  '12' : '14:30',
  '18' : '20:30',
}

# debug mode (1 - yes, 0 - no)
debug = 0;

# user date (default is system date)
user_date = {
  'dd'  : '31',
  'mm'  : '12',
  'yyyy': '2016'
}

###########################################
#####define Families and Tasks#############
###########################################

def family_main():

   # Family MAIN
   return Family("main",

      # Family MEMBER
      [
         Family("MEM_{:02d}".format(mem),
           
            # Task GL
            [
               Task("gl",
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='nf',
                     KOPPLUNG=couplf,
                     NAME="gl_{:02d}".format(mem),
                     WALLT="03"               #walltime in hours
                  ),
                  Label("run", ""),
                  Label("status", ""),
                  Label("error", "ok")
               )
            ],

            # Task 927atm
            [
               Task("927",
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=16,
                     CLASS='np',
                     KOPPLUNG=couplf,
                     NAME="927_{:02d}".format(mem),
                     ASSIM=assimi,
                     WALLT="03"                #walltime in hours
                  ),
                  Label("run", ""),
                  Label("status", ""),
                  Label("error", "ok")
               )
            ],

#            # Task 927/PGD
#            [
#               Task("pgd",
#                  Edit(
##                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
#                     MEMBER="{:02d}".format(mem),
#                     NP=1,
#                     CLASS='np',
#                     NAME="pgd_{:02d}".format(mem),
#                     WALLT="03"                #walltime in hours
#                  ),
#                  Label("run", ""),
#                  Label("status", ""),
#                  Label("error", "ok")
#               )
#            ],

            # Task 927/surf
            [
               Task("927surf",
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     NAME="927surf_{:02d}".format(mem),
                     WALLT="03"                #walltime in hours
                  ),
                  Label("run", ""),
                  Label("status", ""),
                  Label("error", "ok")
               )
            ],

            # Task 001
            [
               Task("001",
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=480,
                     CLASS='np',
                     KOPPLUNG=couplf,
                     ASSIM=assimi,
                     ASSIMC=assimc,
                     NAME="001_{:02d}".format(mem),
                     WALLT="06"                #walltime in hours
                  ),
                  Label("run", ""),
                  Label("status", ""),
                  Label("error", "ok")
               )
            ],

            # Task PROGRID
            [
               Task("progrid",
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     NAME="progrid_{:02d}".format(mem),
                     WALLT="03"                #walltime in hours
                  ),
                  Label("run", ""),
                  Label("status", ""),
                  Label("error", "ok")
               )
            ],

           ) for mem in members
         ]
       )

def date() :
    if user_date.keys() :
        print("=> date defined by user\n");
        return Edit(
                 DD=user_date['dd'],
                 MM=user_date['mm'],
                 YYYY=user_date['yyyy'],
               )

###########################
### create C-LAEF suite ###
###########################

print("\n=> creating suite definition\n");

# user date (if defined)
date()

defs = Defs().add(

          # Suite C-LAEF
          Suite("claef").add(

             Edit(

                # ecflow configuration
                ECF_MICRO='%',         # ecf micro-character
                ECF_EXTN='.ecf',        # ecf files extension
                ECF_HOME=home,         # ecf root path
                ECF_INCLUDE=incl,      # ecf include path

                # suite configuration variables
                ACCOUNT=account,
                MAX_RANGE=max_range,
                STEP_RANGE=step_range,
                CNF_INIT=file_src,
                CNF_FILE=file_src,
                CNF_DEBUG=debug,

                # Running jobs remotely on HPCF
                ECF_OUT = '/scratch/ms/at/kmcw/ECF', # jobs output dir on remote host
                ECF_LOGHOST=host,                     # remote log host
                ECF_LOGPORT=logport,                  # remote log port

                # Submit job (remotely)
                ECF_JOB_CMD="{} {} {} %ECF_JOB% %ECF_JOBOUT%".format(schedule, user, host),
             ),

             # Main Runs per day (00, 06, 12, 18)
#             Family("RUN_00", Time(timing['00']),
#                Edit( LAUF='00', DATUM=user_date['yyyy']+user_date['mm']+user_date['dd'],
#                VORHI=0, LEAD=24),
#
#                # add suite Families and Tasks
#                family_main(),
#             ),
#             Family("RUN_06", Time(timing['06']),
#                Edit( LAUF='06', DATUM=user_date['yyyy']+user_date['mm']+user_date['dd'],
#                VORHI=6, LEAD=6),
#
#                # add suite Families and Tasks
#                family_main(),
#             ),
#             Family("RUN_12", Time(timing['12']),
#                Edit( LAUF='12', DATUM=user_date['yyyy']+user_date['mm']+user_date['dd'],
#                VORHI=0, LEAD=24),
#
#                # add suite Families and Tasks
#                family_main(),
#             ),
             Family("RUN_18", Time(timing['18']),
                Edit( LAUF='18', DATUM=user_date['yyyy']+user_date['mm']+user_date['dd'],
                VORHI=6, LEAD=6),

                # add suite Families and Tasks
                family_main(),
             ),

           )
       )

###################################
### check and save C-LAEF suite ###
###################################

print("=> checking job creation: .ecf -> .job0");
print(defs.check_job_creation());
print("=> saving definition to file 'claef.def'\n");
defs.save_as_defs("claef.def");
exit(0);

