#!/usr/bin/python
#
#Alex M Brown
#12/20/2017
#
#hitlerBot.py - Navigates r/politics and keeps tracks of how many times people mention Hitler
#		This program runs every 24 hours at 11:50 EST
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
if not os.path.isfile("numHitler.txt"):
	hitlerCount = 0
else:
	with open("numHitler.txt","r") as f:
		hitlerCount = int(f.read())

sessionHitlerCount = 0

#if not os.path.isfile("linksToHitler.txt"):
#	links = []
#else:
#	with open("linksToHitler.txt","r") as f:
#		links = f.read()
#		links = links.split("\n")
#		links = list(filter(None, links))

#The links to the comments with "Hitler" in them
links = []

#Construct the post title
now = datetime.datetime.now()
date = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
titleText = "Hitler Hunt for " + date

#Select subreddits
subreddit = reddit.subreddit('politics')
postSubreddit = reddit.subreddit('TheHitlerFallacy')

#Read all the posts from the last 24 hours
for submission in subreddit.top('day',limit=None):
	print submission.title 
	#The comment section on a Reddit post only shows the first few comments
	#The rest are not loaded until the user clicks the 'load more comments' link
	#The replace_more() function loads the comments hidden behind this link
	submission.comments.replace_more(limit=None)		

	for comment in submission.comments.list():
		if re.search("hitler", comment.body, re.IGNORECASE):
			if comment.id not in hitlerIDs:
				#Construct the link, add it to the list, increment the hitler counter, save the comment ID
				l = "www.reddit.com" + comment.permalink
				print l
				links.append(l)
				hitlerCount = hitlerCount+1
				sessionHitlerCount = sessionHitlerCount+1
				hitlerIDs.append(comment.id)

#Save the comments we found
with open("commentsWithHitler.txt","w") as f:
	for commentID in hitlerIDs:
		f.write(commentID + "\n")

#Save the running total
with open("numHitler.txt","w") as f:
	f.write(str(hitlerCount)+"\n")

#Track our day-to-day findings in a csv file
with open("TrackingHitler.csv","a") as f:
	f.write(date + "," + str(sessionHitlerCount) +  "\n")
 

#Begin constructing the bot's post
postText = "I found " + str(sessionHitlerCount) + " Hitlers in r/Politics today.\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"


#Save the links and add them to the bot's post
with open("linksToHitler.txt","w") as f:
	for link in links:
		f.write(link + "\n")
		postText = postText + "\n" + link + "\n"

#Finish the bot's post
postText = postText + "\n\n\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nSeig Heil! I mean... Beep Boop, I am a robot.\n\nMy purpose is to find and link comments in r/politics."
postText = postText + "\n\nSince my birth, I have found a total of " + str(hitlerCount) + " Hitlers in r/politics."

#Submit the post to r/TheHitlerFallacy
postSubreddit.submit(titleText, selftext = postText)
