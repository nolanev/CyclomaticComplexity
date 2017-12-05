from socket import *
import sys
import os
import os.path
#import thread  
import threading
from threading import Thread

import requests

commit_list = []

def run():
	nxt =0
	port=8001
	max_conn=15
	BUFFER_SIZE=1024
	
	
	#SETUP
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serverSocket.bind((gethostbyname(gethostname()), port))
	laod_commits()

	#WAIT FOR CONNECTION
	print( 'The server is ready to listen \n')	  
	
	serverSocket.listen(max_conn)
	while True:	
		
	#ACCEPT CONNECTION
		try:
				  
			#START THREAD FOR CONNECTION
			conn, addr = serverSocket.accept() #acept connection from browser
		
			threading.Thread(target=new_worker, args=(conn, addr,nxt)).start()
			
			
		
		except Exception as e:
			if serverSocket:
				serverSocket.close()
				#print "Could not open socket:", message
			sys.exit(1) 
	
		nxt=nxt+1
		serverSocket.listen(max_conn)
	
def new_worker(conn,addr,nxt):
	print("sending ", commit_list[nxt])
	conn.send(commit_list[nxt].encode())
	
def laod_commits():
	token='XXXX'
	payload = {'access_token': token}
	repo= requests.get('https://api.github.com/repos/nolanev/CS4400/commits', payload)
	while 'next' in repo.links:
		for item in repo.json():
			commit_list.append(item['sha'])
		print(repo.links['next']['url'])
		repo = requests.get(repo.links['next']['url'])
	for item in repo.json():
			commit_list.append(item['sha'])
	#print(commit_list)
	print(len(commit_list))
	
if __name__ == "__main__":
	run()