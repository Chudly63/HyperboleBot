Reddit Hyperbole Bot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
www.reddit.com/u/HitlerFallacyBot
www.reddit.com/r/TheHitlerFallacy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This bot keeps track of how many times someone mentions Hitler on r/Politics

This project is meant to give me more practice with praw (Python Reddit API Wrapper)

This bot works by reading all of the comments on all of the posts in the top section of r/Politics for the last 24 hours.
Whenever the bot finds a comment with "Hitler" in it, it saves the link and the ID of that comment.
After it finishes reading all the comments for the day, it creates a reddit post on r/TheHitlerFallacy with all the links to the comments it found.

The bot keeps a running total of all the "Hitler"s it finds on r/Politics and posts this total with the links.
It also writes each day's total to a csv file along with the date. I plan on using this file to create some pretty graphs after letting this bot run for a while.

The biggest problem with the current version of the bot is that it does not read comments that were posted on posts older than 24 hours.
If someone were to post a comment with "Hitler" in it on a post that was more than a day old, the bot would not find it.



Future Plans:
	+Be able to read comments on older posts that were posted in the last 24 hours
	+Optimization: Current program takes a long time to process large threads. New to praw so this may be too difficult/impossible
	+Rasberry Pi integration
