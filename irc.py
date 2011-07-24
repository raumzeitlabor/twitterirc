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

import socket
import threading
import time

class IRCConnection:
	def send(self, cmd):
		#cmd = '{0}\n'.format(cmd.encode('ascii','replace'))
		cmd = '{0}\n'.format(cmd.encode("UTF-8"))
		self.socket.send(cmd)
		print('>>> {0}'.format(cmd))

	def receive(self):
		while True:
			data = self.socket.recv(1024)
			print('<<< {0}'.format(data))

			data = data.rstrip()
			data = data.split(' ')

			if(data[0].lower() == 'ping'):
				self.send('PONG {0}'.format(data[1]))

			time.sleep(1)

	def __init__(self, server, nick, port = 6667, user = None, realname = None, passwd = None):
		if(user == None):
			user = nick

		if(realname == None):
			realname = nick

		if(passwd == None):
			passwd = 'dummy'

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((server, port))

		receiveThread = threading.Thread(target=self.receive)
		receiveThread.start()

		self.send('PASS {0}'.format(passwd))
		self.send('NICK {0}'.format(nick))
		self.send('USER {0} dummy dummy :{1}'.format(user, realname))

		time.sleep(1)
