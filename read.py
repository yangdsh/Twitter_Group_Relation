#!/usr/bin/python
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

fi = open("tweet_data/nato_fixed.json", "r")
fo_u = open("data/user.txt", "w")
fo_n = open("data/net.txt", "w")
fo_h = open("data/hashtag.txt", "w")
fo_t = open("sentiment/text.txt", "w")
fo_h2u = open("data/h2u.txt", "w")

user = []
user_repeat = {}
net = {}
hashtags = {}
u2h = {}
h2t = {}
h2u = {}
iden = []
keytag = ['Turkey']
record = 0
row_num = 0
for tag in keytag:
    h2t[tag] = []

while 1:
    line = fi.readline()
    if not line:
        break
    data = json.loads(line)
    if str(data['lang']) != 'en':
        continue
    row_num += 1
    user_id = str(data['user']['id'])
    text = str(data['text'])   
    mention_list = data['entities']['user_mentions']
    hashtag = data['entities']['hashtags']
    time = data['created_at']
    timezone = data['user']['time_zone']
    timelist = time.split()  
    
    #build h2t network
    for ktag in keytag:            
        if ktag in text:
            identify = user_id + timelist[2] + text
            if identify in iden:
            	break
            if timezone:
            	h2t[ktag].append(user_id+' '+timezone+' '+timelist[1]+' '+timelist[2]+' '+text)
            	iden.append(identify)
            else:
            	h2t[ktag].append(user_id+' none '+timelist[1]+' '+timelist[2]+' '+text)
            record = 1
            break
    if record == 1:
        record = 0
        #record user
        if user_id not in user:
            user.append(user_id)
            net[user_id] = []
            u2h[user_id] = []
        #build u2h network
        if len(hashtag) > 0:
            for tag in hashtag:
                tag_text = tag['text']
                if not h2u.has_key(tag_text):
                    h2u[tag_text] = []
                    hashtags[tag_text] = 0
                h2u[tag_text].append(user_id)
                hashtags[tag_text] += 1
                if tag_text not in u2h[user_id]:
                    u2h[user_id].append(tag_text)
        #build mention network
        for mser in mention_list:
            net[user_id].append(str(mser['id']))

#write results
sum = 0
for key in user_repeat:
    fo_r.write(key+' '+str(user_repeat[key])+'\n')

'''
for id in user:
    fo_u.write(id+' ')
    if len(u2h[id]) > 0:
        for tag in u2h[id]:
            fo_u.write(tag + ' ')
    fo_u.write('\n')
'''
num = 0
for id in user:
    fo_u.write(id+' '+str(num))
    fo_u.write('\n')
    num += 1

for src_id in user:
    fo_n.write(str(src_id)+' ')
    if len(net[str(src_id)]) > 0:
        for tgt_id in net[str(src_id)]:
            if tgt_id in user:
                fo_n.write(str(tgt_id)+' ')
                sum += 1
    fo_n.write('\n')
   
hashtags_sort = sorted(hashtags.iteritems(), key=lambda d:d[1], reverse = True)

for (hashtag, v) in hashtags_sort:
    fo_h2u.write(hashtag+' ')
    for ut in h2u[hashtag]:
        fo_h2u.write(ut+' ')
    fo_h2u.write('\n')
    
    fo_h.write(hashtag +' '+str(v))
    fo_h.write('\n')
    
for hashtag in keytag:
    #fo_t.write(']'+' ' + hashtag +'\n')
    for ut in h2t[hashtag]:
    	fo_t.write(')'+' '+ut+'\n')
    
print row_num, len(user)

fi.close()
fo_u.close()
fo_h.close()
fo_n.close()
fo_t.close()
