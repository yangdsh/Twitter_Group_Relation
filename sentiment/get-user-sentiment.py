from pattern.en import sentiment
#from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys
import string

reload(sys)
sys.setdefaultencoding('utf8')  

analyzer = SentimentIntensityAnalyzer()
fi_w = open('sentiment/negword2.txt', 'r')
fi_t = open('sentiment/text.txt', 'r')
fo_s = open('sentiment/sentiment.txt', 'w')
fo_s.write('Turkey ')
fo_sample = open('sentiment/sentiment_sample.txt', 'w')

hashtag = ''
sentence = ''
negwords = []

while 1:
    line = fi_w.readline()
    if not line:
    	break
    word = (line.split())[0]
    negwords.append(word)

i = 0
neg_num = 0
line = fi_t.readline()
while 1:
    temp_list = line.split()  
    hashtag = temp_list[1]
    #fo_s.write(hashtag+' ')
    line = fi_t.readline()
    while 1:
    	temp_list = line.split()
    	user = temp_list[1]
    	geo = temp_list[2]
    	while 1:	
    		sentence += line
    		line = fi_t.readline()
    		if not line or line[0] == ')' or line[0] == ']':
    			break
	templist = sentence.split()
    	shortlist = []
    	for temp in templist:
    		word = string.lower(temp[0:5])
    		if word[0] == '#':
    			word = word[1:5]
    		else:
    			word = word[0:4]
        	shortlist.append(word)
    	if 1:
    	#if temp_list[2] == 'Aug' and string.atoi(temp_list[3]) < 20:
    		result = sentiment(sentence)
    		vs = analyzer.polarity_scores(sentence)
    		myresult = 1
    		for word in negwords:
    			if word in shortlist:
    				myresult = -1
    				break
    		if myresult == -1:
    			neg_num += 1
    		if myresult * vs['compound'] < 0:
    			i += 1
    			if i < 50:
    				fo_sample.write(str(vs['compound'])+' '+str(myresult)+' ('+sentence+'\n')
    		fo_s.write(user+' '+str(myresult)+' '+geo+' ')
    		sentence = ''
        else:
        	sentence = ''
    	if not line or line[0] == ']':
    		break
    fo_s.write('\n')
    if not line:
    	break
print i, neg_num

fi_t.close()
fo_s.close()
