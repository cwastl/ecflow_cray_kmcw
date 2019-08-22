#!/usr/bin/env python3
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
import datetime

# get current date
now = datetime.datetime.now()

# ecFlow home and include paths
home = os.path.join(os.getenv("HOME"),"ecf");
incl = os.path.join(os.getenv("HOME"),"ecf/include");

# to submit jobs remotely
schedule = "/usr/local/apps/schedule/1.4/bin/schedule";

################################
### top level suite settings ###
################################

#suite name
suite_name = "claef"

#ensemble members
members = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
#members = [13]

# forecasting range
fcst = 48

# forecasting range control member
fcstctl = 48

# coupling frequency
couplf = 3

# use 15min output for precipitation
step15 = False

# use GL Tool yes/no, if no - 901 is used
gl = False

# assimilation switches
assimi = True   #assimilation yes/no
assimm = 3      #number of members without assimilation
assimc = 6      #assimilation cycle in hours
eda = True      #ensemble data assimilation
seda = True     #surface eda

# use EnJK method of Endy yes/no
enjk = True

# use stochastic physics model error representation yes/no
stophy = True

# SBU account, cluster and user name, logport
account = "atlaef";
schost  = "cca";
user    = "kmcw";
logport = 36652;

# main runs time schedule
timing = {
  'comp' : '23:00',
  'o00_1' : '0135',
  'o00_2' : '0155',
  'o06_1' : '0735',
  'o06_2' : '0755',
  'o12_1' : '1335',
  'o12_2' : '1355',
  'o18_1' : '1935',
  'o18_2' : '1955',
}

# debug mode (1 - yes, 0 - no)
debug = 0;

anzmem = len(members)

# date to start the suite
start_date = int(now.strftime('%Y%m%d'))
#start_date = 20190411
end_date = 20191231

###########################################
#####define Families and Tasks#############
###########################################

def family_dummy():

    # Family dummy
    return Family("dummy",

       # Task dummy1
       [
          Task("dummy1",
             Edit(
                NP=1,
                CLASS='ts',
                NAME="dummy1",
             ),
             Label("run", ""),
             Label("info", ""),
             Defstatus("suspended"),
          )
       ],
   )

def family_cleaning():

   return Task("cleaning",
             Trigger("dummy/dummy1 == complete"),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="cleaning",
                ANZMEMB=anzmem,
             ),
             Label("run", ""),
             Label("info", ""),

          )

def family_lbc():

    # Family LBC
    return Family("lbc",

       Edit(
          GL=gl),

       # Task getlbc
       [
          Task("getlbc",
             Trigger("../dummy/dummy1 == complete"),
             Event("a"),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="getlbc",
             ),
             Label("run", ""),
             Label("info", ""),
             Label("error", ""),
          )
       ],

       # Family MEMBER
       [

         Family("MEM_{:02d}".format(mem),

          # Task divlbc
          [
             Task("divlbc",
                Trigger(":GL == 0 and ../getlbc:a"),
                Complete(":GL == 1 or :MEMBER == 00 and ../../dummy/dummy1 == complete"),
                Event("b"),
                Edit(
                   NP=1,
                   CLASS='ns',
                   MEMBER="{:02d}".format(mem),
                   NAME="divlbc{:02d}".format(mem),
                ),
                Label("run", ""),
                Label("info", ""),
                Label("error", ""),
             )
          ],

          # Task 901
          [
             Task("901",
                Trigger(":GL == 0 and divlbc:b"),
                Complete(":GL == 1 or :MEMBER == 00 and ../../dummy/dummy1 == complete"),
                Event("c"),
                Edit(
                   NP=1,
                   CLASS='ns',
                   MEMBER="{:02d}".format(mem),
                   NAME="901_{:02d}".format(mem),
                ),
                Label("run", ""),
                Label("info", ""),
                Label("error", ""),
             )
          ],

          # Task getlbc_gl
          [
             Task("getlbc_gl",
                Trigger(":GL == 1 and ../../dummy/dummy1 == complete"),
                Complete(":GL == 0"),
                Edit(
                   NP=1,
                   CLASS='ns',
                   SUITENAME=suite_name,
                   MEMBER="{:02d}".format(mem),
                   NAME="getlbcgl{:02d}".format(mem),
                ),
                Label("run", ""),
                Label("info", ""),
             )
          ],

          # Task GL
          [
             Task("gl",
                Trigger(":GL == 1 and getlbc_gl == complete"),
                Complete(":GL == 0"),
                Edit(
                   MEMBER="{:02d}".format(mem),
                   NP=1,
                   CLASS='nf',
                   NAME="gl{:02d}".format(mem),
                ),
                Label("run", ""),
                Label("info", ""),
             )
          ],

        ) for mem in members

      ]
    )

def family_obs(startp1,startp2) :

    # Family OBS
    return Family("obs",

       Edit(ASSIM=assimi),

       # Task assim/getobs
       [
          Task("getobs",
             Trigger(":ASSIM == 1 and /claef:TIME > {} and /claef:TIME < {}".format(startp1,startp2)),
             Complete(":ASSIM == 0"),
             Meter("obsprog", -1, 3, 3),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="getobs",
             ),
             Label("run", ""),
             Label("info", ""),
          )
       ],

       # Task assim/bator
       [
          Task("bator",
             Trigger(":ASSIM == 1 and getobs == complete"),
             Complete(":ASSIM == 1 and getobs:obsprog == 0 or :ASSIM == 0"),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="bator",
             ),
             Label("run", ""),
             Label("info", ""),
             Label("error", "")
          )
       ],

       # Task assim/bator3D
       [
          Task("bator3D",
             Trigger(":ASSIM == 1 and getobs == complete"),
             Complete(":ASSIM == 1 and getobs:obsprog == 0 or :ASSIM == 0"),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="bator3D",
             ),
             Label("run", ""),
             Label("info", ""),
          )
       ],
    )

def family_main():

   # Family MAIN
   return Family("main",

      Edit(
         GL=gl,
         ASSIM=assimi,
         LEADT=fcst),

      # Family MEMBER
      [
         Family("MEM_{:02d}".format(mem),

            # Task 927atm
            [
               Task("927",
                  Trigger(":GL == 1 and ../../lbc/MEM_{:02d}/gl == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901 == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901:c".format(mem,mem,mem)),
                  Event("d"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=16,
                     CLASS='np',
                     NAME="927_{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

#            # Task 927/PGD
#            [
#              Task("pgd",
#                 Trigger(":GL == 1 and ../../lbc/MEM_{:02d}/gl == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901 == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901:c".format(mem,mem,mem)),
#                 Edit(
#                    MEMBER="{:02d}".format(mem),
#                    NP=1,
#                    CLASS='np',
#                    NAME="pgd{:02d}".format(mem),
#                 ),
#                 Label("run", ""),
#                 Label("info", ""),
#               )
#            ],

            # Task 927/surf
            [
               Task("927surf",
                  Trigger(":GL == 1 and ../../lbc/MEM_{:02d}/gl == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901 == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901:c".format(mem,mem,mem)),
#                  Trigger("pgd == complete"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     NAME="927surf{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", ""),
               )
            ],

            # Task assim/sstex
            [
               Task("sstex",
                  Trigger(":ASSIM == 1 and ../MEM_{:02d}/927:d".format(mem)),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ns',
                     NAME="sstex{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task assim/addsurf
            [
               Task("addsurf",
                  Trigger(":ASSIM == 1 and sstex == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ns',
                     NAME="addsurf{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task assim/screening 3D
            [
               Task("screen",
                  Trigger(":ASSIM == 1 and addsurf == complete and ../../obs/bator3D == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=12,
                     CLASS='np',
                     EDA=eda,
                     NAME="screen{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task assim/screening surface
            [
               Task("screensurf",
                  Trigger(":ASSIM == 1 and addsurf == complete and ../../obs/bator == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     NAME="screensurf{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task assim/canari
            [
               Task("canari",
                  Trigger(":ASSIM == 1 and screensurf == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     SEDA=seda,
                     NAME="canari{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task assim/minimization
            [
               Task("minim",
                  Trigger(":ASSIM == 1 and screen == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=12,
                     CLASS='np',
                     ASSIMM=assimm,
                     ENSJK=enjk,
                     NAME="minim{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task 001
            [
               Task("001",
                  Trigger("927 == complete and 927surf == complete and minim == complete and canari == complete"),
                  Event("e"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=360,
                     CLASS='np',
                     STOCH=stophy,
                     STEPS15=step15,
                     NAME="001_{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task PROGRID
            [
               Task("progrid",
                  Trigger("../MEM_{:02d}/001:e".format(mem)),
                  Complete(":LEAD < :LEADT"),
                  Event("f"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     STEPS15=step15,
                     NAME="progrid{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task ADDGRIB
            [
               Task("addgrib",
                  Trigger("../MEM_{:02d}/progrid:f".format(mem)),
                  Complete(":LEAD < :LEADT"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     STEPS15=step15,
                     NAME="addgrib{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", ""),
               )
            ],

           ) for mem in members
         ]
       )

###########################
### create C-LAEF suite ###
###########################

print("\n=> creating suite definition\n");

defs = Defs().add(

          # Suite C-LAEF
          Suite(suite_name).add(

             RepeatDate("DATUM",start_date,end_date),

             Edit(
                # ecflow configuration
                ECF_MICRO='%',         # ecf micro-character
                ECF_EXTN='.ecf',        # ecf files extension
                ECF_HOME=home,         # ecf root path
                ECF_INCLUDE=incl,      # ecf include path
                ECF_TRIES=1,           # number of reruns if task aborts

                # suite configuration variables
                SCHOST=schost,
                USER=user,
                ACCOUNT=account,
                CNF_DEBUG=debug,

                # suite variables
                KOPPLUNG=couplf,
                ASSIMC=assimc,
 
                # Running jobs remotely on HPCF
                ECF_OUT = '/scratch/ms/at/' + user + '/ECF', # jobs output dir on remote host
                ECF_LOGHOST='%SCHOST%-log',                     # remote log host
                ECF_LOGPORT=logport,                  # remote log port

                # Submit job (remotely)
                ECF_JOB_CMD="{} {} %SCHOST% %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
             ),

             # Task complete if something went wrong on the previous day
             Task("complete", Time(timing['comp']),
                Edit( NAME="complete", CLASS="ns", NP=1, SUITENAME=suite_name ),
                Label("run", ""),
                Label("info", ""),
             ),
             # Main Runs per day (00, 06, 12, 18)
             Family("RUN_00",
                Edit( LAUF='00', VORHI=6, LEAD=fcst, LEADCTL=fcstctl ),

                # add suite Families and Tasks
                family_dummy(),
                family_cleaning(),
                family_lbc(),
                family_obs(timing['o00_1'],timing['o00_2']),
                family_main(),
             ),

             Family("RUN_06",
                Edit( LAUF='06',VORHI=6, LEAD=assimc, LEADCTL=assimc ),

                # add suite Families and Tasks
                family_dummy(),
                family_cleaning(),
                family_lbc(),
                family_obs(timing['o06_1'],timing['o06_2']),
                family_main(),
             ),

             Family("RUN_12",
                Edit( LAUF='12',VORHI=6, LEAD=fcst, LEADCTL=fcst ),

                # add suite Families and Tasks
                family_dummy(),
                family_cleaning(),
                family_lbc(),
                family_obs(timing['o12_1'],timing['o12_2']),
                family_main(),
             ),

             Family("RUN_18",
                Edit( LAUF='18',VORHI=6, LEAD=assimc, LEADCTL=assimc ),

                # add suite Families and Tasks
                family_dummy(),
                family_cleaning(),
                family_lbc(),
                family_obs(timing['o18_1'],timing['o18_2']),
                family_main(),
             ),     
          )
       )

###################################
### check and save C-LAEF suite ###
###################################

print("=> checking job creation: .ecf -> .job0");
print(defs.check_job_creation());
print("=> saving definition to file " + suite_name + ".def\n");
defs.save_as_defs(suite_name + ".def");
exit(0);

