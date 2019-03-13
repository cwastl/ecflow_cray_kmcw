#!/usr/bin/env python2.7

import os

suite = "claef"
runs = ["00","06","12","18"]
famil = ["lbc","obs","main"]
members = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16"]
tasks_comp = ["complete"]
tasks_lbc = ["getlbc","901","getlbc_gl","gl"]
tasks_obs = ["getobs","bator","bator3D"]
tasks_main = ["927","pgd","927surf","sstex","addsurf","screen", "screensurf","canari","minim","001","progrid"]

if not os.path.exists("/home/ms/at/kmcw/ecf/" + suite):
    os.mkdir("/home/ms/at/kmcw/ecf/" + suite)

os.chdir("/home/ms/at/kmcw/ecf/" + suite)

for t in tasks_comp:

    if not os.path.lexists(t + ".ecf"):
        os.symlink("/home/ms/at/kmcw/ecf/scripts/" + t + ".ecf", t + ".ecf")

for r in runs:

     if not os.path.exists("RUN_" + r):
         os.mkdir("RUN_" + r)  

     for f in famil:

          if not os.path.exists("RUN_" + r + "/" + f):
              os.mkdir("RUN_" + r + "/" + f)

          if f == "lbc":

             for m in members:

                 if not os.path.exists("RUN_" + r + "/" + f + "/MEM_" + m):
                     os.mkdir("RUN_" + r + "/" + f + "/MEM_" + m)                     

                 for t in tasks_lbc:

                     if not os.path.lexists("RUN_" + r + "/" + f + "/MEM_" + m + "/" + t + ".ecf"):
                        os.symlink("/home/ms/at/kmcw/ecf/scripts/" + t + ".ecf", "RUN_" + r + "/" + f + "/MEM_" + m + "/" + t + ".ecf")

          if f == "obs":

             for t in tasks_obs:

                 if not os.path.lexists("RUN_" + r + "/" + f + "/" + t + ".ecf"):
                     os.symlink("/home/ms/at/kmcw/ecf/scripts/" + t + ".ecf", "RUN_" + r + "/" + f + "/" + t + ".ecf")

          if f == "main":

             for m in members:

                 if not os.path.exists("RUN_" + r + "/" + f + "/MEM_" + m):
                     os.mkdir("RUN_" + r + "/" + f + "/MEM_" + m)

                 for t in tasks_main:
 
                     if not os.path.lexists("RUN_" + r + "/" + f + "/MEM_" + m + "/" + t + ".ecf"):
                        os.symlink("/home/ms/at/kmcw/ecf/scripts/" + t + ".ecf", "RUN_" + r + "/" + f + "/MEM_" + m + "/" + t + ".ecf")
   




