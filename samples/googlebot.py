#!/usr/local/bin/python
#
# AIM bot that performs Google searches.
#
# Cobbled together by Matt King 6/26/02
#

# Py-TOC from http://jamwt.com/Py-TOC/index.html
from toc import TocTalk
# PyGoogle from http://diveintomark.org/projects
import google

google.LICENSE_KEY = "YOUR LICENSE KEY HERE"
USERNAME = "ScreenName"
PASSWORD = "Password"

class GoogleBot(TocTalk):
    def __init__(self, user, pw):
        TocTalk.__init__(self, user, pw)
        self._info = "Google-AIM Bot"

    #whenever someone IMs us
    def on_IM_IN(self,data):
        # data contains "screenname:flag:message", such as
        # "jamwt:F:hey, ben.. how's work?"
        data_components = data.split(":",2) #maxsplit for handling 
                                            #in-message colons
        
        screenname = data_components[0]  # the sender's screenname
        message = data_components[2]     # in case the sender 
                                                # used a colon in their 
                                                # message

        # TocTalk also includes a special helper function called
        # strip_html().  Many AIM clients like Windows AIM use HTML
        # code.  strip_html() will remove HTML tags and make it text
        message = self.strip_html(message)

        # Perform the Google search
        data = google.doGoogleSearch(message)

        # Format the results.  For now, just the top 3...
        response = """\nSearch: %s\nResuls:\n""" % message
        for res in data.results[0:3]:
            response = response + """<a href="%s">%s</a>\n""" % (res.URL, res.title)

        # Send the results back to the user
        self.do_SEND_IM(screenname, response)
                
# if this file is run directly
if __name__ == "__main__":
        
        # create the bot, specify some AIM account to use
        bot = GoogleBot(USERNAME, PASSWORD)
        try:
            bot.go()
        except KeyboardInterrupt:
            pass
        
