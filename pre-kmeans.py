import sys
import string
fi_t = open("sentiment/text.txt", "r")
fi_s = open("sentiment/stopword.txt", "rb")
fi_u = open("data/user.txt", "r")
fi_m = open("data/net.txt", "r")
fo_w = open("sentiment/keyword.txt", "w")
fo_k = open("sentiment/k2u.txt", "w")
fo_n = open("sentiment/negword2.txt", "w") 

consider_mention = 0

stopword = []
mention = {}
words = {}
words_short = {}
user_id = {}

while 1:
    line = fi_u.readline()
    if not line:
        break
    templist = line.split()
    user_id[templist[0]] = templist[1]

while 1:
    line = fi_m.readline()
    if not line:
        break
    templist = line.split()
    src = templist.pop(0)
    mention[src] = []
    for dst in templist:
        mention[src].append(dst)

while 1:
    line = fi_s.readline()
    if not line:
        break
    templist = line.split()
    stopword.append(templist[0])

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
    templist.pop(0)
    templist.pop(0)
    templist.pop(0)
    templist.pop(0)
    templist.pop(0)
    for Word in templist:
        word_lower = string.lower(Word)
        word_short = word_lower[0:4]
        if words_short.has_key(word_short):
            words_short[word_short] += 1
        elif word_short not in stopword and word_lower not in stopword and word_lower.isalpha():
            words_short[word_short] = 1

words_sort = sorted(words_short.iteritems(), key=lambda d:d[1], reverse = True)
words_top = []
w2u = {}
word_num = 0

for (word, v) in words_sort:
    if v < 50:
        break
    if v > 1500:
        continue
    word_num += 1
    fo_w.write(word +' '+str(v))
    fo_w.write('\n')
    words_top.append(word)
    w2u[word] = {}

fi_t.close()
fi_t = open("sentiment/text.txt", "r")
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
    shortlist = []
    for temp in templist:
        shortlist.append(string.lower(temp[0:4]))
    for word in words_top:
        if word in shortlist:
            w2u[word][user_id[user]] = 1
        else:
            w2u[word][user_id[user]] = 0

fo_k.write(str(word_num)+' '+str(len(user_id))+' '+str(5)+'\n')    
for (word, v) in words_sort:
    if not w2u.has_key(word):
        continue
    for id in w2u[word]:
        fo_k.write(str(w2u[word][id])+' ')
    fo_k.write('\n')
    
fi_n = open("sentiment/negword.txt", "r")
negrank3 = {}
negwords = []
negusers = {}
similar = {}
for word in words_top:
    similar[word] = {}
    
while 1:
    line = fi_n.readline()
    if not line:
        break
    templist = line.split()
    negwords.append(templist[0])
    negrank3[templist[0]] = 1

iter = 0
cnt1 = 0
while iter < 5:
    iter += 1
    fi_t.close()
    fi_t = open("sentiment/text.txt", "r")
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
        shortlist = []
        for temp in templist:
            shortlist.append(string.lower(temp[0:4]))
        for word in negwords:        
            if word in shortlist:
                negusers[user] = sentence
                if consider_mention:
                    for dst in mention[user]:
                        if not negusers.has_key(dst):
                            negusers[dst] = ''
                break 

    fo_s = open("sentiment/similar_rank.txt", "w")
    '''
for word1 in words_top:
    maxsim = 0
    wordsim = ''
    for word2 in words_top:
        if word1 == word2:
            continue
        common = 0.0
        for i in range(0, len(user_id)-1):
            id = str(i)
            if w2u[word1][id] == 1 and w2u[word2][id] == 1:
                common += 1
        similar[word1][word2] = common/words_short[word2]
        #similar[word1][word2] = common
        if similar[word1][word2] > maxsim:
            maxsim = similar[word1][word2]
            wordsim = word2
    sim_sort = sorted(similar[word1].iteritems(), key=lambda d:d[1], reverse = True)
    fo_s.write(word1+' ')
    num = 0
    for (word, sim) in sim_sort:
        num += 1
        fo_s.write(word+' ')
        if num == 5:
            break
    fo_s.write('\n')
    if wordsim in negwords and word1 not in negwords:
        negwords.append(word1)
    '''
    fi_t.close()
    fi_t = open("sentiment/text.txt", "r")
    negrank = {}
    negrank2 = {}
    for word in words_top:
        negrank[word] = 0.0
        negrank2[word] = 0.0
    
    cnt2 = 0 
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
        shortlist = []
        neg = 0
        if consider_mention:
            for nuser in negusers:
                if nuser in mention[user] and not negusers.has_key(user):
                    neg = 1
            if neg == 1:
                negusers[user] = ''
        if negusers.has_key(user):
        #if 1:
            if negusers[user] != sentence:
                cnt2 += 1
                for temp in templist:
                    shortlist.append(string.lower(temp[0:4]))
                for word in shortlist:
                    if word in words_top:
                        negrank[word] += 1
        if iter == 1:
            cnt1 = cnt2        
    for word in negrank:
        negrank[word] = negrank[word]/words_short[word]
    neg_sort = sorted(negrank.iteritems(), key=lambda d:d[1], reverse = True)
    num = 0
    nwords = []
    for (word, neg) in neg_sort:
        if word in negwords:
            continue
        num += 1
        #if num > 20:
        #    break
        nwords.append(word)
    
    fi_t.close()
    fi_t = open("sentiment/text.txt", "r")
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
        shortlist = []
        for temp in templist:
            shortlist.append(string.lower(temp[0:4]))
        for nword in nwords:
            if nword in shortlist:
                #for nuser in negusers:
                #    if user == nuser:
                for word in negwords:
                    if word in shortlist:
                        negrank2[nword] += 1
    for word in negrank2:
        negrank2[word] = negrank[word] * negrank2[word]/words_short[word]
        
    neg_sort = sorted(negrank2.iteritems(), key=lambda d:d[1], reverse = True)
    
    num = 0
    for (word, neg) in neg_sort:
        if word in negwords:
            continue
        num += 1
        if neg < 0.23*cnt2/cnt1*iter:
            break
        negwords.append(word)
        negrank3[word] = neg/cnt2*cnt1/iter
    for (word, neg) in neg_sort:
        fo_s.write(word+' '+str(neg)+'\n')

neg_sort = sorted(negrank3.iteritems(), key=lambda d:d[1], reverse = True)
for (word, neg) in neg_sort:
    fo_n.write(word+'\n')    
   
print cnt1, cnt2 
