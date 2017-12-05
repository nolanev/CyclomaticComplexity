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
from pprint import pprint
from re import match
BUFFER_SIZE=1024

def run():

	#Repo.clone_from(https://github.com/nolanev/CS4400, repo)
	
	while True:
		#connect to lock server
		clientSocket=socket(AF_INET,SOCK_STREAM)
		clientSocket.connect((gethostbyname(gethostname()),8001))
		#send request
		msg ="READY"
		clientSocket.send(msg.encode())
		print("SENT ", msg)
		#if reply granted
		reply=clientSocket.recv(BUFFER_SIZE).decode()
		print("RECIEVED ", reply)
		
		if "DONE" in reply:
			print("bye!")
			conn.close()
			sys.exit()
		do_work(reply,clientSocket)
		time.sleep(3)
		
def do_work(reply, conn):
	sha=reply
	blob_urls = []
	files = []
	token='XXXX'
	payload = {
		'recursive': 'true',
		'access_token': token
	}
	
	repo = requests.get("https://api.github.com/repos/nolanev/CS4400/git/trees/{}".format(sha), params=payload)	
	file_tree = repo.json()['tree']
	for item in file_tree:
		if item['type'] == 'blob':
			blob_urls.append(item['url'])
	
	payload = {'access_token': token}
	headers = {'Accept': 'application/vnd.github.v3.raw+json'} #gets the raw text?
	
	for i, url in enumerate(blob_urls):
		repo = requests.get(url, params=payload, headers=headers)
		files.append(repo.text)		
		#files[i]=repo.text
		print(files[i])

if __name__ == "__main__":
	run()