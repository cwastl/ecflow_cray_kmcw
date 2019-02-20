#!/usr/bin/env python2.7
#
#CREATE C-LAEF SUITE DEFINITION FILE
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
members = [1]

# coupling frequency
couplf = 6

# use GL Tool yes/no, if no - 901 is used
gl = True

# assimilation switches
assimi = True   #assimilation yes/no
assimc = 6      #assimilation cycle in hours
eda = True      #ensemble data assimilation
seda = True     #surface eda

# use EnJK method of Endy yes/no
enjk = False

# use stochastic physics model error representation yes/no
stophy = True

# SBU account, cluster and user name, logport
account = "atlaef";
host    = "cca";
user    = "kmcw";
logport = 36652;

# main runs time schedule
timing = {
  '00' : '13:09',
  '06' : '08:30',
  '12' : '14:30',
  '18' : '20:30',
}

# debug mode (1 - yes, 0 - no)
debug = 0;

# user date (default is system date)
user_date = {
  'dd'  : '12',
  'mm'  : '01',
  'yyyy': '2017'
}

###########################################
#####define Families and Tasks#############
###########################################

def family_lbc() :

    # Family LBC
    return Family("lbc",

       Edit(
          GL=gl),

       # Family MEMBER
       [

         Family("MEM_{:02d}".format(mem),

          # Task getlbc
          [
             Task("getlbc",
                Trigger(":GL == 0"),
                Edit(
                   NP=1,
                   CLASS='ns',
                   KOPPLUNG=couplf,
                   MEMBER="{:02d}".format(mem),
                   NAME="getlbc{:02d}".format(mem),
                   WALLT="01",
                ),
                Label("run", ""),
                Label("status", ""),
                Label("error", "ok"),
             )
          ],

          # Task 901
          [
             Task("901",
                Trigger(":GL == 0 and getlbc == complete"),
                Edit(
                   NP=1,
                   CLASS='ns',
                   KOPPLUNG=couplf,
                   MEMBER="{:02d}".format(mem),
                   NAME="901{:02d}".format(mem),
                   WALLT="03",
                ),
                Label("run", ""),
                Label("status", ""),
                Label("error", "ok"),
             )
          ],

          # Task getlbc_gl
          [
             Task("getlbc_gl",
                Trigger(":GL == 1"),
                Edit(
                   NP=1,
                   CLASS='ns',
                   KOPPLUNG=couplf,
                   MEMBER="{:02d}".format(mem),
                   NAME="getlbc_gl{:02d}".format(mem),
                   WALLT="01",
                ),
                Label("run", ""),
                Label("status", ""),
                Label("error", "ok"),
             )
          ],

          # Task GL
          [
             Task("gl",
                Trigger(":GL == 1 and getlbc_gl == complete"),
                Edit(
                   MEMBER="{:02d}".format(mem),
                   NP=1,
                   CLASS='nf',
                   KOPPLUNG=couplf,
                   NAME="gl{:02d}".format(mem),
                   WALLT="03"               #walltime in hours
                ),
                Label("run", ""),
                Label("status", ""),
                Label("error", "ok")
             )
          ],

        ) for mem in members

      ]
    )

def family_obs() :

    # Family OBS
    return Family("obs",

       Edit(ASSIM=assimi),

       # Task assim/getobs
       [
          Task("getobs",
             Trigger(":ASSIM == 1"),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="getobs",
                WALLT="01"              #walltime in hours
             ),
             Label("run", ""),
             Label("status", ""),
             Label("error", "ok")
          )
       ],

       # Task assim/bator
       [
          Task("bator",
             Trigger(":ASSIM == 1 and getobs == complete"),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="bator",
                WALLT="01"               #walltime in hours
             ),
             Label("run", ""),
             Label("status", ""),
             Label("error", "ok")
          )
       ],

       # Task assim/bator3D
       [
          Task("bator3D",
             Trigger(":ASSIM == 1 and getobs == complete"),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="bator3D",
                WALLT="01"               #walltime in hours
             ),
             Label("run", ""),
             Label("status", ""),
             Label("error", "ok")
          )
       ],
    )

def family_main():

   # Family MAIN
   return Family("main",

      Edit(
         ASSIM=assimi,
         GL=gl),

      # Family MEMBER
      [
         Family("MEM_{:02d}".format(mem),
           
            # Task 927atm
            [
               Task("927",
                  Trigger("../../lbc/MEM_{:02d}/gl == complete or ../../lbc/MEM_{:02d}/901 == complete".format(mem,mem)),
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=16,
                     CLASS='np',
                     KOPPLUNG=couplf,
                     NAME="927{:02d}".format(mem),
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
#              Task("pgd",
#                  Trigger("../../lbc/MEM_{:02d}/gl == complete or ../../lbc/MEM_{:02d}/901 == complete".format(mem,mem)),
#                 Edit(
##                    ECF_DUMMY_TASK="", # TEMPORARY DUMMY
#                    MEMBER="{:02d}".format(mem),
#                    NP=1,
#                    CLASS='np',
#                    NAME="pgd{:02d}".format(mem),
#                    WALLT="01"                #walltime in hours
#                 ),
#                 Label("run", ""),
#                 Label("status", ""),
#                 Label("error", "ok")
#               )
#            ],

            # Task 927/surf
            [
               Task("927surf",
                  Trigger("../../lbc/MEM_{:02d}/gl == complete or ../../lbc/MEM_{:02d}/901 == complete".format(mem,mem)),
#                  Trigger("pgd == complete"),
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     NAME="927surf{:02d}".format(mem),
                     WALLT="01"                #walltime in hours
                  ),
                  Label("run", ""),
                  Label("status", ""),
                  Label("error", "ok")
               )
            ],

            # Task assim/sstex
            [
               Task("sstex",
                  Trigger(":ASSIM == 1 and 927 == complete"),
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ns',
                     ASSIMC=assimc,
                     NAME="sstex{:02d}".format(mem),
                     WALLT="01"                #walltime in hours
                  ),
                  Label("run", ""),
                  Label("status", ""),
                  Label("error", "ok")
               )
            ],

            # Task assim/addsurf
            [
               Task("addsurf",
                  Trigger(":ASSIM == 1 and sstex == complete"),
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ns',
                     ASSIMC=assimc,
                     NAME="addsurf{:02d}".format(mem),
                     WALLT="01"                #walltime in hours
                  ),
                  Label("run", ""),
                  Label("status", ""),
                  Label("error", "ok")
               )
            ],

            # Task assim/screening 3D
            [
               Task("screen",
                  Trigger(":ASSIM == 1 and addsurf == complete and ../../obs/bator3D == complete"),
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=12,
                     CLASS='np',
                     ASSIMC=assimc,
                     EDA=eda,
                     NAME="screen{:02d}".format(mem),
                     WALLT="03"                #walltime in hours
                  ),
                  Label("run", ""),
                  Label("status", ""),
                  Label("error", "ok")
               )
            ],

            # Task assim/screening surface
            [
               Task("screensurf",
                  Trigger(":ASSIM == 1 and addsurf == complete and ../../obs/bator == complete"),
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     ASSIMC=assimc,
                     NAME="screensurf{:02d}".format(mem),
                     WALLT="03"                #walltime in hours
                  ),
                  Label("run", ""),
                  Label("status", ""),
                  Label("error", "ok")
               )
            ],

            # Task assim/canari
            [
               Task("canari",
                  Trigger(":ASSIM == 1 and screensurf == complete"),
                  Complete(":ASSIM == 0"),
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     ASSIMC=assimc,
                     SEDA=seda,
                     NAME="canari{:02d}".format(mem),
                     WALLT="03"                #walltime in hours
                  ),
                  Label("run", ""),
                  Label("status", ""),
                  Label("error", "ok")
               )
            ],

            # Task assim/minimization
            [
               Task("minim",
                  Trigger(":ASSIM == 1 and screen == complete"),
                  Complete(":ASSIM == 0"),
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=12,
                     CLASS='np',
                     ASSIMC=assimc,
                     ENSJK=enjk,
                     NAME="minim{:02d}".format(mem),
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
                  Trigger("927 == complete and 927surf == complete and minim == complete and canari == complete"),
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=480,
                     CLASS='np',
                     KOPPLUNG=couplf,
                     ASSIM=assimi,
                     ASSIMC=assimc,
                     STOCH=stophy,
                     NAME="001{:02d}".format(mem),
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
                  Trigger("001  == complete"),
                  Edit(
#                     ECF_DUMMY_TASK="", # TEMPORARY DUMMY
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     NAME="progrid{:02d}".format(mem),
                     WALLT="01"                #walltime in hours
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
                CNF_DEBUG=debug,

                # Running jobs remotely on HPCF
                ECF_OUT = '/scratch/ms/at/kmcw/ECF', # jobs output dir on remote host
                ECF_LOGHOST=host,                     # remote log host
                ECF_LOGPORT=logport,                  # remote log port

                # Submit job (remotely)
                ECF_JOB_CMD="{} {} {} %ECF_JOB% %ECF_JOBOUT%".format(schedule, user, host),
             ),

#             # Main Runs per day (00, 06, 12, 18)
#             Family("RUN_00",
#                Edit( LAUF='00', DATUM=user_date['yyyy']+user_date['mm']+user_date['dd'],
#                VORHI=0, LEAD=6),
#
#                # add suite Families and Tasks
#                family_lbc(),
#                family_obs(),
#                family_main(),
#             ),

             Family("RUN_06",
                Edit( LAUF='06', DATUM=user_date['yyyy']+user_date['mm']+user_date['dd'],
                VORHI=6, LEAD=6),

                # add suite Families and Tasks
                family_lbc(),
                family_obs(),
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

