from socket import *

import sys
import os
import os.path
import time
import requests
import json

import threading
from threading import Thread
from git import Repo
import radon
from radon.cli import Config
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
BUFFER_SIZE=1024



def run():
	
	while True:
		clientSocket=socket(AF_INET,SOCK_STREAM)
		clientSocket.connect((gethostbyname(gethostname()),8001))
		#send request
		msg ="READY"
		clientSocket.send(msg.encode())
		#print("SENT ", msg)
			#if reply granted
		reply=clientSocket.recv(BUFFER_SIZE).decode()
			#print("RECIEVED ", reply)
		
		if "DONE" in reply:
			print("bye!")
			conn.close()
			sys.exit()
		else:	
			do_work(reply,clientSocket)
			
			
		#reply=clientSocket.recv(BUFFER_SIZE).decode()
		
def do_work(reply,conn):
	sha=reply
	blob_urls = []
	files = []
	cc=[]
	token='XXX'
	payload = {
		'recursive': 'true',
		'access_token': token
	}
	
	#repo = requests.get("https://api.github.com/repos/nolanev/CS4400/git/trees/{}".format(sha), params=payload)
	repo = requests.get("https://api.github.com/repos/nolanev/Distributed-File-System/git/trees/{}".format(sha), params=payload)	#smaller repo to make life earlier
	#https://github.com/nolanev/Distributed-File-System
	file_tree = repo.json()['tree']
	for item in file_tree:
		if item['type'] == 'blob' and (".py" in item['path']):

			blob_urls.append(item['url'])
	
	payload = {'access_token': token}
	headers = {'Accept': 'application/vnd.github.v3.raw+json'} #gets the raw text?
	
	for i, url in enumerate(blob_urls):
		repo = requests.get(url, params=payload, headers=headers)
		with open('./repo/{}.py'.format(i), 'w') as f:
			files.append('./repo/{}.py'.format(i)) #list holding all the file names
			f.write(repo.text) #put text of all files in the commit into python files in directory repo
	avg=getCC(files)		
	msg="Complexity of commit: " + str(avg) 
	
	conn.send(msg.encode())
	
def getCC(files):
	config = Config(
			exclude="",
			ignore="",
			order=SCORE,
			no_assert=True,
			show_complexity=True,
			average=True,
			total_average=True,
			show_closures=True,
			min='A',
			max='F'
			)
	commit_complexity=0
	numfiles=0
	for i ,item in enumerate(files):
		f = open(files[i], 'r')
		results = CCHarvester(files[i], config).gobble(f)
		numfiles +=1
		print("here")
		total_cc = 0
		for result in results:
			commit_complexity += int(result.complexity)
			#print(commit_complexity)
				
	return commit_complexity / numfiles
	
if __name__ == "__main__":
	run()