#!/usr/local/bin/python
########################################################
#
#        File: BattleBots.py
#        Author: Jamie Turner <jamwt@jamwt.com>
#        Date: 4/24/02
#
#        Description:
#
#        See two bots use BotManager and duke it out
#
#        These screennames will truly beat the crap
#        out of each other, so--don't do this to your
#        own s/n unless you want a very high warning
#        percentage
#

sn1 = "nickname"
sn2 = "nickname"

pass1 = "password"
pass2 = "password"

from toc import TocTalk,BotManager

import time


class BattleBot(TocTalk):
	def __init__(self,user,passwd):
		TocTalk.__init__(self,user,passwd)
		self.IMcount = 0
		self.messages = [
"I'm angry, don't talk to me...",
"That's it!  If you talk to me one more time, I'm going to warn you.",
"You asked for it." ]

	def on_IM_IN(self,data):
		# get the screenname to IM back--
		# we don't care about the message
		# in this case!
		screenname = data.split(":")[0]

		# send them the appropriate message
		time.sleep(2)
		self.do_SEND_IM(screenname, self.messages[self.IMcount])
		self.IMcount = self.IMcount + 1
		if self.IMcount == 3:
			self.do_warn(screenname)
			self.IMcount = 0

	def on_EVILED(self,data):
		# who did this to us???
		# (see the on_EVILED event documentation for data format)
		screenname = data.split(":")[1].strip()

		# Anonymous?
		if screenname == "":
			# retribution will not be coming.. of course!
			return

		# Get 'em back
		self.do_warn(screenname)

	def do_warn(self,screenname):
		# three times, we'll try.  Ignore the on_ERROR events
		# if we cannot warn more. We really don't care at
		# this point
		for x in xrange(0,3):
			self.do_EVIL(screenname)

			# so that we don't exceed speed limit
			time.sleep(2)
			
# if this file is run directly
if __name__ == "__main__":
	
	bot = BattleBot(sn1, pass1)
	bot._info = "I'm warrior #1 in this sad, sad fight."
	# make verbose output.  more fun to watch frenzy
	bot._debug = 2

	bot2 = BattleBot(sn2, pass2)
	bot2._info = "I'm warrior #2, sure to be the victor!"
	bot2._debug = 2

	bm = BotManager()
	bm.addBot(bot,"myBot")
	bm.addBot(bot2,"myBot2")

	time.sleep(4) # time to log on

	#set 'em off..
	bot.do_SEND_IM(sn2,"Hi, friend?  How are you?")

	bm.wait()  # this will never return
