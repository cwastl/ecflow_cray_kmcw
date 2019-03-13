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

#ensemble members
members = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
#members = [13]

# coupling frequency
couplf = 6

# use GL Tool yes/no, if no - 901 is used
gl = False

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
  'dd'  : '13',
  'mm'  : '03',
  'yyyy': '2019'
}

###########################################
#####define Families and Tasks#############
###########################################

def date():

    try: 
       user_date
       print("=> date defined by user\n")
       return user_date['yyyy'] + user_date['mm'] + user_date['dd']

    except NameError:
       print("=> current date")
       return now.strftime('%Y%m%d')
          
def family_lbc():

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
                Complete(":GL == 1"),
                Edit(
                   NP=1,
                   CLASS='ns',
                   KOPPLUNG=couplf,
                   MEMBER="{:02d}".format(mem),
                   NAME="getlbc{:02d}".format(mem),
                   WALLT="01",
                ),
                Label("run", ""),
                Label("info", ""),
                Label("error", ""),
             )
          ],

          # Task 901
          [
             Task("901",
                Trigger(":GL == 0 and getlbc == complete"),
                Complete(":GL == 1"),
                Edit(
                   NP=1,
                   CLASS='ns',
                   KOPPLUNG=couplf,
                   MEMBER="{:02d}".format(mem),
                   NAME="901_{:02d}".format(mem),
                   WALLT="03",
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
                   MEMBER="{:02d}".format(mem),
                   NAME="getlbcgl{:02d}".format(mem),
                   WALLT="01",
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
                   WALLT="03"               #walltime in hours
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
                WALLT="01"              #walltime in hours
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
                WALLT="01"               #walltime in hours
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
                WALLT="01"               #walltime in hours
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
         GL=gl),

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
                     WALLT="03"                #walltime in hours
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
#                    WALLT="01"                #walltime in hours
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
                     WALLT="01"                #walltime in hours
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
                     WALLT="01"                #walltime in hours
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
                     WALLT="01"                #walltime in hours
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
                     WALLT="03"                #walltime in hours
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
                     WALLT="03"                #walltime in hours
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
                     WALLT="03"                #walltime in hours
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
                     WALLT="03"                #walltime in hours
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
                     NP=480,
                     CLASS='np',
                     KOPPLUNG=couplf,
                     ASSIMC=assimc,
                     STOCH=stophy,
                     NAME="001_{:02d}".format(mem),
                     WALLT="06"                #walltime in hours
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task PROGRID
            [
               Task("progrid",
                  Trigger("001  == complete"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     NAME="progrid{:02d}".format(mem),
                     WALLT="01"                #walltime in hours
                  ),
                  Label("run", ""),
                  Label("info", ""),
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
          Suite("claef_2").add(

             Edit(

                # ecflow configuration
                ECF_MICRO='%',         # ecf micro-character
                ECF_EXTN='.ecf',        # ecf files extension
                ECF_HOME=home,         # ecf root path
                ECF_INCLUDE=incl,      # ecf include path
                ECF_TRIES=1,           # number of reruns if task aborts
                DATUM=date(),

                # suite configuration variables
                ACCOUNT=account,
                CNF_DEBUG=debug,

                # Running jobs remotely on HPCF
                ECF_OUT = '/scratch/ms/at/kmcw/ECF', # jobs output dir on remote host
                ECF_LOGHOST=host,                     # remote log host
                ECF_LOGPORT=logport,                  # remote log port
                ECF_LISTS='/home/ms/at/kmcw/ecf/def/perm.list', 

                # Submit job (remotely)
                ECF_JOB_CMD="{} {} {} %ECF_JOB% %ECF_JOBOUT%".format(schedule, user, host),
             ),

#             # Main Runs per day (00, 06, 12, 18)
#             Family("RUN_00",
#                Edit( LAUF='00', VORHI=0, LEAD=6),
#
#                # add suite Families and Tasks
#                family_lbc(),
#                family_obs(),
#                family_main(),
#             ),

             Family("RUN_06",
                Edit( LAUF='06',VORHI=6, LEAD=6),

                # add suite Families and Tasks
                family_lbc(),
                family_obs(),
                family_main(),
              ),

#             Family("RUN_12",
#                Edit( LAUF='12',VORHI=6, LEAD=6),
#
#                # add suite Families and Tasks
#                family_lbc(),
#                family_obs(),
#                family_main(),

#             Family("RUN_18",
#                Edit( LAUF='18',VORHI=6, LEAD=6),
#
#                # add suite Families and Tasks
#                family_lbc(),
#                family_obs(),
#                family_main(),
#             ),
             
          )
       )

###################################
### check and save C-LAEF suite ###
###################################

print("=> checking job creation: .ecf -> .job0");
print(defs.check_job_creation());
print("=> saving definition to file 'claef_2.def'\n");
defs.save_as_defs("claef_2.def");
exit(0);

