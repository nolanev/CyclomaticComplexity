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
BUFFER_SIZE=1024

def run():

	#Repo.clone_from(https://github.com/nolanev/CS4400, repo)
	#acf1633fa54ece1702f2035d673c533c99c6d4ca
	
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
		do_work(reply)
		time.sleep(10)
		
def do_work(reply):
	repo= requests.get('https://api.github.com/repos/nolanev/CS4400/commits',reply)
	
		
if __name__ == "__main__":
	run()