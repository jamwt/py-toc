#!/usr/local/bin/python
########################################################
#
#        File: AwayBot.py
#        Author: Jamie Turner <jamwt@jamwt.com>
#        Date: 4/11/02
#
#        Description:
#
#        Weird little bot that sets its away message
#        according to viewers incoming IMs.
#


from toc import TocTalk

import time

class AwayBot(TocTalk):
	#whenever someone IMs us
	def on_IM_IN(self,data):
		# get the screenname to IM back--
		# and the message to set as our away
		screenname = data.split(":")[0]
		message = self.strip_html(":".join(data.split(":")[2:]) )

		# first, clear it
		self.do_SET_AWAY("")

		# delay
		time.sleep(2)

		# thank them
		self.do_SEND_IM(screenname, 
		"Thanks for giving me an idea for my away message!" )

		# delay
		time.sleep(2)

		# set the away message accordingly
		self.do_SET_AWAY(
		'''<B>%s</B> offered this: "<I>%s</I>"''' % (screenname,message) )
			
# if this file is run directly
if __name__ == "__main__":
	
	# create the bot, specify some AIM account to use
	bot = AwayBot("IMscreenname", "somepass")

	# Py-TOC will use this var as our info
	bot._info = \
"Hi, I'm an away message bot.  IM me something clever and I'll use it as my away message."

	# Start it up.  We never return from this
	bot.go()


