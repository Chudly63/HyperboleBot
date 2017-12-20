#!/usr/bin/python
#
#Alex M Brown
#12/20/2017
#
#hitlerBot.py - Navigates r/MarchAgainstTrump and keeps tracks of how many times people mention Hitler
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
if not os.path.isfile("comments_read.txt"):
	comments_read = []
else:
	with open("comments_read.txt","r") as f:
		comments_read = f.read()
		comments_read = comments_read.split("\n")
		comments_read = list(filter(None, comments_read))


subreddit = reddit.subreddit('Justletmetest') #Selecting our subreddit

for submission in subreddit.hot(limit=1): 			#Get the posts from that subreddit
	
	#The comment section on a Reddit post only shows the first few comments
	#The rest are not loaded until the user clicks the 'load more comments' link
	#The replace_more() function loads the comments hidden behind this link
	submission.comments.replace_more(limit=None)		

	
	for comment in submission.comments.list():
		if comment.id not in comments_read:
			if re.search("bot", comment.body, re.IGNORECASE):
				print(comment.body)
				comments_read.append(comment.id)

with open("comments_read.txt","w") as f:
	for comment_id in comments_read:
		f.write(comment_id + "\n")
