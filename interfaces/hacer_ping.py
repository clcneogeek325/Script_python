#!/usr/bin/env python
#-*- coding:utf-8 -*-

import ping, socket

try:
	ping.verbose_ping('www.google.com')
	delay = ping.Ping('www.wikipedia.org', timeout=2000).do()
except socket.error, e:
	print "Ping Error:", e
