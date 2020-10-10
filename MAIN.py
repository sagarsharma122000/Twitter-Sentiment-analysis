import re
import nn 
import numpy as np
from nn import NeuralNetwork
import twitters
from twitters import TwitterClient

def processTweet(tweet):
   
    tweet = tweet.lower()
    
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    
    tweet = re.sub('[\s]+', ' ', tweet)
    
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    
    tweet = tweet.strip('\'"')

    return tweet

positive = []
negative = []



with open("positive_keywords.txt") as f:
    for line in f:
        line=line.strip()
        positive.append(line)

with open("negative_keywords.txt") as f:
    for line in f:
        line=line.strip()
        negative.append(line)

data=[]
output=[]

with open("data.txt") as f:
	for line in f:
		line=line.strip("\n")
		data.append(line)

with open("target.txt") as f:
	for line in f:
		line=line.strip("\n")
		output.append(line)

posCnt=0
negCnt=0
idx=0

print(len(data))
print(len(output))
big=[]
op=[]
for tweet in data:
	tweet=processTweet(tweet)
	tweet=re.sub(r'[^\w\s]','',tweet)
	#print tweet
	tweet=tweet.split()
	posCnt=0
	negCnt=0
	small=[]
	for word in tweet:
		word=word.strip('\'"?,.!')
		word=word.lower()
		if word in positive:
			posCnt+=1
		if word in negative:
			negCnt+=1
	print(posCnt)
	print(negCnt)
	small.append(posCnt)
	small.append(negCnt)
	big.append(small)
	target=output[idx]
	if target=="positive":
		op.append(1)
	elif target=="negative":
		op.append(-1)
	else:
		op.append(0)
	print(target)
	idx=idx+1


nn = NeuralNetwork([2,2,1])

X = np.array(big)

y = np.array(op)

nn.fit(X, y)


api = TwitterClient()
q = input("Enter the keyword to search about : ")
c = int(input("Number of query: "))
tweets = api.get_tweets(query = q , count = c)
pos = 0
neg = 0
neut = 0
for tweet in tweets:
    stmt = tweet['text']
    tw = processTweet(stmt)
    tw = re.sub(r'[^\w\s]','',tw)
    tw = tw.split()
    posCnt=0
    negCnt=0
    small=[]
    for word in tw:
        word=word.strip('\'"?,.!')
        word=word.lower()
        if word in positive:
            posCnt+=1
        if word in negative:
            negCnt+=1
    small.append(posCnt)
    small.append(negCnt)

    ans=nn.predict(small)
    if ans >= 0.5:
        pos = pos +1
    elif ans<=-0.4:
        neg = neg +1
    else:
        neut = neut +1 
    print(ans)

print("\n\n")
posper = (pos*100)/c
negper = (neg*100)/c
neutper = (neut*100)/c

print("Positive Tweets Percentage is: {}%".format(posper))
print("Negative Tweets Percentage is: {}%".format(negper))
print("Neutral Tweets Percentage is: {}%".format(neutper))
