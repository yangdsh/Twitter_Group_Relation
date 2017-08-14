import string
import copy
import random
import math
import numpy as np

fi_s = open('sentiment/sentiment.txt', 'r')
#fi_g = open('sentiment/grouping.txt', 'r')
fi_g = open('sentiment/group.csv', 'r')
fo_z = open('sentiment/g-sentiment.txt', 'w')
fo_geo = open('sentiment/geo-sentiment.txt', 'w')
fo_g2g = open('sentiment/group-net.txt', 'w')

g2s = {}
u2g = {}
g2n = {}
geo2s = {}
geo2n = {}
g2m = {}
g2v = {}

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

tag_num = 0
n = 0
m = 0
z = 0
while tag_num < 1:
	tag_num += 1
	line = fi_s.readline()
	if not line:
		break
	temp_list = line.split()
	
	hashtag = temp_list.pop(0)

	while len(temp_list) > 0:
		m += 1
		user = temp_list.pop(0)
		sentiment = string.atof(temp_list.pop(0))
		geo = temp_list.pop(0)
		if u2g.has_key(user):	
			group = u2g[user]
		else:
			continue
		n += 1
		if g2s.has_key(group):
			g2s[group].append(sentiment)
			g2n[group] += 1
		else:
			g2s[group] = []
			g2s[group].append(sentiment)
			g2n[group] = 1
		if geo2s.has_key(geo):
			geo2s[geo].append(sentiment)
			geo2n[geo] += 1
		else:
			geo2s[geo] = []
			geo2s[geo].append(sentiment)
			geo2n[geo] = 1

	for group in g2s:
		if sum(g2s[group]) != 0.0 and g2n[group] > 30:
			meani = []
			for i in range(0,100):
				vlist = copy.deepcopy(g2s[group])
				random.shuffle(vlist)
				random.shuffle(vlist)
				while len(vlist) > g2n[group]*0.6:
					vlist.pop(0)
				narray = np.array(vlist)
				sumi = narray.sum()
				meani.append(sumi/len(vlist))
			N = len(meani)
			array1 = np.array(meani)
			sum1 = array1.sum()
			mean = sum1/N
			deviation = np.std(array1)*math.sqrt(g2n[group])
			fo_z.write(str(group)+','+hashtag+','+str(len(g2s[group]))+','+str(sum(g2s[group])/g2n[group])+','+str(mean)+','+str(deviation)+'\n')
			g2m[group] = mean
			g2v[group] = deviation
			z += g2n[group]
	for group in geo2s:
		if sum(geo2s[group]) != 0.0 and geo2n[group] > 10:
			meani = []
			for i in range(0,100):
				vlist = copy.deepcopy(geo2s[group])
				random.shuffle(vlist)
				random.shuffle(vlist)
				while len(vlist) > geo2n[group]*0.6:
					vlist.pop(0)
				narray = np.array(vlist)
				sumi = narray.sum()
				meani.append(sumi/len(vlist))
			N = len(meani)
			array1 = np.array(meani)
			sum1 = array1.sum()
			mean = sum1/N
			fo_geo.write(str(group)+','+hashtag+','+str(len(geo2s[group]))+','+str(sum(geo2s[group])/geo2n[group])+','+str(mean)+','+str((np.std(array1))*math.sqrt(geo2n[group]))+'\n')
			z += geo2n[group]
	geo2s.clear()
	geo2n.clear()
	
	fo_g2g.write('g1,g2,val\n')
	for group1 in g2m:
		for group2 in g2m:
			if abs(g2m[group1] - g2m[group2]) > 1.5:
				fo_g2g.write(str(group1)+','+str(group2)+','+str(-abs(g2m[group1] - g2m[group2]))+'\n')
			if abs(g2m[group1] - g2m[group2]) < 0.2 and abs(g2v[group1] + g2v[group2]) < 1:
				fo_g2g.write(str(group1)+','+str(group2)+','+str(1/(0.5+abs(g2m[group1] - g2m[group2])))+'\n')
print m, n, z
