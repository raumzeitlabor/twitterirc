#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2011 Lukas Martini <lukas.martini@unionhost.de>

# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.

# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:

# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software. If you use this software
# in a product, an acknowledgment in the product documentation would be
# appreciated but is not required.

# 2. Altered source versions must be plainly marked as such, and must not be
# misrepresented as being the original software.

# 3. This notice may not be removed or altered from any source
# distribution.

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
