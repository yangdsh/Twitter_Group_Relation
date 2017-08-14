#!/usr/bin/python
import json
import sys
import random
import math

reload(sys)
sys.setdefaultencoding('utf8')

fi_n = open("data/net.txt", "r")
fi_h2u = open("data/h2u.txt", "r")
fi_f2u = open("data/follow.txt", "r")
fo_n = open("edge.txt", "w")

u2h = {}
u2f = {}

while 1:
    line = fi_h2u.readline()
    if not line:
        break
    temp_list = line.split()
    dst = temp_list.pop(0)
    for src in temp_list:
        if u2h.has_key(src):
            u2h[src] += 1
        else:
            u2h[src] = 1

fi_h2u.close()
fi_h2u = open("data/h2u.txt", "r")

while 1:
    line = fi_f2u.readline()
    if not line:
        break
    temp_list = line.split()
    dst = temp_list.pop(0)
    for src in temp_list:
        if u2f.has_key(src):
            u2f[src] += 1
        else:
            u2f[src] = 1
            
fi_f2u.close()
fi_f2u = open("data/follow.txt", "r")
sumh = 0
sumf = 0

tag_num = 0
while 1:
    line = fi_h2u.readline()
    if not line:
        break
    temp_list = line.split()
    hashtag = temp_list.pop(0)
    length = len(temp_list)
    if length > 500:
        continue
    if length == 1:
        break
    for src in temp_list:
        idf = 1.0/math.log(length+1)
        tf = 1.0/u2h[src]
        val = tf*idf
        '''sample = 0
        try_num = 0
        while sample < num:
            dst = random.choice(temp_list)
            try_num += 1
            if try_num == 100*length:
                break
            if dst == src:
                continue
            sample += 1
            row_num += 1'''
        for dst in temp_list:
            if src != dst:
                sumh += val
                fo_n.write(src+' '+dst+' '+str(val)+'\n')
                tag_num += 1

while 1:
    line = fi_f2u.readline()
    if not line:
        break
    temp_list = line.split()
    dst = temp_list.pop(0)
    length = len(temp_list)
    for src in temp_list:
        idf = 1.0/math.log(length+1)
        tf = 1.0/u2f[src]
        val = 30*tf*idf+0.01
        sumf += val
        '''sample = 0
        try_num = 0
        while sample < num:
            dst = random.choice(temp_list)
            try_num += 1
            if try_num == 100*length:
                break
            if dst == src:
                continue
            sample += 1
            row_num += 1'''    
        fo_n.write(src+' '+dst+' '+str(val)+'\n')
            
'''
#rebuild user to user mention network
while 1:
    line = fi_n.readline()
    if not line:
        break
    temp_list = line.split()
    src = temp_list.pop(0)
    length = len(temp_list)
    if length == 0:
        continue  
    val = str(1/math.sqrt(length))
    for dst in temp_list:
        row_num += 1
        fo_n.write(src+' '+dst+' '+val+'\n')
'''
print tag_num, sumh, sumf

fi_n.close()
fi_h2u.close()
fo_n.close()
