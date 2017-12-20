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

#commentsWithHitler.txt stores the ID of comments that have "Hitler" and have already been read by the bot.
# This keeps the bot from counting the same "Hitler" more than once
if not os.path.isfile("commentsWithHitler.txt"):
	hitlerIDs = []
else:
	with open("commentsWithHitler.txt","r") as f:
		hitlerIDs = f.read()
		hitlerIDs = hitlerIDs.split("\n")
		hitlerIDs = list(filter(None, hitlerIDs))


if not os.path.isfile("numHitler.txt"):
	hitlerCount = 0
else:
	with open("numHitler.txt","r") as f:
		hitlerCount = int(f.read())


if not os.path.isfile("linksToHitler.txt"):
	links = []
else:
	with open("linksToHitler.txt","r") as f:
		links = f.read()
		links = links.split("\n")
		links = list(filter(None, links))


subreddit = reddit.subreddit('politics') #Selecting our subreddit
postSubreddit = reddit.subreddit('TheHitlerFallacy')

print("READY FOR HITLERS")
for submission in subreddit.top('day',limit=1): 			#Get the posts from that subreddit
	print submission.title 
	#The comment section on a Reddit post only shows the first few comments
	#The rest are not loaded until the user clicks the 'load more comments' link
	#The replace_more() function loads the comments hidden behind this link
	submission.comments.replace_more(limit=None)		

	for comment in submission.comments.list():
		if re.search("hitler", comment.body, re.IGNORECASE):
			if comment.id not in hitlerIDs:
				l = "www.reddit.com" + comment.permalink
				print l
				links.append(l)
				hitlerCount = hitlerCount+1
				hitlerIDs.append(comment.id)

with open("commentsWithHitler.txt","w") as f:
	for commentID in hitlerIDs:
		f.write(commentID + "\n")

with open("numHitler.txt","w") as f:
	f.write(str(hitlerCount)+"\n")


postText = "I found " + str(hitlerCount) + " Hitlers in r/Politics today.\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"


with open("linksToHitler.txt","w") as f:
	for link in links:
		f.write(link + "\n")
		postText = postText + "\n" + link
postSubreddit.submit('Today', selftext = postText)
