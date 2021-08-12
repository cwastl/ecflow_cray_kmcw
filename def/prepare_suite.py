#!/usr/bin/env python3

import os

suite = "claef"
runs = ["00","06","12","18"]
ofamil = ["admin","runs"]
famil = ["obs","main","harp"]
members = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16"]
tasks_comp = ["complete","cleanlog"]
tasks_ez_trigger = ["dummy1"]
tasks_check_obs = ["dummy2"]
tasks_check_main = ["dummy2"]
tasks_clean = ["cleaning"]
tasks_harp = ["harpio"]
tasks_obs = ["getobs","bator","bator3D","pregps"]
tasks_main = ["927","pgd","927surf","sstex","addsurf","varbccomb","screen","screensurf","canari","minim","pertsurf","001","progrid","addgrib","verif","transfer","archmars"]

hpath="/home/ms/at/kmcw/ecf/"

if not os.path.exists(hpath + suite):
   os.mkdir(hpath + suite)

os.chdir(hpath + suite)

for s in ofamil:
      
     if not os.path.lexists(s):
        os.mkdir(s)
        
     if s == "admin":

        for t in tasks_comp:

           if not os.path.lexists(s + "/" + t + ".ecf"):
              os.symlink(hpath + "scripts/" + t + ".ecf", s + "/" + t + ".ecf")

     if s == "runs":

        os.chdir(s)

        if not os.path.lexists("dummy.ecf"):
           os.symlink(hpath + "scripts/dummy.ecf", "dummy.ecf")

        for r in runs:

           if not os.path.exists("RUN_" + r):
              os.mkdir("RUN_" + r)  

           if not os.path.exists("RUN_" + r + "/dummy"):
              os.mkdir("RUN_" + r + "/dummy")  

           if not os.path.exists("RUN_" + r + "/dummy" + "/ez_trigger"):
              os.mkdir("RUN_" + r + "/dummy" + "/ez_trigger")  

           for s in tasks_ez_trigger:

              if not os.path.lexists("RUN_" + r + "/dummy" + "/ez_trigger/" + s + ".ecf"):
                 os.symlink(hpath + "scripts/" + s + ".ecf", "RUN_" + r + "/dummy" + "/ez_trigger/" + s + ".ecf")

           if not os.path.exists("RUN_" + r + "/dummy" + "/check_obs"):
              os.mkdir("RUN_" + r + "/dummy" + "/check_obs")

           for s in tasks_check_obs:

              if not os.path.lexists("RUN_" + r + "/dummy" + "/check_obs/" + s + ".ecf"):
                 os.symlink(hpath + "scripts/" + s + ".ecf", "RUN_" + r + "/dummy" + "/check_obs/" + s + ".ecf")
 
           if not os.path.exists("RUN_" + r + "/dummy" + "/check_main"):
              os.mkdir("RUN_" + r + "/dummy" + "/check_main")

           for s in tasks_check_main:

              if not os.path.lexists("RUN_" + r + "/dummy" + "/check_main/" + s + ".ecf"):
                 os.symlink(hpath + "scripts/" + s + ".ecf", "RUN_" + r + "/dummy" + "/check_main/" + s + ".ecf")

           for t in tasks_clean:

              if not os.path.lexists("RUN_" + r + "/" + t + ".ecf"):
                 os.symlink(hpath + "scripts/" + t + ".ecf", "RUN_" + r + "/" + t + ".ecf")

           for f in famil:

              if not os.path.exists("RUN_" + r + "/" + f):
                 os.mkdir("RUN_" + r + "/" + f)

              if f == "obs":

                 for t in tasks_obs:

                    if not os.path.lexists("RUN_" + r + "/" + f + "/" + t + ".ecf"):
                        os.symlink(hpath + "scripts/" + t + ".ecf", "RUN_" + r + "/" + f + "/" + t + ".ecf")

              if f == "main":

                 for m in members:

                    if not os.path.exists("RUN_" + r + "/" + f + "/MEM_" + m):
                       os.mkdir("RUN_" + r + "/" + f + "/MEM_" + m)

                    for t in tasks_main:
 
                       if not os.path.lexists("RUN_" + r + "/" + f + "/MEM_" + m + "/" + t + ".ecf"):
                          os.symlink(hpath + "scripts/" + t + ".ecf", "RUN_" + r + "/" + f + "/MEM_" + m + "/" + t + ".ecf")

              if f == "harp":

                 for t in tasks_harp:

                    if not os.path.lexists("RUN_" + r + "/" + f + "/" + t + ".ecf"):
                        os.symlink(hpath + "scripts/" + t + ".ecf", "RUN_" + r + "/" + f + "/" + t + ".ecf")
 
