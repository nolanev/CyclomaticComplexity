from socket import *
import sys
import os
import os.path
import time
import requests
import json
import shutil
import threading
from threading import Thread
import radon
from radon.cli import Config
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
BUFFER_SIZE=1024

workernum= int(sys.argv[1])
commitdir='./commit' + str(workernum) +'/' #folder where files will be held named for the number of the worker so workers dont interact with eachothers files

def run():
	
	while True:
		clientSocket=socket(AF_INET,SOCK_STREAM)
		clientSocket.connect((gethostbyname(gethostname()),8001))
		
		msg ="READY"
		clientSocket.send(msg.encode())# request for more work
		
		reply=clientSocket.recv(BUFFER_SIZE).decode()
		if "DONE" in reply: #if theres no more work say bye and shit down
			print("bye!")
			clientSocket.close()
			sys.exit()
		else:	
			do_work(reply,clientSocket)
			
			
		
def do_work(reply,conn):
	sha=reply
	blob_urls = []
	files = []
	cc=[]
	token='XXXX'
	payload = {
		'recursive': 'true',
		'access_token': token
	}
	os.mkdir(commitdir)
	
	repo = requests.get("https://api.github.com/repos/nolanev/Distributed-File-System/git/trees/{}".format(sha), params=payload)	#smaller repo to make life earlier
	
	
	file_tree = repo.json()['tree']
	for item in file_tree:
		if item['type'] == 'blob' and (".py" in item['path']): #if the item is a python file

			blob_urls.append(item['url'])  
	
	payload = {'access_token': token}
	headers = {'Accept': 'application/vnd.github.v3.raw+json'} #gets the raw text?
	
	for i, url in enumerate(blob_urls): #of the files that we want go through each one and save the text to a file
		repo = requests.get(url, params=payload, headers=headers)
		filename= commitdir+ '{}.py'.format(i)
		with open(filename, 'w') as f:
			files.append(filename) #list holding all the file names
			f.write(repo.text) #put text of all files in the commit into python files in directory repo
	
	avg=getCC(files)
	shutil.rmtree(commitdir)
	if avg!=None:
		msg="Complexity of commit: " + str(avg) 
	else:
		msg="done"
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
			) #found online
	commit_complexity=0
	numfiles=0
	for i ,item in enumerate(files): #forever file get complexity and increase total complexity
		f = open(files[i], 'r')
		results = CCHarvester(files[i], config).gobble(f)
		numfiles +=1
		total_cc = 0
		for result in results:
			commit_complexity += int(result.complexity)
				
	if numfiles !=0:	
		return commit_complexity / numfiles
	else: return None #to avoid divide by zero for empyt commit

if __name__ == "__main__":
	run()