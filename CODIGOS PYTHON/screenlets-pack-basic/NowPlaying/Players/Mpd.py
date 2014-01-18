#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MpdApi 

import os
import sys
import string
import gobject
import commands
from GenericPlayer import GenericAPI
from mpd import (MPDClient, CommandError)
from socket import error as SocketError

class MpdAPI(GenericAPI):
	__name__ = 'MpdAPI'
	__version__ = '0.3.4.2'
	__author__ = 'Alexibaba, modified by BruceLee'
	__desc__ = 'MPD API to a Music Player'
	
	type = 'mpd'

	playerAPI = None

	__timeout = None
	__interval = 1

	callback_fn = None
	__curplaying = None
	__nowisplaying = True

	session_bus = False


	def __init__(self, session_bus):
		# Ignore the session_bus. Initialize a dcop connection
		GenericAPI.__init__(self, session_bus)


	# connect to MPD.
	def mpdConnect(self, client, con_id):
		try:
			client.connect(**con_id)
			return True
		except SocketError:
			return False

	# Authenticate at MPD
	def mpdAuth(self, client, secret):
		try:
			client.password(secret)
			return True
		except CommandError:
			return False

	def mpdServerConnect(self):
    ## MPD object instance
		try: 
			self.client = MPDClient()
		except: 
			print 'python-mpd not found'

		if self.mpdConnect(self.client, self.CON_ID) == True:
			try:
				self.client.status()
				#print 'Got connected!'
				return True
			except:
				if self.this_mpd_pw:
					if self.mpdAuth(self.client, self.this_mpd_pw) == True:
						try:
							self.client.status()
							#print 'Got connected!'
							return True
						except:
							#print 'No Connection! (Authentification failed)'
							return False
					else:
						#print 'Authentification failed! (wrong password)'
						return False
				else:
					#print 'No Password, but you need one!'
					return False
		else:
			#print 'No Connection!(No MPD_Server found)'
			return False


	# Check if the player is active : Returns Boolean
	# A handle to the dbus interface is passed in : doesn't need to be used
	# if there are other ways of checking this (like dcop in amarok)
	def is_active(self, dbus_iface, screenlet_settings):

		for i in range(1, 3):
			self.screenlet_settings = screenlet_settings
			self.this_mpd_host       = self.screenlet_settings['mpd_host_'+str(i)]
			self.this_mpd_port       = self.screenlet_settings['mpd_port_'+str(i)]
			self.this_mpd_pw         = self.screenlet_settings['mpd_pw_'+str(i)]
			self.this_mpd_music_path = self.screenlet_settings['mpd_music_path_'+str(i)]

			try:
				test = self.client.currentsong().get('title')
				if test and test != '':
					return True
					break
			except:
				self.CON_ID = {'host':self.this_mpd_host, 'port':self.this_mpd_port}
				try:
					if self.mpdServerConnect() == True:
						return True
						break
				except:
					continue
		else:
			return False

#			self.client.disconnect()


	# Make a connection to the Player
	def connect(self,screenlet_settings):
		pass

	
	# The following return Strings
	def get_title(self):
		return self.client.currentsong().get('title')
	
	def get_album(self):
		return self.client.currentsong().get('album')

	def get_artist(self):
		return self.client.currentsong().get('artist')
		
	def get_url(self):
		music_dir = os.path.expanduser(self.this_mpd_music_path)
		if music_dir != '':
			try:
				songurl = music_dir+self.client.currentsong().get('file')
				return songurl
			except:
				return ''
		else:
			return ''
	
	def get_url_dir(self):
		buff = self.get_url()
		for l,foo in enumerate(buff.split('/')): i=l; song=foo
		return buff.replace(song, '')

	def get_cover_path(self):
		cover_path = ''
		# Check the song folder for any PNG/JPG/JPEG image.
		tmp = self.get_cover_from_path(self.get_url_dir())
		if tmp: cover_path = tmp
		return cover_path

	# Returns Boolean
	def is_playing(self):
		#try:
		if self.client.status().get('state') == 'play' or self.client.status().get('state') == 'pause':
			return True
		else:
			return False
		#except:
		#	return False

	def is_paused(self):
		try:
			if self.client.status().get('state') == 'pause':
				return True
			else:
				return False
		except:
			return False

	# The following do not return any values
	def play_pause(self):
		if self.client.status().get('state') == 'stop':
			self.client.play()
		if self.client.status().get('state') == '':
			self.client.play()
		else:
			self.client.pause()

	def next(self):
		self.client.next()

	def previous(self):
		self.client.previous()


	def current_playing(self):
		return self.client.status().get('songid')

	def register_change_callback(self, fn):
		self.callback_fn = fn
		# Could not find a callback signal for Listen, so just calling after some time interval
		if self.__timeout:
			gobject.source_remove(self.__timeout)
		self.__timeout = gobject.timeout_add(self.__interval * 1000, self.info_changed)
		#self.playerAPI.connect_to_signal("playingUriChanged", self.info_changed)

	def info_changed(self, signal=None):
		# Only call the callback function if Data has changed
		if self.__timeout:
			gobject.source_remove(self.__timeout)
		try:
			if self.__curplaying != self.playerAPI.current_playing():
				self.__curplaying = self.playerAPI.current_playing()
				self.callback_fn()
			if self.__nowisplaying != self.playerAPI.is_playing():
				self.__nowisplaying = self.playerAPI.is_playing()
				#self.redraw_background_items()
			self.__timeout = gobject.timeout_add(self.__interval * 1000, self.info_changed)
		except:
			# The player exited ? call callback function
			self.callback_fn()
		self.__timeout = gobject.timeout_add(self.__interval * 1000, self.info_changed)



