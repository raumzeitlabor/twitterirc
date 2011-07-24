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

import httplib
import json
import socket
import time
import urllib

SEARCH_HOST="search.twitter.com"
SEARCH_PATH="/search.json"

class Crawler(object):
	''' Crawl twitter search API for matches to specified tag.  Use since_id to
	hopefully not submit the same message twice.  '''

	def __init__(self, tag, max_id = None):
		self.max_id = max_id
		self.tag = tag
        
	def search(self):
		c = httplib.HTTPConnection(SEARCH_HOST)
		params = {'q' : self.tag}

		if self.max_id is not None:
			params['since_id'] = self.max_id

		path = "%s?%s" %(SEARCH_PATH, urllib.urlencode(params))

		try:
			c.request('GET', path)
			r = c.getresponse()
			data = r.read()
			c.close()

			try:
				result = json.loads(data)
			except ValueError:
				return None

			if 'results' not in result:
				return None

			self.max_id = result['max_id']
			return result['results']

		except (httplib.HTTPException, socket.error, socket.timeout), e:
			logging.error("search() error: %s" %(e))
			return None
