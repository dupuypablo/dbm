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
def readFile(fileHandle): 

     line = fileHandle.readline() 
     dictName = {} 

     while line: 
         splitted = line.split("\t")
	 key = splitted[0].split("@")[0]
	 print key
	 dictName[key] = splitted[1].rstrip('\n') 
         line = fileHandle.readline() 

     return dictName
     
     
   
         
class UserClass:
    def __init__(self,username):
      self.user = username

class SampleBot(GtalkRobot):
    

    def run(self,p,user,message,args):
        print 'esperando...'
        print p
        for line in iter(p.stdout.readline, ""): 
            self.replyMessage(user, line+"\n")
            print 'leido...'
            print line

    def comm(self,user,message,args):
      while True:
	print 'leyendo el fifo...'
	user.fifo = open('{}/characters/p{}/.fifo'.format(os.environ['WORLD'],self.names[user.getNode()]),'r')
	print 'file fifo abierto...'
        for line in iter(user.fifo.readline, ""): 
            print 'leido...'
            self.replyMessage(user, line)
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
	print "soy:", user.getNode(), " (((())))\n"  
	self.u[user.getNode()].user = user.getNode()   
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
        '''(atacar)( +(.*))?$(?i)'''
	self.u[user.getNode()].user = user.getNode()
        print self.u[user.getNode()].p
        thread.start_new_thread( self.run, (self.u[user.getNode()].p,user,message, args ) )

    def command_004_status(self, user, message, args):
        #status
        '''(nuevo personaje)( +(.*))?$(?i)'''
        self.u[user.getNode()].p = Popen(['genPlayer'], stderr=STDOUT, stdout=PIPE, stdin=PIPE, bufsize=0, universal_newlines=True)
        self.u[user.getNode()].user = user.getNode()
	print self.u[user.getNode()].p
        thread.start_new_thread( self.run, (self.u[user.getNode()].p,user,message, args ) )


    def command_005_status(self, user, message, args):
        #status
        '''(hola)( +(.*))?$(?i)'''
	if not hasattr(self,'u'):
	  myu = UserClass(user.getNode());
	  self.u={ user.getNode(): myu }
	  print "aca1", user.getNode(), self.u;
	if not user.getNode() in self.u:
	  print "aca2";
	  myu = UserClass(user.getNode());
	  self.u[user.getNode()] = myu;
	print "Alguien dijo Hola", user.getNode(), self.u;
	
	self.replyMessage(user, "Hola {}".format(self.names[user.getNode()]))

        if not hasattr(self.u[user.getNode()], 'fifo'):
          thread.start_new_thread( self.comm, (user,message, args ) )

	
    def command_006_status(self, user, message, args):
        #status
        '''(info)( +(.*))?$(?i)'''
        f = Popen(['info', '{}/characters/p{}'.format(os.environ['WORLD'],self.names[user.getNode()])] , stderr=STDOUT, stdout=PIPE, stdin=PIPE, bufsize=0, universal_newlines=True)
	self.replyMessage(user, ("".join(f.stdout.readlines())).replace("\t",": " ))
   
    def command_007_status(self, user, message, args):
        #status
        '''(log)( +(.*))?$(?i)'''
        f = Popen(['log', self.names[user.getNode()]], stderr=STDOUT, stdout=PIPE, stdin=PIPE, bufsize=0, universal_newlines=True)
	f.stdin.write(message)
	f.stdin.write('\n')
	f.stdin.close()
	self.replyMessage(user, ("".join(f.stdout.readlines())).replace("\t",": " ))   

    def command_008_status(self, user, message, args):
        #status
        '''(partylog)( +(.*))?$(?i)'''
        f = Popen(['log'], stderr=STDOUT, stdout=PIPE, stdin=PIPE, bufsize=0, universal_newlines=True)
	f.stdin.write(message)
	f.stdin.write('\n')
	f.stdin.close()
	self.replyMessage(user, ("".join(f.stdout.readlines())).replace("\t",": " ))   

    def command_099_help(self, user, message, args):
        #status
        '''(help)( +(.*))?$(?i)'''
	self.replyMessage(user, "hola|nuevo personaje|atacar|info|log|partylog")
  
   #This method is used to response users.
    def command_100_default(self, user, message, args):
        '''.*?(?s)(?m)'''
        self.replyMessage(user, time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))
        print '...'
        print user.getNode()
	#help(user);
        print message
	if not hasattr(self,'u'):
	  myu = UserClass(user.getNode());
	  self.u={ user.getNode(): myu }
	  print "aca1", user.getNode(), self.u;
	if not user.getNode() in self.u:
#	  print "aca2";
	  myu = UserClass(user.getNode());
	  self.u[user.getNode()] = myu;
#	print "aca3", user.getNode(), self.u;

        if hasattr(self.u[user.getNode()], 'p'):
            print 'si!'
            if self.u[user.getNode()].p.poll() is None:
                self.u[user.getNode()].p.stdin.write(message+"\n")
   
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
    import os
    f = open('{}/characters/players'.format(os.environ['WORLD']), 'r')
    bot.names = readFile(f)
    bot.start("dungeon.bot.master@gmail.com", "pablodupuy2")
    print "hola\n"
