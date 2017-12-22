#!/usr/bin/python
#
#Alex M Brown
#12/20/2017
#
#hitlerBot.py - Navigates r/politics and keeps tracks of how many times people mention Hitler
#		This program runs every 24 hours at 23:50 EST
#		It reads all the comments on posts in r/Politics that were posted that day
#		Any comments that mention Hitler are saved
#		The bot posts all the links it finds each day to r/TheHitlerFallacy
#
import praw
import pdb
import re
import os
import datetime


#Create a reddit instance using the config settings stored in praw.ini
reddit = praw.Reddit('bot2')


#commentsWithHitler.txt stores the ID of comments that have "Hitler" and have already been read by the bot.
#This keeps the bot from counting the same "Hitler" more than once
if not os.path.isfile("commentsWithHitler.txt"):
	hitlerIDs = []
else:
	with open("commentsWithHitler.txt","r") as f:
		hitlerIDs = f.read()
		hitlerIDs = hitlerIDs.split("\n")
		hitlerIDs = list(filter(None, hitlerIDs))


#Load our running total
if not os.path.isfile("stats.txt"):
	hitlerCount = 0
	recordHitler = 0
	commentCount = 0
else:
	with open("stats.txt","r") as f:
		stats = f.read()
		stats = stats.split("\n")
		stats = list(filter(None, stats))
	hitlerCount = int(stats[0])
	recordHitler = int(stats[1])
	commentCount = int(stats[2])


#if not os.path.isfile("recordHitler.txt"):
#	recordHitler = 0
#else:
#	with open("recordHitler.txt","r") as f:
#		recordHitler = int(f.read())





#The links to the comments with "Hitler" in them
links = []


#Construct the post title
now = datetime.datetime.now()
date = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
titleText = "Hitler Hunt for " + date


#Select subreddits
subreddit = reddit.subreddit('Justletmetest')
postSubreddit = reddit.subreddit('TheHitlerFallacy')

submissionsRead = 0
sessionCommentCount = 0
sessionHitlerCount = 0

print "Beginning Session for: "+ str(now.month) + "/" + str(now.day) + "/" + str(now.year) + " " + str(now.hour) + ":" + str(now.minute)

#Read all the posts from the last 24 hours
for submission in subreddit.top('week',limit=None):
	submissionsRead += 1
	print "---Sumbission "+str(submissionsRead)
	#The comment section on a Reddit post only shows the first few comments
	#The rest are not loaded until the user clicks the 'load more comments' link
	#The replace_more() function loads the comments hidden behind this link
	submission.comments.replace_more(limit=None)		
	print str(len(submission.comments.list()))
	sessionCommentCount += len(submission.comments.list())
	for comment in submission.comments.list():
		if re.search("hitler", comment.body, re.IGNORECASE):
			if comment.id not in hitlerIDs:
				#Construct the link, add it to the list, increment the hitler counter, save the comment ID
				l = "www.reddit.com" + comment.permalink
				print l
				links.append(l)
				sessionHitlerCount += 1
				hitlerIDs.append(comment.id)

hitlerCount += sessionHitlerCount
commentCount += sessionCommentCount

#Save the comments we found
with open("commentsWithHitler.txt","w") as f:
	for commentID in hitlerIDs:
		f.write(commentID + "\n")


#Track our day-to-day findings in a csv file
with open("TrackingHitler.csv","a") as f:
	f.write(date + "," + str(sessionHitlerCount) +  "\n")
 

#Begin constructing the bot's post
postText = "##I found " + str(sessionHitlerCount) + " Hitlers in r/Politics today.\n\n***\n\n"

#Check for a new record!
if sessionHitlerCount > recordHitler:
	postText += "\nDING DING DING! New Record!!\n\n***\n\n"
	recordHitler = sessionHitlerCount
elif sessionHitlerCount == recordHitler:
	postText += "\nWow, a tie for the record!\n\n***\n\n"


#Save the links and add them to the bot's post
with open("linksToHitler.txt","w") as f:
	for link in links:
		f.write(link + "\n")
		postText = postText + "\n^" + link + "\n"
if len(links) == 0:
	postText += "\nI have no links to share. I am sorry, friends.\n"


#Save the running total
with open("stats.txt","w") as f:
	f.write(str(hitlerCount)+"\n")
	f.write(str(recordHitler)+"\n")
	f.write(str(commentCount)+"\n")


#Finish the bot's post
postText += "\n\n***\n\nSieg Heil! I mean... Beep Boop, I am a robot.\n\nMy purpose is to find and link comments in r/Politics "
postText +="that contain the word 'Hitler'\n\nSince my birth, I have found a total of " + str(hitlerCount) + " Hitlers in r/Politics.\n\n"
postText +="Today, I read " + str(sessionCommentCount) + " comments. In total, I have read " + str(commentCount) + " comments."


#Submit the post to r/TheHitlerFallacy
#postSubreddit.submit(titleText, selftext = postText)

print postText

#Display ending notification
now = datetime.datetime.now()
print "Ending Session for: "+ str(now.month) + "/" + str(now.day) + "/" + str(now.year) + " " + str(now.hour) + ":" + str(now.minute)
