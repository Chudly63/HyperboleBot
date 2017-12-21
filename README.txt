Reddit Hyperbole Bot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This bot keeps track of how many times someone mentions Hitler on r/Politics

This project is meant to give me more practice with praw (Pyton Reddit API Wrapper)

The bot stores the ID's of the comments that have Hitler in them and produces a list of links to these comments.

I'm thinking about having this script run every day and produce a reddit post linking to all the "Hitler"s that were posted that day. Might be too much though considering how much
is posted to r/politics

I have this script run through every post in the top section for the last 24 hours. This lets me see everything that was posted that day.
However, this method misses all comments posted that day on posts that were more than 24 hours old. 

After the bot runs, it posts all of the links to the comments it found on r/TheHitlerFallacy

Future Plans:
	+Be able to read comments on older posts that were posted in the last 24 hours
	+Optimization: Current program takes a long time to process large threads. New to praw so this may be too difficult/impossible
