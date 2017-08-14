import string
import copy
import random
import math
import numpy as np

fi_t = open('sentiment/text.txt', 'r')
fi_g = open('sentiment/group.csv', 'r')
fo_g = open('sentiment/g2geo.txt', 'w')
fo_geo = open('sentiment/geo2g.txt', 'w')

g2geo = {}
geo2g = {}
u2g = {}
g2n = {}
geo2n = {}

#line = fi_g.readline()
while 1:
    line = fi_g.readline()
    if not line:
        break
    temp_list = line.split(',')
    #temp_list = line.split()
    user = str(temp_list.pop(0))
    group = string.atoi(temp_list.pop(0))
    u2g[user] = group
    g2geo[group] = {}
    g2n[group] = 0.0

line = fi_t.readline()
while 1:
    sentence = ''
    while 1:	
        sentence += line
        line = fi_t.readline()
        if not line or line[0] == ')':
    	    break
    if not line:
        break
    templist = sentence.split()
    user = templist.pop(1)
    geo = templist.pop(1)
    if geo == 'none' or not u2g.has_key(user):
    	continue
    group = u2g[user]
    if not g2geo[group].has_key(geo):
    	g2geo[group][geo] = 0
    g2geo[group][geo] += 1
    g2n[group] += 1

fo_g.write('group geo val\n')
for group in g2geo:
    if g2n[group] < 20:
    	continue
    for geo in g2geo[group]:
    	if not geo2n.has_key(geo) or g2geo[group][geo]/g2n[group] > geo2n[geo]:
    	    geo2g[geo] = group
    	    geo2n[geo] = g2geo[group][geo]/g2n[group]
    	fo_g.write(str(group)+','+geo+','+str(g2geo[group][geo]/g2n[group])+'\n')

for geo in geo2g:
    fo_geo.write(geo+','+str(geo2g[geo])+'\n')

fi_t.close()
fi_g.close()
fo_g.close()
