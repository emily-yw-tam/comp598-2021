# HW1

It turns out that our approach isn’t counting tweets properly … meaning that some tweets are getting counted more than once.  Go through and look at your annotated data.  Identify where the counting problem is coming from.

**In 3 sentences or less, explain where the counting problem is coming from.**

Some tweets are getting counted more than once because our code does not account for whether a tweet is a retweet or not.  As a result, the number of tweets that mention Trump (and thus the percent of tweets that mention Trump) is higher than it should be.
