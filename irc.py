# coding: utf-8

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
