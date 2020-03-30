#!/usr/local/apps/python/2.7.12-01/bin/python2.7

import random

random.seed(20190525)
zufall=random.sample(range(1,17),3)
#print("%02d" % (zufall[1]))
#for x in range(len(zufall)): 
#    zufall2[x]=("%02d"% (zufall[x]))
print(zufall)
