Reddit Hyperbole Bot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This bot keeps track of how many times someone mentions Hitler on r/Politics

This project is meant to give me more practice with praw (Pyton Reddit API Wrapper)

The bot stores the ID's of the comments that have Hitler in them and produces a list of links to these comments.

I'm thinking about having this script run every day and produce a reddit post linking to all the "Hitler"s that were posted that day. Might be too much though considering how much
is posted to r/politics

Currently, the script only runs on the first post in the "hot" section of r/politics

Future Plans:
	+Search all posts in r/politics in the last 24 hours
	+Create a reddit post with all the links from the last 24 hours
	+Keep a running total and a daily total of "Hitler"s
	+Optimization: Current program takes a long time to process large threads. New to praw so this may be too difficult/impossible
