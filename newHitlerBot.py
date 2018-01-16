#!/usr/bin/python

import praw
import re
import os
import datetime
import time

print "Sleeping"
time.sleep(360)

reddit = praw.Reddit('bot1')	#bot1 = u/Chudlybot63	bot2 = u/HitlerFallacyBot

subreddit = reddit.subreddit('Politics')
postSubreddit = reddit.subreddit('Justletmetest')

now = datetime.datetime.now()

#Input: A list of strings in the form "comment.id::submission.id"
#Output: A list of comment ids sorted by there submission id
def sortComments( id_list ):
	IDS = {}
	postIDs = []
	sortedList = []

	for x in hitlerIDs:
		y = x.split("::")
		POST_ID=y[1]
		COMMENT_ID=y[0]	
		if IDS.has_key(POST_ID):
			l = IDS[POST_ID]
		else:
			postIDs.append(POST_ID)
			l = []
		l.append(COMMENT_ID)
		IDS[POST_ID] = l
	for post in postIDs:
		comments = IDS[post]
		for c in comments:
			sortedList.append(c)
	return sortedList



#Input: The full body of a comment
#Output: A single sentence of the comment containing the word "Hitler"
def cleanUpComment( Q ):
	print Q + "\n\n\n\n\n\n\n"
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



def constuctPost( commentIDs ):
	postText = ""
	quotes = []
	currentPost = ""
	hitlerCount = 0
	for i in range(len(commentIDs)):
		com = reddit.comment(commentIDs[i])
		if not com.body == "[deleted]" or com.body == "[removed]":	#Cowards
			if not currentPost == com.submission.id:	#New Post
				quotes = []
				currentPost = com.submission.id
				postText += "\n#####" + com.submission.title 
			quote = cleanUpComment( com.body )
			commentLink = "https://www.reddit.com" + com.permalink
			if quote not in quotes:
				quotes.append(quote)
				hitlerCount +=1
				postText += '\n- ["' +  quote + '."](' + commentLink + ') - ' + str(com.author) + '\n'

	postText = "#I found " + str(hitlerCount) + " Hitlers in r/Politics today!\n\n***\n\n" + postText
	return postText



#Gathers comments by reading all posts from the last 24 hours. Takes a long time to run. ~1 hour
#This function is only used as a backup in case the comment stream failed to run
def oldFasionedTechnique( ):
	submissionIDs = []
	hitlerIDs = []
	for submission in subreddit.top('day', limit = None):
 		if submission.id not in submissionIDs:
			print "--Submission"
			submissionIDs.append(submission.id)
			quotes = []
			submission.comments.replace_more(limit = None)
			for comment in submission.comments.list():
				if re.search("hitler", comment.body, re.IGNORECASE):
					hitlerIDs.append(str(comment.id) + "::" + str(submission.id))
					print str(comment.id)
	return hitlerIDs



def transferFiles( ):
	if not os.path.isfile("streamFindings.txt"):
		print "File Not Found"
		me = reddit.redditor(name='chudly63')
		me.message(str(now), "streamFindings.txt was missing. Using top 24 hours.")
		return oldFasionedTechnique()
	else:
		with open("streamFindings.txt","r") as f:
			hitlerIDs = f.read()
			with open("backup.txt", "w") as w:
				w.write(hitlerIDs)
			hitlerIDs = hitlerIDs.split("\n")
			hitlerIDs = list(filter(None, hitlerIDs))
		os.remove("/home/boadster/Documents/python/StreamPractice/streamFindings.txt")		
		return hitlerIDs

print "Getting IDs"
hitlerIDs = transferFiles( )

print "Sorting IDs"
hitlerIDs = sortComments(hitlerIDs)

print "Constructing Post"
body = constuctPost(hitlerIDs)

title = "Hitler Hunt Beta for " + str(now.month) + "/"+ str(now.day) + "/" + str(now.year)

postSubreddit.submit(title,selftext=body)
