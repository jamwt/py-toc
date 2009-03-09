#!/usr/local/bin/python
########################################################
#
#        File: SDBot.py
#        Author: Jamie Turner <jamwt@jamwt.com>
#        Date: 4/11/02
#
#        Description:
#
#        Self-Defense bot.  When you message it,
#        it just bounces back a reminder not to
#        warn it.  
#
#        When someone warns it, it quickly 
#        tries to warn them three times--
#        taking a 2 second break between each
#        as not to violate speed rules.
#
#        It then blocks them so that they cannot
#        converse with you/warn you additionally.
# 
#        blocked (list) will be set to [] on load,
#        so it's not persistent.  The bot 
#        re-allows blocked users after restart
#        

# some lib things...
import time

from toc import TocTalk

# global list to hold blocked screennames
blocked = []

class SDBot(TocTalk):
	#whenever someone IMs us
	def on_IM_IN(self,data):
		# get the screenname to IM back--
		# we don't care about the message
		# in this case!
		screenname = data.split(":")[0]

		# just cautioning 'em
		self.do_SEND_IM(screenname, 
		'''<B>Caution.</B> I am prepared to defend myself from the 
likes of you.  Warn me not!''' )
		
	def on_EVILED(self,data):
		global blocked
		# who did this to us???
		# (see the on_EVILED event documentation for data format)
		screenname = data.split(":")[1].strip()

		# Anonymous?
		if screenname == "":
			# retribution will not be coming.. of course!
			return

		# three times, we'll try.  Ignore the on_ERROR events
		# if we cannot warn more. We really don't care at
		# this point
		for x in xrange(0,3):
			self.do_EVIL(screenname)

			# so that we don't exceed speed limit
			time.sleep(2)

		# add to the list
		blocked.append("d %s\n" % screenname)

		# (see on_CONFIG event documentation for arg format)
		self.do_SET_CONFIG(
		"m 4\ng Buddies\nb jamwt\n" + "".join(blocked)
		)

		# just loggin'
		print "Warned and blocked %s!  Who's next?" % screenname

			
# if this file is run directly
if __name__ == "__main__":
	
	# create the bot, specify some AIM account to use
	bot = SDBot("IMscreenname", "somepass")

	# Py-TOC will use this var as our info
	bot._info = "Self-Defense bot.  You lookin' at me?"

	# Start it up.  We never return from this
	bot.go()


