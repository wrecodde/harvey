# a python powered, web based music player

import os
import re
import hashlib
import threading
import logging

logging.basicConfig(
    level = logging.DEBUG,
    format = "%(asctime)s | %(levelname)s | %(message)s",
)

# logging switch
logging.disable(logging.DEBUG)

# todo:
	# read info off the  music file

class Track():
	"""
	define attributes related to a track
	[currently materialised from the filename]
	"""
	
	def __init__(self, filepath):
		self.filename = os.path.basename(filepath)
		
		stack = self.build(self.filename)
		features = stack.get("feat")
		
		self.title = stack.get("title")
		self.artist = stack.get("artist")
		self.feat = features if features else "None"
		
		self.uri = self.get_hash()
		self.url = os.path.abspath(filepath)
		
		self.track = True if self.title and self.artist else False
	
	def __repr__(self):
		return f"{self.title} by {self.artist}"
	
	def get_hash(self):
		filename = self.filename
		hash = hashlib.md5(filename.encode()).hexdigest()
		return hash[:16]
	
	def build(self, filename):
		"""
		uses regex to extract primary info from a given filename
		:: artist, title, features/single ..for now
		"""
		
		def extract(filename):
			# a really delicate contraption
			# tested, trusted and proven true, but delicate
			try:
				form = re.compile(r"(.+) -- (.+)") # written norm
				mo = re.match(form, filename)
				
				artist = mo.group(1)
				title = mo.group(2).partition('.')[0] # assuming there's an extension
				feat = []
				
				if 'ft.' in mo.group(2): # then, this is not a single
					ftform = re.compile(r"(.+) ft. (.+)")
					mo2 = re.match(ftform, mo.group(2))
					
					title = mo2.group(1)
					feat = mo2.group(2).partition('.')[0].split(', ')
				
				logging.debug(f"successfully parsed {filename}")
				return artist, title, ", ".join(feat)
				
			except: # catch any error at all, take no chances.
				logging.debug(f"could not parse {filename}")
				return '', '', [] # let 'em have those blanks. safe!
		
		artist, title, feat = extract(filename)
		return {"artist":artist, "title":title, "feat":feat}

def run_scan(target_dir="/sdcard", save=False):
	"""
	do a targeted or system wide scan of the device
	for music files
	"""
	file_formats =[".mp3", ".m4a"]
	ignore = ["data", "Android", "codde", "ProgramData", "code"]
	
	saved = []
	
	def walk_dir(dir="/"):
		for dirname, subdirs, files in os.walk(dir, topdown=True):
			if files:
				for file in files:
					ext = os.path.splitext(file)[-1]
					if ext in file_formats:
						file_path = os.path.join(dirname, file)
						music_files.append(file_path)
						if save:
							saved.append(file_path)
			for dir in subdirs:
				if dir:
					if dir.startswith(".") or dir in ignore:
						subdirs.remove(dir)
				for dir in subdirs:
					walk_dir(dir)
	
	logging.info(f"walking {target_dir}")
	walk_dir(target_dir)
	logging.info("walk finished")
	
	if save:
		return saved
	else:
		return

music_files = []
run_scan('/sdcard/music')

class Library():
	def __init__(self):
		self.track_shelf = self.stack_tracks()
		self.tracks = self.get_track('all')
		
		self.artist_shelf = self.stack_artists()
		self.artists = self.get_artist('all')
	
	def stack_tracks(self):
		files = music_files
		shelf = {}
		
		for filepath in files:
			track = Track(filepath)
			shelf[track.uri] = track
		
		return shelf
	
	def stack_artists(self):
		tracks = self.tracks
		shelf = {}
		
		for track in tracks:
			track_list = shelf.get(track.artist, [])
			track_list.append(track)
			shelf[track.artist] = track_list
		
		return shelf
	
	def get_track(self, target='all'):
		
		if target == 'all':
			return list(self.track_shelf.values())
		else:
			return self.track_shelf.get(target)
	
	def get_artist(self, target='all'):
		
		if target == 'all':
			return list(self.artist_shelf.keys())
		else:
			return self.artist_shelf.get(target.title())

lib = Library()
