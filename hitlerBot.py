#!/usr/bin/python
#
#Alex M Brown
#12/20/2017
#
#hitlerBot.py - Navigates r/politics and keeps tracks of how many times people mention Hitler
#		The first iteration will simply count the number of "Hitler"s on the front page.
#		I would like to later have the bot track the number of "Hitler"s by date.
#
#
#
import praw
import pdb
import re
import os

#Create a reddit instance using the config settings stored in praw.ini
reddit = praw.Reddit('bot1')

#comments_read.txt stores the ID of comments that have already been read by the bot. This keeps the bot from counting the same "Hitler" more than once
if not os.path.isfile("commentsRead.txt"):
	commentsRead = []
else:
	with open("commentsRead.txt","r") as f:
		commentsRead = f.read()
		commentsRead = commentsRead.split("\n")
		commentsRead = list(filter(None, commentsRead))

if not os.path.isfile("numHitler.txt"):
	hitlerCount = 0
else:
	with open("numHitler.txt","r") as f:
		hitlerCount = int(f.read())


subreddit = reddit.subreddit('politics') #Selecting our subreddit

for submission in subreddit.hot(limit=10): 			#Get the posts from that subreddit
	
	#The comment section on a Reddit post only shows the first few comments
	#The rest are not loaded until the user clicks the 'load more comments' link
	#The replace_more() function loads the comments hidden behind this link
	submission.comments.replace_more(limit=None)		

	
	for comment in submission.comments.list():
		if comment.id not in commentsRead:
			if re.search("hitler", comment.body, re.IGNORECASE):
				print(comment.body)
				hitlerCount = hitlerCount+1
			commentsRead.append(comment.id)

with open("commentsRead.txt","w") as f:
	for commentID in commentsRead:
		f.write(commentID + "\n")

with open("numHitler.txt","w") as f:
	f.write(str(hitlerCount)+"\n")
