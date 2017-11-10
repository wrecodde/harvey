# i dont really want to trash and forget functions i wrote already

# todo list
	# model music object --done
	# playlists creation and editing --done
	# file organization; selection, sorting and searching
	

# -- id345.edit('year':'2016', 'album':'night owls')
# -- id345.name >> 'track by artist single/ft featlist

## ==== archives ====

def shelf():
	# write a dict table of identified tracks against serial ids
	
	with open('files') as f: # source objects: filenames from source file
		cf=list(f.read().split('\n'))
		cf.remove('')

	for c in cf:
		temp[cf.index(c)]=makemusic(c)
	lib["all"]=temp; lib.close()
	
def fileit():
	# write the contents of the fileslist in memory to an ext file
	# or write the contents of -the- ext file to memory

	global files
	if files == []:
		f=open('files', 'r')
		files=list(f.read().split('\n'))
		f.close()

	if files != []:
		f=open('files', 'w')
		for file in files:
			#print(file)
			f.write(file.lower()+'\n')


def fit(word, length):
	return word if len(word)<length else word[:length-3]+"..."

	# usage
	"""
	print ("ID".rjust(3)+"|"+"Artist".rjust(27)+"|"+"Song".rjust(30))
	for t in music.temp:
		print (str(t).rjust(3)+"|",
		fit(music.temp[t]["artist"],27).rjust(27,"-")+"|",
		fit(music.temp[t]["title"],30).rjust(30,"-"))
	"""

def buildlist(src, attrib):
	# make a list of tracks according to given attibutes	
	# deprecated now. middle() now works for it

	FILES = src	# a list of filenames to work with
	FLIP = {} 	# a temp dict of ids against music objects
	LIST = [] 	# what we're building
	
	for file in FILES:
		FLIP[FILES.index(file)]=makemusic(file)
	
	#LIST.append(FLIP.get(id)[attrib])
	
	LIST.sort()
	return LIST

class Car():
	def __init__(self, make, model, year):
		self.make=make
		self.model=model
		self.year=year
		
		self.fullname=self.getname()
	
	def getname(self):
		return ((self.make+" "+self.model+" "+str(self.year)).title())
		
		
class ElectricCar(Car):
	def __init__(self, make, model, year):
		super().__init__(make, model, year)
		self.batterysize = 0
		
	def battery(self):
		print (self.getname() +" has about "+ str(self.batterysize) + "KWh of battery power.")


friday=Car("Rolls Royce", "Bespoke", 2017)
apollo=ElectricCar("Tesla", "Model 3", 2015)


# Knuth-Morris-Pratt string matching
# David Eppstein, UC Irvine, 1 Mar 2002

#from http://code.activestate.com/recipes/117214/
def KnuthMorrisPratt(text, pattern):

    '''Yields all starting positions of copies of the pattern in the text.
Calling conventions are similar to string.find, but its arguments can be
lists or iterators, not just strings, it returns all matches, not just
the first one, and it does not need the whole text in memory at once.
Whenever it yields, it will have read the text exactly up to and including
the match that caused the yield.'''

    # allow indexing into pattern and protect against change during yield
    pattern = list(pattern)

    # build table of shift amounts
    shifts = [1] * (len(pattern) + 1)
    shift = 1
    for pos in range(len(pattern)):
        while shift <= pos and pattern[pos] != pattern[pos-shift]:
            shift += shifts[pos-shift]
        shifts[pos+1] = shift

    # do the actual search
    startPos = 0
    matchLen = 0
    for c in text:
        while matchLen == len(pattern) or \
              matchLen >= 0 and pattern[matchLen] != c:
            startPos += shifts[matchLen]
            matchLen -= shifts[matchLen]
        matchLen += 1
        if matchLen == len(pattern):
            yield startPos
            
kmp=KnuthMorrisPratt

# ================= #
# the old bank system...

#! some/arbitrary/path topython

# data objects: files[], disk[], tracks{}, artists[]
# what this script contains:
	# a music class
	# a walker function
	# a musicmaker function
	# and several lines of code that build data
		# to work with
	# .. 

import os, re
files=[]
sdata=[]

class Music():
	"""
	==building blocks==
	
	the class simply defines how a music
	object should look like
	"""
	def __init__(self, raw, path):
		self.name=raw
		raw=makemusic(raw)
		
		self.track=raw["title"]
		self.artist=raw["artist"]
		self.feat=raw["feat"] if raw["feat"]!=[] else "single"
		
		self.path=path

def walk(dir='./.media'):
	"""
	given a directory (the music folder on my phone),
	create a list of all the file types matching a specific format
	artist -- tracktitle [ft. featuring]
	"""
		
	def primary():
		"""
		the first and still primary way it goes
		"""
		ls = os.listdir(dir)
		for name in ls:
			path = dir+'/'+name
			
			if os.path.isdir(path):
				# enter and continue walking
				walk(path)
				
			elif os.path.isfile(path) and re.match(re.compile(r"(.+) -- (.+)"), name)!=None:
				# only take cognizance of file objects,
				# esp if they match predfined formats
				files.append(name.lower())
				sdata.append((name.lower(), path))
	
	def secondary():
		"""
		when testing away from my phone, dir never exists
		so...
		"""
		# open the file 'files' and read from it
		global files
		f=open('files', 'r')
		files=list(f.read().split('\n'))
	
	# check if we're working from home or not
	if os.path.exists(dir):
		primary()
	elif not os.path.exists(dir):
		secondary()

def makemusic(file):
	"""
	simply lift the info; artist, tracktitle, and features
	from a filename in a given format: artist -- tracktitle [ft. featuring]
	where -features- are optional
	"""
	def extract(file):
		# a weak, wiry contraption
		# extract info from the filename
		try:
			form = re.compile(r"(.+) -- (.+)") #the key to it all
			mo = re.match(form, file)
			
			artist = mo.group(1)
			title  = mo.group(2).partition('.')[0] #assuming there's an extension attached
			feat   = []
			
			if 'ft.' in mo.group(2): #if this is not a single, get a list of featured artists
				ftform = re.compile(r"(.+) ft. (.+)")
				mo2    = re.match(ftform, mo.group(2))
				
				title  = mo2.group(1)
				feat   = mo2.group(2).partition('.')[0].split(', ') #not contingency safe though
				
			return artist, title, feat
			
		except: #catch any error at all
			# and return blanks
			return '', '', []
	
	xtract = extract(file)
	music={'artist':xtract[0], 'title':xtract[1], 'feat':xtract[2]}
	
	return music

def middle(point):
	# i simply couldnt come up with a more fitting name

	house=[]
	for f in files:
		house.append(makemusic(f)[point])
	return house

# perform the walking operation
walk()

# make music objects of every music file
# make a list of artists
# sort tracks by artist
disk=[]
opfl=open("files", "w")

for file in sdata:
	disk.append(Music(file[0], file[1]))
	opfl.write(file[0]+"=>"+file[1]+"\n")

artists=list(set(middle('artist')))
tracks={}
tracks['all']=middle('title')

for artist in artists:
	tracks[artist]=[]

for trk in disk:
	artist=trk.artist
	lhist=tracks.get(artist)
	lhist.append(trk.track)


# =================== #
# renaming folders doesnt work like i want it to
# so im scraping it

import os, shutil

rootdir = "/sdcard/code/music-app/raw-code/bunker/tests/testdir"
def renamefolders():
	"""
	make sure every artist has a folder
	"""
	# data definitions
	global dirs, files
	dirs, files = [], []
	
	def observe():
		try:
			classlist = os.listdir()
			for item in classlist:
				if os.path.isdir(item) and not item.startswith("."):
					dirs.append(item)
				elif os.path.isfile(item):
					files.append(item)
			print ("\tfolders and files identified")
		except:
			print ("something went wrong during observation. exiting")
			import sys; sys.exit()
	
	def rename():
		try:
			while files:
				file=files[0]
				artistname = file.split(" -- ")[0].lower()
				if artistname in dirs:
					shutil.move(file, artistname)
					files.remove(file)
				elif artistname not in dirs:
					os.mkdir(artistname)
					dirs.append(artistname)
					shutil.move(file, artistname)
					files.remove(file)
			print ("\trenaming complete")
		except:
			print ("something went wrong while renaming. exiting")
			import sys; sys.exit()
	
	
	try:
		os.chdir(os.path.abspath(rootdir))
		_classes = os.listdir(os.curdir)
		for _class in _classes:
			print ("class " + _class)
			if os.path.isdir(_class): # and not _class.startswith("."):
				os.chdir(_class)
				observe(); rename()
				os.chdir("..")
			else:
				print ("not so")
	except:
		print ("fatal error. exiting")
		import sys; sys.exit()

	# to-do
		# log reporting is not comprehensive
		# restructure and properly document code

renamefolders()


# ======#
# thanks to progress, im re-doing bank.py into music.py
# hold this copy, please.

# a python powered, web based music player

import os, re
from operator import attrgetter

disk = {
	"files":[],
	"tracks":[],
	"artists":[],
}

class Music():
	"""
	defines a custom object to simplify data handling
	works better than dictionaries
	"""
	def __init__(self, filename):
		self.filename = filename
		# self.filepath = ??
		
		suspend = makemusic(filename)
		self.title = suspend.get("title")
		self.artist = suspend.get("artist")
		
		feat_list = suspend.get("feat")
		self.feat = feat_list if feat_list != [] else "single"
	
	def __repr__(self):
		return "Music({})".format(self.title)

def walk():
	"""
	look through the "./sdcard/music" folder
	and make music objects of its content.
	"""
	
	# after re-doing the file storage and access method,
	# this function would simply go through the ./static/files
	# folder and check for updates - not the file system!
	
	# ideally, it should write an index of its walk to another file
	# or not
	
	files=os.listdir("/sdcard/music")
	files.remove(".www")
	for file in files:
		disk["files"].append(Music(file))

def makemusic(filename):
	"""
	uses regex to extract primary info from a given filename
	:: artist, title, features/single ..for now
	"""
	# the future makemusic would use info embedded in the file
	
	def extract(filename):
		# a really delicate contraption
		# tested, trusted and proven true
		try:
			form = re.compile(r"(.+) -- (.+)") # written norm
			mo = re.match(form, filename)
			
			artist = mo.group(1)
			title  = mo.group(2).partition('.')[0] # assuming there's an extension
			feat   = []
			
			if 'ft.' in mo.group(2): # then, this is not a single
				ftform = re.compile(r"(.+) ft. (.+)")
				mo2    = re.match(ftform, mo.group(2))
				
				title  = mo2.group(1)
				feat   = mo2.group(2).partition('.')[0].split(', ')
				
			return artist, title, feat
			
		except: #catch any error at all, take no chances
			return '', '', [] # let 'em have those blanks. safe!
	
	artist, title, feat = extract(filename)
	return {"artist":artist, "title":title, "feat":feat}

def load(attrib):
	"""
	load track list by attrib from  disk.files
	i.e build a list of artists or a list of tracks by title
	attributes: artists, or tracks ..for now
	"""
	
	for file in disk["files"]:
		if attrib=="artists" and file.artist not in disk["artists"]:
			disk["artists"].append(file.artist)
		elif attrib=="tracks":
			disk["tracks"].append(file.title)

def tracksby(artist):
	"""
	retrieve a list of tracks by a particular artist
	"""
	bucket=[]
	
	for file in disk["files"]:
		if file.artist.lower() == artist.lower():
			bucket.append(file)
	
	return sorted(bucket, key=attrgetter("title"))

walk()
load("artists"); load("tracks")

# start server
import server