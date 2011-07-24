#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
import settings
from irc import IRCConnection
import twitter
import time
import urllib2
import HTMLParser

def main():
	irc = IRCConnection(settings.server, settings.nick, port = settings.port)
	irc.send('JOIN {0}'.format(settings.channel))

	crawlers = tuple()
	for search in settings.searchfor:
		crawler = twitter.Crawler(search)
		crawler.search()
		crawlers += (crawler,)

	parser = HTMLParser.HTMLParser()

	while True:
		for crawler in crawlers:
			results = crawler.search()

			for i in results:
				queryurl = settings.shortener.format('http://twitter.com/{0}/status/{1}'.format(i['from_user'], i['id_str']))
				response = urllib2.urlopen(queryurl)
				url = response.read()

				encoded = '\x02{0}\x02: {1} - {2}'.format(i['from_user'], parser.unescape(i['text']), url)
				irc.send('PRIVMSG {0} :{1}'.format(settings.channel, encoded))
				time.sleep(1)

		time.sleep(settings.searchevery)


if __name__ == '__main__':
	main()
