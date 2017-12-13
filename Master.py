from socket import *
import sys
import os
import os.path
#import thread  
import threading
from threading import Thread
BUFFER_SIZE=1024
import time

import requests

commit_list = []
results=[]

def run():
	nxt =0
	port=8001
	max_conn=15
	BUFFER_SIZE=1024
	
	
	notDone= True
	start = time.time()
	print("Start Time", start)


	#SETUP
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serverSocket.bind((gethostbyname(gethostname()), port))
	laod_commits()
	print(len(commit_list))
	#WAIT FOR CONNECTION
	print( 'The server is ready to listen \n')	  
	
	#serverSocket.listen(max_conn)
	while notDone:	
		serverSocket.listen(max_conn)
	#ACCEPT CONNECTION
		try:
					
			#START THREAD FOR CONNECTION
			conn, addr = serverSocket.accept() #acept connection from browser
		
			threading.Thread(target=msg_decode, args=(conn, addr,nxt)).start()
			
		except Exception as e:
			if serverSocket:
				serverSocket.close()
				#print "Could not open socket:", message
			sys.exit(1) 
	
		nxt=nxt+1
			
	
	
		
	serverSocket.close()
	
	#sys.exit(1)
	
def msg_decode(conn,addr,nxt):
	ans=conn.recv(BUFFER_SIZE).decode()
	if "READY" in ans:
		print("recieved ready sending more work")
		new_worker(conn,addr,nxt)
		
		conn.close()
	else:
		print("error")
		sys.exit()
		
def new_worker(conn,addr,nxt):
	if nxt>len(commit_list)-1:
		print("done")
		msg="DONE"
		conn.send(msg.encode())
		end = time.time()
		print("End Time ",end)
		#print(end - start)	
		
	else:
		print("sending ", commit_list[nxt])	
		conn.send(commit_list[nxt].encode())
		recive_data(conn,addr,nxt)
	#else: notDone=False

	
def recive_data(conn,addr,nxt):
	msg=conn.recv(BUFFER_SIZE).decode()
	if "Complexity" in msg:
		splitMessage = msg.split('\n')
		ans = splitMessage[0].split(':')[1].strip()
		print(ans)
		results.append(ans)
	#else: 
	#	notDone=False
		
def laod_commits():
	token='fc8bac5dfd0f603b5471a13090a2a101a47a6e10'
	payload = {'access_token': token}
	#repo= requests.get('https://api.github.com/repos/nolanev/CS4400/commits', payload)	
	repo= requests.get('https://api.github.com/repos/nolanev/Distributed-File-System/commits', payload)
	while 'next' in repo.links:
		for item in repo.json():
			#print("first sha: ", item['sha'])
			commit_list.append(item['sha'])
		print(repo.links['next']['url'])
		repo = requests.get(repo.links['next']['url'])
	for item in repo.json():
			commit_list.append(item['sha'])
	#print(commit_list)
	print(len(commit_list))
	
if __name__ == "__main__":
	run()