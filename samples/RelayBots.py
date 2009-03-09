#!/usr/local/bin/python
########################################################
#
#        File: RelayBots.py
#        Author: Jamie Turner <jamwt@jamwt.com>
#        Date: 4/24/02
#
#        Description:
#
#        Demonstrates script-side data sharing between
#        two bots
#
#        say things to master and slave will echo them
#        back to you
#

masterSN = "nickname"
slaveSN = "nickname"

masterPW = "password"
slavePW = "password"

from toc import TocTalk,BotManager

import time
import Queue


class Master(TocTalk):
	def __init__(self,user,passwd):
		TocTalk.__init__(self,user,passwd)
		# great method of passing data 
		# between the threads
		self.queue = Queue.Queue() 

	def on_IM_IN(self,data):
		screenname, dont_care, message = data.split(":",2)
		self.queue.put([screenname,message])

		self.do_SEND_IM(screenname,
"I'm not going to echo that.  I'll have my slave do it.")

class Slave(TocTalk):
	def __init__(self,user,passwd, masterSN):
		TocTalk.__init__(self,user,passwd)
		self.masterSN = masterSN

	def on_IM_IN(self,data):
		screenname = data.split(":")[0]

		self.do_SEND_IM(screenname,
"Sorry, I only say what my master, %s, tells me to say." % self.masterSN)

# if this file is run directly
if __name__ == "__main__":
	
	# create the master
	mb = Master(masterSN, masterPW)

	# create the slave
	sb = Slave(slaveSN, slavePW, masterSN)

	bm = BotManager()
	bm.addBot(mb,"mb")
	bm.addBot(sb,"sb")

	while 1:
		# blocks until we read
		[screenname, message] = mb.queue.get() 
		sb.do_SEND_IM(screenname, 
'''You said %s to my master %s.''' % (message,masterSN) )
