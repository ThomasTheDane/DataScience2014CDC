# 3/28/2014
# Charles O. Goddard

import feedparser
import google

rss_url = "http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&topic=m&output=rss"
feed = feedparser.parse(rss_url)

for item in feed.entries:
	print '-'*80
	title, source = item.title.split(' - ')
	print title
	for url in google.search("site:cdc.gov " + title, stop=3):
		print url
		break
	else:
		print 'No relevant URLs'
	print
