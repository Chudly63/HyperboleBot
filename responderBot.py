#!/usr/bin/python

import praw
import os
import datetime
import time


r = praw.Reddit('bot2')

if not os.path.isfile("links.txt"):
	links = []
else:
	with open("links.txt","r") as f:
		links = f.read()
		links = links.split("\n")
		links = list(filter(None, links))

while len(links) > 0 and not (datetime.datetime.now().hour == 23 and datetime.datetime.now().minute > 30): #Keep responding until we run out of comments or until the HitlerBot is about to run again
	
	posted = False
	while not posted:
		try:
			reply = "Hello there! I noticed you mentioned 'Hitler' in your comment. This comment has been linked in r/TheHitlerFallacy\n\n"
			reply += "***\n\n^(Beep Boop ~ I am a robot. My purpose is to find and link comments in r/Politics that mention Hitler.)\n\n"
			reply += "^(Have a nice day! I love you <3)"
			l = links[0]
			print l
			s=r.comment(l)
			s.reply(reply)
			links.pop(0)

			with open("links.txt","w") as f:
				for l in links:
					f.write(l+"\n")

			posted = True
		except APIException as err:
			print err
			time.sleep(300)	


with open("links.txt","w") as f:
	for l in links:
		f.write(l+"\n")


