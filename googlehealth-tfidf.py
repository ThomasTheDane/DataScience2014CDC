# 4/19/2014
# Charles O. Goddard

import feedparser
import google

import tfidf_search


rss_url = "http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&topic=m&output=rss"
feed = feedparser.parse(rss_url)

for item in feed.entries:
    print '-'*80
    title, source = item.title.split(' - ')
    searchstring = tfidf_search.striptext(title + item.description)
    print title
    for score, url in tfidf_search.search(searchstring):
        print score, ':', url
        break
    else:
        print 'No relevant URLs'
    print
