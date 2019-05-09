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
suite_name = "claef_2"

#ensemble members
members = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
#members = [13]

# forecasting range
fcst = 48

# forecasting range control member
fcstctl = 12

# coupling frequency
couplf = 6

# use 15min output for precipitation
step15 = True 

# use GL Tool yes/no, if no - 901 is used
gl = True

# assimilation switches
assimi = True   #assimilation yes/no
assimc = 6      #assimilation cycle in hours
eda = True      #ensemble data assimilation
seda = True     #surface eda

# use EnJK method of Endy yes/no
enjk = True

# use stochastic physics model error representation yes/no
stophy = True

# SBU account, cluster and user name, logport
account = "atlaef";
host    = "cca";
user    = "kmcw";
logport = 36652;

# debug mode (1 - yes, 0 - no)
debug = 0;

anzmem = len(members)

# user date (default is system date)
start_date = 20160702
end_date = 20160703

###########################################
#####define Families and Tasks#############
###########################################

def family_lbc():

    # Family LBC
    return Family("lbc",

       Edit(
          GL=gl),

       # Task getlbc
       [
          Task("getlbc",
             Event("a"),
             Edit(
                NP=1,
                CLASS='ns',
                KOPPLUNG=couplf,
                NAME="getlbc",
                WALLT="02",
                USER=user
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
                Complete(":GL == 1 or :MEMBER == 00"),
                Event("b"),
                Edit(
                   NP=1,
                   CLASS='ns',
                   KOPPLUNG=couplf,
                   MEMBER="{:02d}".format(mem),
                   NAME="divlbc{:02d}".format(mem),
                   WALLT="02",
                   USER=user
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
                Complete(":GL == 1 or :MEMBER == 00"),
                Edit(
                   NP=1,
                   CLASS='ns',
                   KOPPLUNG=couplf,
                   MEMBER="{:02d}".format(mem),
                   NAME="901_{:02d}".format(mem),
                   WALLT="03",
                   USER=user
                ),
                Label("run", ""),
                Label("info", ""),
                Label("error", ""),
             )
          ],

          # Task getlbc_gl
          [
             Task("getlbc_gl",
                Trigger(":GL == 1"),
                Complete(":GL == 0"),
                Edit(
                   NP=1,
                   CLASS='ns',
                   KOPPLUNG=couplf,
                   SUITENAME=suite_name,
                   MEMBER="{:02d}".format(mem),
                   NAME="getlbcgl{:02d}".format(mem),
                   WALLT="01",
                   USER=user
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
                   KOPPLUNG=couplf,
                   NAME="gl{:02d}".format(mem),
                   WALLT="03",
                   USER=user
                ),
                Label("run", ""),
                Label("info", ""),
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
             Complete(":ASSIM == 0"),
             Meter("obsprog", -1, 3, 3),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="getobs",
                WALLT="01",
                USER=user
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
                WALLT="01",
                USER=user
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
                WALLT="01",
                USER=user
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
         ASSIM=assimi,
         GL=gl,
         LEADT=fcst),

      # Family MEMBER
      [
         Family("MEM_{:02d}".format(mem),
           
            # Task 927atm
            [
               Task("927",
                  Trigger(":GL == 1 and ../../lbc/MEM_{:02d}/gl == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901 == complete".format(mem,mem)),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=16,
                     CLASS='np',
                     KOPPLUNG=couplf,
                     NAME="927_{:02d}".format(mem),
                     WALLT="03",
                     USER=user
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

#            # Task 927/PGD
#            [
#              Task("pgd",
#                 Trigger(":GL == 1 and ../../lbc/MEM_{:02d}/gl == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901 == complete".format(mem,mem)),
#                 Edit(
#                    MEMBER="{:02d}".format(mem),
#                    NP=1,
#                    CLASS='np',
#                    NAME="pgd{:02d}".format(mem),
#                    WALLT="01",
#                    USER=user
#                 ),
#                 Label("run", ""),
#                 Label("info", ""),
#               )
#            ],

            # Task 927/surf
            [
               Task("927surf",
                  Trigger(":GL == 1 and ../../lbc/MEM_{:02d}/gl == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901 == complete".format(mem,mem)),
#                  Trigger("pgd == complete"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     NAME="927surf{:02d}".format(mem),
                     WALLT="01",
                     USER=user
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task assim/sstex
            [
               Task("sstex",
                  Trigger(":ASSIM == 1 and 927 == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ns',
                     ASSIMC=assimc,
                     NAME="sstex{:02d}".format(mem),
                     WALLT="01",
                     USER=user
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
                     ASSIMC=assimc,
                     NAME="addsurf{:02d}".format(mem),
                     WALLT="01",
                     USER=user
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
                     ASSIMC=assimc,
                     EDA=eda,
                     NAME="screen{:02d}".format(mem),
                     WALLT="03",
                     USER=user
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
                     ASSIMC=assimc,
                     NAME="screensurf{:02d}".format(mem),
                     WALLT="03",
                     USER=user
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
                     ASSIMC=assimc,
                     SEDA=seda,
                     NAME="canari{:02d}".format(mem),
                     WALLT="03",
                     USER=user
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
                     ASSIMC=assimc,
                     ENSJK=enjk,
                     NAME="minim{:02d}".format(mem),
                     WALLT="03",
                     USER=user
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task 001
            [
               Task("001",
                  Trigger("927 == complete and 927surf == complete and minim == complete and canari == complete"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=360,
                     CLASS='np',
                     KOPPLUNG=couplf,
                     ASSIMC=assimc,
                     STOCH=stophy,
                     STEPS15=step15,
                     NAME="001_{:02d}".format(mem),
                     WALLT="06",
                     USER=user
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task PROGRID
            [
               Task("progrid",
                  Trigger("001 == complete"),
                  Complete(":LEAD < :LEADT"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     STEPS15=step15,
                     NAME="progrid{:02d}".format(mem),
                     WALLT="01",
                     USER=user
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task ADDGRIB
            [
               Task("addgrib",
                  Trigger("progrid == complete"),
                  Complete(":LEAD < :LEADT"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     STEPS15=step15,
                     NAME="addgrib{:02d}".format(mem),
                     WALLT="01",
                     USER=user
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
                ACCOUNT=account,
                CNF_DEBUG=debug,

                # Running jobs remotely on HPCF
                ECF_OUT = '/scratch/ms/at/' + user + '/ECF', # jobs output dir on remote host
                ECF_LOGHOST=host,                     # remote log host
                ECF_LOGPORT=logport,                  # remote log port

                # Submit job (remotely)
                ECF_JOB_CMD="{} {} {} %ECF_JOB% %ECF_JOBOUT%".format(schedule, user, host),
             ),

             # Main Runs per day (00, 06, 12, 18)
             Family("RUN_00",
                Edit( LAUF='00', VORHI=0, LEAD=fcst, LEADCTL=fcstctl ),

                # add suite Families and Tasks
                family_lbc(),
                family_obs(),
                family_main(),
             ),

             Family("RUN_06",
                Edit( LAUF='06',VORHI=6, LEAD=assimc, LEADCTL=assimc ),
                Trigger("RUN_00 == complete"), 

                # add suite Families and Tasks
                family_lbc(),
                family_obs(),
                family_main(),
             ),

             Family("RUN_12",
                Edit( LAUF='12',VORHI=0, LEAD=fcst, LEADCTL=fcst ),
                Trigger("RUN_06 == complete"), 

                # add suite Families and Tasks
                family_lbc(),
                family_obs(),
                family_main(),
             ),

             Family("RUN_18",
                Edit( LAUF='18',VORHI=6, LEAD=assimc, LEADCTL=assimc ),
                Trigger("RUN_12 == complete"), 

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
print("=> saving definition to file " + suite_name + ".def\n");
defs.save_as_defs(suite_name + ".def");
exit(0);

