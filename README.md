# Twitter_Group_Relation
This work is mostly done during 2017 summer internship at CASOS in CMU. This project is not finished. We are adding more functions and debugging.
## Introduction
For two groups of people on Twitter, our project aims to find out how these two groups like each other. 
These two groups may not talk to each other directly. However, it is highly possible that they talk about similar topics. 
Our strtegy is to measure their attitudes towards those topics, and if they share similar opinions, these two groups have close relation.
Otherwise, if they do not talk about similar topics or they have different opinions towards most of their co-mention topics, 
these two groups do not have close relation.
## Structure
### Topic Clustering
In this part we split input tweets into different topics. 
Each topic is mined from input tweets by runing Louvain Grouping Algorithm on the word co-existance network.
The insight is that if some words always appear together, they are under the same topic.
### Sentiment Analysis
First, we use bootstrap algorithm to learn sentiment words from tweets. 
Then we run Vader Sentiment Algorithm with its lexicon in addition to the learned sentiment words.
After that, we get the sentiment of all users in each group.
### Relation Analysis
First we aggragate the sentiment of each group towards each topic. 
Then we compute the relation of two groups by weighting their difference on each topic.
The factors influencing the weight include the consistence of sentiments within the group, and the percentage of users mention this topic within the group.
## How to run the code
```makefile
sudo sh auto.sh
```
