#!/usr/local/bin/python
##############  NewSNBot.py  ################
##
##  This is a screenname change bot.
##  When you change your screenname,
##  let this bot help get the word out.
##  
##  Run this bot with your old screenname
##  and password, and whenever someone IMs
##  your old name, it will tell them about
##  about your new one.
##
##	Copyright Dylan Thomas
############ dylant@ucla.edu ################


from toc import TocTalk

## Set These ##
new_sn = "NewNick"
old_sn = "OldNick"
old_pw = "password"


class SNBot(TocTalk):
	#whenever someone IMs us
	def on_IM_IN(self,data):
		# data contains "screenname:flag:message", such as
		# "jamwt:F:hey, ben.. how's work?"
		data_components = data.split(":")

		screenname = data_components[0]  # the sender's screenname

		# let's tell them your new screenname
		self.do_SEND_IM(screenname, "Hey, guess what, I'm using <b> " + new_sn +" </b> as my screenname now.  Please use that.  Thanks alot.")
		
# if this file is run directly
if __name__ == "__main__":
	
	# create the bot, specify some AIM account to use
	bot = SNBot(old_sn, old_pw)
	bot.go()

