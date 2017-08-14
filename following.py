#!/usr/bin/python
import json
import sys
import random
import string

reload(sys)
sys.setdefaultencoding('utf8')

fi_n = open("data/net.txt", "r")
fi_u = open("data/user.txt", "r")
fi_g = open("sentiment/group.csv", "r")
fi_m = open("sentiment/group-net.txt", "r")
fi_f = open("data/following.txt", "r")
fo_m = open("data/group-mention.txt", "w")
fo_f = open("data/group-follow.txt", "w")
users = []
u2g = {}
g2g = {}
g2gm = {}
g2gf = {}
follow_num = 0
mention_num = 0
contain_num = 0

while 1:
    line = fi_g.readline()
    if not line:
        break
    temp_list = line.split(',')
    #temp_list = line.split()
    user = str(temp_list.pop(0))
    group = str(string.atoi(temp_list.pop(0)))
    g2gm[group] = {}
    g2gf[group] = {}
    u2g[user] = group

line = fi_m.readline()
while 1:
    line = fi_m.readline()
    if not line:
        break
    temp_list = line.split(',')
    #temp_list = line.split()
    g1 = temp_list.pop(0)
    g2 = temp_list.pop(0)
    if not g2g.has_key(g1):
        g2g[g1] = {}
    g2g[g1][g2] = 1

while 1:
    line = fi_u.readline()
    if not line:
        break
    temp_list = line.split()
    users.append(temp_list[0])
    
#rebuild user to user mention network
while 1:
    line = fi_n.readline()
    if not line:
        break
    mention_num += 1
    temp_list = line.split()

    src = temp_list.pop(0)
    if u2g.has_key(src):
        groups = u2g[src]
        for dst in temp_list:
            if u2g.has_key(dst):
    	        groupd = u2g[dst]
    	        if not g2gm[groups].has_key(groupd):
    	            g2gm[groups][groupd] = 0
    	        g2gm[groups][groupd] += 1

line = fi_f.readline()
while 1:
    if not line:
        break
    follow_num += 1
    temp_list = line.split()
    src = temp_list.pop(0)
    
    if src not in users or not u2g.has_key(src):
        while 1:
            line = fi_f.readline()
            if not line:
                break
            temp_list = line.split()
            src2 = temp_list.pop(0)
            if src2 != src:
                break
        continue
    groups = u2g[src]
    dst = temp_list.pop(0)
    if dst in users:
        if u2g.has_key(dst):
    	        groupd = u2g[dst]
    	        if not g2gf[groups].has_key(groupd):
    	            g2gf[groups][groupd] = 0
    	        g2gf[groups][groupd] += 1
    line = fi_f.readline()
    if not line:
        break

fo_m.write('s,d,v\n')
for groups in g2gm:
    if not g2g.has_key(groups):
        continue
    for groupd in g2gm[groups]:
        if not g2g[groups].has_key(groupd):
            continue
        fo_m.write(str(groups)+' '+str(groupd)+' '+str(g2gm[groups][groupd])+'\n')

fo_f.write('s,d,v\n')
for groups in g2gf:
    if not g2g.has_key(groups):
        continue
    for groupd in g2gf[groups]:
        if not g2g[groups].has_key(groupd):
            continue
        fo_f.write(str(groups)+' '+str(groupd)+' '+str(g2gf[groups][groupd])+'\n')

print mention_num, follow_num
fi_n.close()
fi_f.close()
