#! /data/data/com.termux/files/usr/bin/python

import tornado.ioloop
import tornado.web

import os
import random
import sqlite3 as sql
import secrets
import logging

import box

# logging config
logging.basicConfig(
    level=logging.DEBUG,
    format = "%(asctime)s | %(levelname)s | %(message)s"
)

# logging switch
# logging.disable(logging.DEBUG)

logging.info("dependencies imported")
logging.info("configuring settings")
logging.info("setting up handlers")

# database config
db = sql.connect("disk.db")
cu = db.cursor()

# cookie secret
token = secrets.token_hex(5)

# app handlers
class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("user")

class MainPage(BaseHandler):
	def get(self):
		shuffle = random.sample(box.lib.tracks, 7)
		self.render("index.html", tracks=shuffle)

class StreamHandler(BaseHandler):
	def get(self, uri):
		"""stream the track with the requested uri"""
		
		path = box.lib.get_track(uri).url
		self.redirect(f"/source/{path}")

class TracksHandler(BaseHandler):
	def get(self):
		tracks = box.lib.tracks
		self.render('index.html', tracks=tracks)

class TrackHandler(BaseHandler):
	def get(self, uri):
		track = box.lib.get_track(uri)
		self.render("track.html", track=track)

handlers = [
	(r"^/", MainPage),
	(r"^/source/(.*)", tornado.web.StaticFileHandler, {"path":"/"}),
	(r"^/play/(.*)", StreamHandler),
	(r"^/tracks", TracksHandler),
	(r"^/tracks/(.*)", TrackHandler),
]

settings = dict(
	debug = True,
	static_path = os.path.join(os.path.dirname(__file__), "assets"),
	template_path = os.path.join(os.path.dirname(__file__), "pages"),
	cookie_secret = token,
	)

# music app
app=tornado.web.Application(
	handlers = handlers,
	default_host = "localhost",
	**settings,
)

try:
	logging.info("starting application")
	logging.info("listening on port 8080")
	app.listen(8080)
	tornado.ioloop.IOLoop.current().start()
except:
	print ("\nshutting down!")
	import sys
	sys.exit()
