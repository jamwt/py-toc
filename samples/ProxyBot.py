#!/usr/bin/env python
########################################################
#
#        File: ProxyBot.py
#        Author: Jamie Turner <jamwt@jamwt.com>
#        Date: 4/08/03
#
#        Description:
#
#        Use a bot as a proxy to send/recieve messages.
#
#        Set REAL_SCREENNAME to your true screenname.
#        Set BOT_SCREENNAME,BOT_PASSWORD to an appropriate
#        AIM account.
#
#		Then, send messages to the bot like "target hey, how are you?"
#		The bot will forward these messages to the screenname "target"
#
#		Note: make sure that "target" contains no spaces.  If your buddy
#		has spaces in his screenname, omit them.  "Top Dawg" becomes "topdawg"

from toc import TocTalk

import re


REAL_SCREENNAME = "screenname"
BOT_SCREENNAME = "screenname"
BOT_PASSWORD = "password"

class ProxyBot(TocTalk):
	"""Send a message to another screenname, recieve responses."""
	def __init__(self,uname,password):
		TocTalk.__init__(self,uname,password)

	def on_IM_IN(self,data):
		# Get the screenname, and original message.
		screenname, flag, omessage = data.split(":",2)

		# If this isn't from our screenname, forward it over.
		if self.normalize(screenname) != REAL_SCREENNAME:
			self.do_SEND_IM(REAL_SCREENNAME,("%s said:" % screenname) + omessage)
			return

		# Remove HTML formatting, for now.
		message = self.strip_html(omessage)

		# We need to get the target screenname.
		mess_comps = message.split(" ",1)

		# Did they remember to send the target screenname?
		if len(mess_comps) != 2:
			self.do_SEND_IM(REAL_SCREENNAME, 
"""Error: Bad format.  
Please send messages to me like this:<br>
<i>[target screen name]</i> <i>[message]</i><br>
Where target screen name contains no spaces.""")
			return

		target = mess_comps[0]

		# Preserve the formatting of the message.
		exp = re.compile("%s\s+" % target, re.MULTILINE)

		# Remove the first instance of the screenname.
		messout = re.subn(exp,"",omessage,1)[0]

		# Ok, we'll try to forward it.
		self.do_SEND_IM(target,messout)


	def on_ERROR(self,data):
		"""Handle 901 error if the user isn't signed online"""
		if data.count(":"):
			id,desc = data.split(":",1)

		else:
			id = data

		if id == "901":
			self.do_SEND_IM(REAL_SCREENNAME,
"""Error: User not online.  
Please send messages to me like this:<br>
<i>[target screen name]</i> <i>[message]</i><br>
Where target screen name contains no spaces.""")


# Kick it off
if __name__ == "__main__":
	bot = ProxyBot(BOT_SCREENNAME,BOT_PASSWORD)
	bot._debug = 2
	bot.go()
