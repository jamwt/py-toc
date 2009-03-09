#!/usr/bin/env python

"""CLAIM is a command-line instant messenger.  

Requirements
------------

Python 2.0+ http://www.python.org  (compiled w/threads)
Py-TOC http://jamwt.com/Py-TOC/

Usage
-----

python claim.py

(then just login with your AIM screenname and password...)

Basic Commands
--------------

Enter '1' (one)  to see your buddy list.
Enter '2' (two)  to see a hotlist of shortcuts to talk to
                 buddies who you have recently conversed with
Enter '0' (zero) to log out

Messaging
---------

To message a buddy, type their name, then the message you want
to send them at the prompt:

? jamwt hey, py-toc is cool!

Every time you message someone, that person is marked as the 
"last buddy" item in the hotlist.  To message this person again,
use the hotlist shortcut '.' (period).

? . like I said, I really like it

Whenever you message someone, or someone messages you, an entry
will be made in the hotlist so that you can use a shortcut to 
message back.  Enter '2' alone on a line to see your hotlist.

If 'spamguy' sends you a message, he will be given the hotlist
slot 's'.  You can respond to him using this shortcut.

? s What do you want, spammer?

If you send 'sally' a message soon after that, she will be given
the 'a' slot, because 's' is already taken (and so on).

? sally I didn't see you at school today
? a are you ok?

Of course, the shortcut '.' would have worked equally well here.

Hotlist entires eventually expire if no messages are sent to or
from that person for awhile.

Other Features
--------------

CLAIM will notify you of warnings, and it will automatically warn
in response (no AIM network messenger could really be complete 
without this basic ability.)  

Author
------

Jamie Turner <jamwt@jamwt.com>
The on_ERROR code is ripped from Kent Hu's alarmbot.

"""

from toc import TocTalk, BotManager

import sys
import time
import string
import getpass

buds = None
def rlcomplete(text,state):
	global buds
	if not state:
		buds = bot.blist.keys()
		buds.sort()

	x = 0
	for bud in buds:
		if bud.startswith(text):
			x += 1
			if x > state:
				return bud + " "
	
	return None

try:
	import readline
except:
	pass
else:
	readline.set_completer(rlcomplete)
	readline.parse_and_bind("tab: complete")

cfgset = 0


class Outputter:
	def __init__(self,hl):
		self.last = None
		self.hl = hl
		
	def error(self,msg):
		sys.stdout.write("\n--- ERROR: %s ---\n" % msg)

	def info(self,msg):
		sys.stdout.write("\n--- %s ---\n" % msg)

	def message(self,f,msg):
		sys.stdout.write("\n<== %s: %s\n" % (f,msg))

	def mout(self,t,msg):
		sys.stdout.write("\n==> to %s: %s\n" % (t,msg))

	def hotlist(self):
		map = self.hl.getList()
		keys = map.keys()
		keys.sort()
		sys.stdout.write("\n  Hotlist\n  ---------------------------\n")
		sys.stdout.write(" . is %s\n" % self.last)

		for item in keys:
			sys.stdout.write(" %s is %s\n" % (item,map[item]))
		sys.stdout.write("\n")

	def setBot(self,bot):
		self.bot = bot

	def blist(self):
		bds = self.bot.blist.copy()

		nms = bds.keys()
		nms.sort()
		sys.stdout.write("\n  Buddies (%d Online)\n  ---------------------------------------------------------\n" % len(nms))

		x = 0

		offset = len(nms) / 2
		if len(nms) % 2:
			offset = len(nms) / 2 + 1

		for x in xrange(len(nms)/2):
			nm = nms[x]
			idle = ""
			if bds[nm].idle:
				idle = ( " (idle %sm)" % 
				(bds[nm].idle[0] + ( (int(time.time()) - bds[nm].idle[1])/60 )))

			nm2 = nms[x + offset] #odd.. need to increment
			idle2 = ""
			if bds[nm2].idle:
				idle2 = ( " (idle %sm)" % 
				(bds[nm2].idle[0] + ( (int(time.time()) - bds[nm2].idle[1])/60 )))

			sys.stdout.write(
			"   %-30s %s\n" % ( bds[nm].name + idle,bds[nm2].name + idle2) )

		if len(nms) % 2:
			nm = nms[len(nms) / 2]
			idle = ""
			if bds[nm].idle:
				idle = (  "(idle %sm)" % 
				(bds[nm].idle[0] + ( (int(time.time()) - bds[nm].idle[1])/60 )))

			sys.stdout.write(
			"   %s\n" % ( bds[nm].name + idle) )
		sys.stdout.write("\n")



	def go(self):
		while 1:

			l = raw_input("claim> ").strip()

			if l == "":
				continue

			if l == "1":
				self.blist()
				continue

			if l == "2":
				self.hotlist()
				continue

			if l == "0":
				sys.exit(0)

			try:
				n,m = l.split(' ',1)
			except:
				self.error("format <screename> <message>")
				continue

			if n == ".":
				if not self.last:
					self.error("no last screenname yet")
					continue
				n = self.last

			elif len(n) == 1 and n in string.ascii_letters:
				n = self.hl.get(n)
				if not n:
					self.error("unknown hotlist buddy")
					self.hotlist()
					continue

			self.last = n
			self.hl.hint(self.last)

			self.bot.do_SEND_IM(n,m)
			self.mout(n,m)

_HLEXPIRE = 15 # minutes

class Hotlist:
	def __init__(self):
		self.buddies = {}

	def _weed(self):
		t = time.time()
		for k in self.buddies.keys():
			if t - self.buddies[k][1] > _HLEXPIRE * 60:
				del self.buddies[k]

	def hint(self,name):
		self._weed()
		if self.buddies.has_key(name):
			self.buddies[name][1] = time.time()
		else:
			letters = []
			for k in self.buddies.keys():
				letters.append(self.buddies[k][0])

			# now we find the letter to use for this one
			for let in name.lower():
				if let in string.ascii_letters and not let in letters:
					self.buddies[name] = [let,time.time()]
					break

	def getList(self):
		self._weed()
		out = {}
		for item in self.buddies.keys():
			out[self.buddies[item][0]] = item
		return out

	def get(self,letter):
		letter = letter.lower()
		for item in self.buddies.keys():
			if self.buddies[item][0] == letter:
				return item
		return None

class Buddy:
	def __init__(self,name,idle):
		self.name = name
		self.idle = 0
		if int(idle):
			self.idle = [int(idle),int(time.time())]

class Claim(TocTalk):
	def __init__(self,name,passwd,outer,hl):
		TocTalk.__init__(self,name,passwd)
		self.outer = outer
		self.blist = {}
		self.hl = hl

	def on_IM_IN(self,data):
		sn,dc,msg = data.split(":",2)
		sn = self.normalize(sn)

		self.hl.hint(sn)

		msg = self.strip_html(msg)

		self.outer.message(sn,msg)

	def on_UPDATE_BUDDY(self,data):
		sn,online,warning,dc,idle,dc = data.split(":")
	#	print data # this will work for each buddy in your config
		snorm = self.normalize(sn)

		if online.upper() == "T":
			self.blist[snorm] = Buddy(self.normalize(sn),idle)
		else:
			try:
				del self.blist[snorm]
			except:
				pass

	def on_CONFIG(self,data):
		global cfgset

		# first time logging in--add buddies from config...
		if not cfgset:
			cfgset = 1

			buds = []

			# remember the format of config data here:
			# "m 1\ng Buddies\nb bouncebot\nb perlaim\n"
			for item in data.split("\n"):
				if item == '':
					continue
				if item[0] == "b":
					buds.append(item[1:].strip())

				#add no more than ~20 at a time, msg len restrictions
				if len(buds) == 20:
					self.do_ADD_BUDDY(buds)
					time.sleep(0.2) # don't SLAM the server...
					buds = []

			if len(buds):
				self.do_ADD_BUDDY(buds)
					
			sys.stdout.write("--- OK, go! ---\n")

	def on_EVILED(self,data):
		# who did this to us???
		# (see the on_EVILED event documentation for data format)
		per,screenname = data.split(":")

		screenname = screenname.strip()

		# Anonymous?
		if screenname == "":
			# retribution will not be coming.. of course!
			self.outer.info("You have been warned anonymously to %s%%" % 
			per)

		else:
			self.outer.info("You have been warned by %s to %s%%." % 
			(screenname,per))
			self.do_EVIL(screenname)
			self.outer.info("You automatically warned back.")

	def on_ERROR(self, data):
		data_components = data.split(':', 1)
		err = data_components[0]

		if err in errMessages.keys():
			errmsg1 = errMessages[err]
		else:
			errmsg1 = 'unknown error code'

		if len(data_components) == 2:
			errmsg2 = data_components[1]
		else:
			errmsg2 = 'ARGUMENT'

		message = errmsg1
		if message.count('%s'):
			message = message % errmsg2
		else:
			message += ': %s' % errmsg2
		self.outer.error(message)

errMessages = {'901':'%s not currently available',
               '902':'Warning of %s not currently available',
               '903':'A message has been dropped, you are exceeding the server speed limit',
               '950':'Chat in %s is unavailable.',
               '960':'You are sending message too fast to %s',
               '961':'You missed an im from %s because it was too big.',
               '962':'You missed an im from %s because it was sent too fast.',
               '970':'Failure',
               '971':'Too many matches',
               '972':'Need more qualifiers',
               '973':'Dir service temporarily unavailable',
               '974':'Email lookup restricted',
               '975':'Keyword Ignored',
               '976':'No Keywords',
               '977':'Language not supported',
               '978':'Country not supported',
               '979':'Failure unknown %s'}


if __name__ == "__main__":
	sn = raw_input("Username: ").strip()
	pw = getpass.getpass("Password: ").strip()

	hl = Hotlist()

	output = Outputter(hl)

	bot = Claim(sn,pw,output,hl)
	bot._debug = 0
	bot._profile = "Hi, I'm running CLAIM 1.0: Py-TOC powered!"
	output.setBot(bot)

	bm = BotManager()

	try:
		bm.addBot(bot,"claimbot")

	except TOCError:
		output.error(sys.exc_value)
		sys.exit(1)


	output.go()
