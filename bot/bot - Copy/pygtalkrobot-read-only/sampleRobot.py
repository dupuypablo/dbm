#!/usr/bin/python
# -*- coding: utf-8 -*-

# PyGtalkRobot: A simple jabber/xmpp bot framework using Regular Expression Pattern as command controller
# Copyright (c) 2008 Demiao Lin <ldmiao@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Homepage: http://code.google.com/p/pygtalkrobot/
#

#
# This is an sample PyGtalkRobot that serves to set the show type and status text of robot by receiving message commands.
#
import thread
import socket
import sys
import time
import re
import shlex
from subprocess import *

from PyGtalkRobot import GtalkRobot

############################################################################################################################

class SampleBot(GtalkRobot):
    

    def run(self,p,user,message,args):
        print 'esperando...'
        print p
        #print p.stdout..rstrip()

        for line in p.stdout:
            print 'leido...'
            print line


    #Regular Expression Pattern Tips:
    # I or IGNORECASE <=> (?i)      case insensitive matching
    # L or LOCALE <=> (?L)          make \w, \W, \b, \B dependent on the current locale
    # M or MULTILINE <=> (?m)       matches every new line and not only start/end of the whole string
    # S or DOTALL <=> (?s)          '.' matches ALL chars, including newline
    # U or UNICODE <=> (?u)         Make \w, \W, \b, and \B dependent on the Unicode character properties database.
    # X or VERBOSE <=> (?x)         Ignores whitespace outside character sets
    
    #"command_" is the command prefix, "001" is the priviledge num, "setState" is the method name.
    #This method is used to change the state and status text of the bot.
    def command_001_setState(self, user, message, args):
        #the __doc__ of the function is the Regular Expression of this command, if matched, this command method will be called. 
        #The parameter "args" is a list, which will hold the matched string in parenthesis of Regular Expression.
        '''(available|online|on|busy|dnd|away|idle|out|off|xa)( +(.*))?$(?i)'''
        show = args[0]
        status = args[1]
        jid = user.getStripped()
        
        print jid
        # Verify if the user is the Administrator of this bot
        if re.search('dupuypablo', jid).group(0) == 'dupuypablo':
            print jid, " ---> ",bot.getResources(jid), bot.getShow(jid), bot.getStatus(jid)
            self.setState(show, status)
            self.replyMessage(user, "State settings changed！")

    #This method is used to send email for users.
    def command_002_SendEmail(self, user, message, args):
        #email ldmiao@gmail.com hello dmeiao, nice to meet you, bla bla ...
        '''[email|mail|em|m]\s+(.*?@.+?)\s+(.*?),\s*(.*?)(?i)'''
        email_addr = args[0]
        subject = args[1]
        body = args[2]
        call_send_email_function(email_addr, subject,  body)
        
        self.replyMessage(user, "\nEmail sent to "+ email_addr +" at: "+time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))
    
    def command_003_status(self, user, message, args):
        #status
        '''(status)( +(.*))?$(?i)'''
        #p = Popen(['cat', 'status' ], stdout=PIPE).communicate()[0];
        #self.p = Popen(['perl', '-e', "'print 1; while (<>){print $_,$_}'"], stdout=PIPE, stdin=PIPE);
        self.p = Popen(['./tryme'], stdout=PIPE, stdin=PIPE)
        

        ##for i in range(10):
        #    self.p.stdin.write('ff %d\n' % i)
        #    output = self.p.stdout.readline()
        #    print output.rstrip()
        #remainder = self.p.communicate()[0]
        #print remainder

        print self.p
        #self.p.stdin.write('one\ntwo\nthree\nfour\nfive\nsix\n')
        #print(self.p.stdout.readline())
        thread.start_new_thread( self.run, (self.p,user,message, args ) )

        #grep_stdout2 = p.communicate(input='one\ntwo\nthree\nfour\nfive\nsix\n')[0]
        #print(grep_stdout2)
        ##self.p = Popen(['grep', 'f'], stdout=PIPE, stdin=PIPE)
        ##print self.p.communicate(input='Probando\none\ndos\nthres\n')[0]
#        p = Popen(['echo ', user.getStripped() ], stdout=PIPE).communication()[0];
        ##self.replyMessage(user, self.p.communicate(input="probando probando..."))


    #This method is used to response users.
    def command_100_default(self, user, message, args):
        '''.*?(?s)(?m)'''
        self.replyMessage(user, time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))
        print '...'
        if hasattr(self, 'p'):
            print message
            print 'si!'
            print self.p
            self.p.stdin.write(message+"\n")
            #print 'acabo de escribir en el programa 123456.'
   
        #self.replyMessage(user, "Digo:" + self.p.communicate(message))
   
############################################################################################################################
if __name__ == "__main__":

    bot = SampleBot()
    #UDP_IP="127.0.0.1"
    #UDP_PORT=5005
    #try:
    #    bot.sock = socket.socket( socket.AF_INET, # Internet
    #                   socket.SOCK_DGRAM ) # UDP
    #    bot.sock.bind( (UDP_IP,UDP_PORT) )
    #    bot.sock.settimeout(.1)
    #except:
    bot.setState('available', "Simple Gtalk Robot")
    bot.start("dungeon.bot.master@gmail.com", "pablodupuy")
    
