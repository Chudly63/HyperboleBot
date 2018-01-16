#!/usr/bin/python
#
#Alex M Brown
#12/20/2017
#
#
#ReadingBot.py - reads comments from Reddit
#		 Will be used for later projects
#

import praw
import datetime
import re 
import time
from praw.exceptions import APIException




def cleanUpComment( Q ):

	sentences = re.split("(\.|\?|\!|\n)",Q)
	x = [sentence for sentence in sentences if 'hitler' in sentence.lower()]
	target = x[0].replace("\n","") 		#Target becomes the sentence in the comment containing the word Hitler
	target = target.replace('"','')		#Remove double quotes
	target = target.replace('[','\[')	#Escape square brackets for Reddit's formatting
	target = target.replace(']','\]') 	
	target = target.replace('>','') 	#Remove '>' : This symbol is used on Reddit to symbolize quotes, so it appears often.
	target = target.replace('  ',' ') 	#Remove extra spaces between words.
	while target[:1] == " " :		
		target = target[1:]		#Remove the first character of the quote if it is blank
	target = target[:1].upper() + target[1:]#Capitalize the first letter
	return target

				




	

reddit = praw.Reddit('bot1')
now = datetime.datetime.now()

subreddit = reddit.subreddit('politics')

date = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
print date
num = 0
ABORT = False
while not ABORT:
	try:
		for comment in subreddit.stream.comments():
			if re.search("hitler", comment.body, re.IGNORECASE):
				num +=1
				quote = cleanUpComment(comment.body)
				print str(num) + ". " + quote + "\n\n"


				with open("streamFindings.txt","a") as f:
					f.write(comment.id+"::"+comment.submission.id+"\n")
	
	except Exception as err:
		print err
		time.sleep(15)

