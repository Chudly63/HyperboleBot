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
#			The bot writes to three .csv files. One tracks how many Hitlers were said each day,
#			one tracks whenever there is a new record number of hitlers, and the last tracks
#			who said Hitler and how many times they said it.
#
import praw
import pdb
import re
import os
import datetime
import csv

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


#Load our Stats
if not os.path.isfile("stats.txt"):
	hitlerCount = 0		#total number of hitlers found (all time)
	recordHitler = 0	#greatest number of hitlers found in one day
	commentCount = 0	#total comments read (all time)
	runCount = 1		#total number of program runs
else:
	with open("stats.txt","r") as f:
		stats = f.read()
		stats = stats.split("\n")
		stats = list(filter(None, stats))
	hitlerCount = int(stats[0])
	recordHitler = int(stats[1])
	commentCount = int(stats[2])
	runCount = int(stats[3]) + 1

#Redditors.csv lists redditors by name and the number of times they posted a comment on r/Politics with "Hitler"
if not os.path.isfile("Redditors.csv"):
	reds = []
else:
	r = csv.reader(open("Redditors.csv"))
	reds = [l for l in r]


#The title of posts in r/Politics and the links/quotes to comments that mention Hitler
postBody = ""

#Construct the post title
now = datetime.datetime.now()
date = str(now.month) + "/" + str(now.day) + "/" + str(now.year)
titleText = "Hitler Hunt for " + date


#Subreddits for running ::  MAKE SURE YOU UPDATE SUBMISSION LOOP WHEN CHANGING
subreddit = reddit.subreddit('Politics')
postSubreddit = reddit.subreddit('TheHitlerFallacy')

#Subreddits for testing :: MAKE SURE YOU UPDATE SUBMISSION LOOP WHEN CHANGING
#subreddit = reddit.subreddit('Justletmetest')
#postSubreddit = reddit.subreddit('Justletmetest')

submissionsRead = 0		#Submissions read this session (not saved)
sessionCommentCount = 0		#Comments read this session
sessionHitlerCount = 0		#Hitlers found this session


#Print starting message for debugging
print "Beginning Session for: "+ str(now.month) + "/" + str(now.day) + "/" + str(now.year) + " " + str(now.hour) + ":" + str(now.minute)

maxSizeReached = False		#Reddit posts can only be 40000 characters. Almost every post will be under this limit, but if this is left unchecked, there is a chance the bot will be unable to post


submissionIDs = []
#Read all the posts from the last 24 hours
for submission in subreddit.top('day',limit=None):
	if submission.id not in submissionIDs:
		submissionIDs.append(submission.id)
		hitlerFound = False	#Did we find a comment with "Hitler"?
		quotes = []		#Quotes of comments that have "Hitler"
		submissionsRead += 1
		print "---Sumbission "+str(submissionsRead)	#Useful for debugging
	
		#The comment section on a Reddit post only shows the first few comments
		#The rest are not loaded until the user clicks the 'load more comments' link
		#The replace_more() function loads the comments hidden behind this link
		submission.comments.replace_more(limit=None)	#Loads all comments in the submission
		sessionCommentCount += len(submission.comments.list())
		for comment in submission.comments.list():
			if re.search("hitler", comment.body, re.IGNORECASE):
				if comment.id not in hitlerIDs:
					body = comment.body
				
					#Find the sentence with "Hitler" in it, quote it, format it to a reddit hyperlink, and add the author
					y = re.split("(\.|\?|\!|\n)",body)
					x = [sentence for sentence in y if 'hitler' in sentence.lower()]
					target = x[0].replace("\n","") 		#Target becomes the sentence in the comment containing the word Hitler
					target = target.replace('"','')		#Remove double quotes
					target = target.replace('[','\[')	#Escape square brackets for Reddit's formatting
					target = target.replace(']','\]') 	
					target = target.replace('>','') 	#Remove '>' : This symbol is used on Reddit to symbolize quotes, so it appears often.
					target = target.replace('  ',' ') 	#Remove extra spaces between words.
					while target[:1] == " " :		
						target = target[1:]		#Remove the first character of the quote if it is blank
					target = target[:1].upper() + target[1:]#Capitalize the first letter
					isLink = (target[:4] == "Com/" or target[:4] == "Org/" or target[:4] == "Net/" or target[:4] == "Gov/") #Makes sure the quote is not a hidden link
					if target not in quotes and not isLink:	#Checks to see if someone is quoting a different comment in the same thread. Quoting a Hiler does not qualify as another Hitler	
						if not hitlerFound and not maxSizeReached: 
							postBody += '\n#####' + submission.title + '\n'
							hitlerFound = True
						#Construct the quote, increment the hitler counter, save the comment ID, update Redditors.csv
						l = "https://www.reddit.com" + comment.permalink
						print l		#For debugging
						sessionHitlerCount += 1
						hitlerIDs.append(comment.id)
						
						#Update the Redditors csv
						author = comment.author
						noted = False	#Becomes true if the author is already in the csv
						for i in range(len(reds)):
							if reds[i][0] == author:
								n = int(reds[i][1]) + 1
								reds[i][1] = str(n)
								noted = True
						if not noted:	#True if this is the first time this author was 'caught' saying "Hitler"
							reds.append([author,"1"])
		
						#A reddit link is formatted as such: [*Quote*](*Link*) | Author. This will display the quote as a link to *Link*
						if not maxSizeReached:
							postBody += '\n- ["' + target + '."](' + l + ') - ' + str(comment.author) + '\n'
						if len(postBody) >= 38000:	#Maximum post size is 40,000 characters. Stopping at 38,000 leaves room for heading and stats
							maxSizeReached = True
						quotes.append(target)
	
	
#Calculate new totals
hitlerCount += sessionHitlerCount
commentCount += sessionCommentCount	

if maxSizeReached:
	postBody += "\n#Das ist schlecht! I've reached my limit! Some links may be missing from this post.\n"

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
	with open("RecordHistory.csv","a") as f:
		f.write(date + "," + str(recordHitler) + "\n")
elif sessionHitlerCount == recordHitler:
	postText += "\nWow, a tie for the record!\n\n***\n\n"


#Add links to the post
if sessionHitlerCount == 0:
	postBody = "I have no links to share. I am sorry, friends.\n"
postText += postBody


#Save the running total
with open("stats.txt","w") as f:
	f.write(str(hitlerCount)+"\n")
	f.write(str(recordHitler)+"\n")
	f.write(str(commentCount)+"\n")
	f.write(str(runCount)+"\n")

#Save redditors
w = csv.writer(open("Redditors.csv","w"))
w.writerows(reds)


averageHitlers = hitlerCount/runCount


#Finish the bot's post
postText += "\n\n***\n\nSieg Heil! I mean... Beep Boop, I am a robot.\n\nMy purpose is to find and link comments in r/Politics "
postText += "that contain the word 'Hitler'\n\nSince my birth, I have found a total of " + str(hitlerCount) + " Hitlers in r/Politics. "
postText += "On average, I found " + str(averageHitlers) + " Hitlers per day.\n\n"
postText += "Today, I read " + str(sessionCommentCount) + " comments. In total, I have read " + str(commentCount) + " comments."
postText += "\n\n\n\n#I am in my second phase of testing. I am not perfect. I am sorry. I love you."


#Submit the post to r/TheHitlerFallacy
postSubreddit.submit(titleText, selftext = postText)

#For testing
#print postText

#Display ending notification for debugging
now = datetime.datetime.now()
print "Ending Session for: "+ str(now.month) + "/" + str(now.day) + "/" + str(now.year) + " " + str(now.hour) + ":" + str(now.minute)
