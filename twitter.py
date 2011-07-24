# coding: utf-8

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
