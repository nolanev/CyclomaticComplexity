from socket import *
import sys
import os
import os.path
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
	
	while notDone:	
		serverSocket.listen(max_conn)
	
		try:
					
			conn, addr = serverSocket.accept() #acept connection from browser
		
			threading.Thread(target=msg_decode, args=(conn, addr,nxt)).start()
			
		except Exception as e:
			if serverSocket:
				serverSocket.close()
			sys.exit(1) 
	
		nxt=nxt+1 #counts which commit we are sending
			
	serverSocket.close()
	
	
def msg_decode(conn,addr,nxt): #check message from worker is valid and if they are asking for more work or sending results
	msg=conn.recv(BUFFER_SIZE).decode()
	if "READY" in msg:
		print("recieved ready sending more work")
		new_worker(conn,addr,nxt)
		conn.close()
	elif "Complexity" in msg:
		splitMessage = msg.split('\n')
		ans = splitMessage[0].split(':')[1].strip()
		print(ans)
		results.append(ans)
	else:
		print("error")
		sys.exit()
		
def new_worker(conn,addr,nxt):

	if nxt>len(commit_list)-1: #if we have run out of commits to send out we're done
		print("done")
		msg="DONE"
		conn.send(msg.encode())
		end = time.time()
		print("End Time ",end)
		notDone=False #exit loop and close socket
				
	else:
		print("sending ", commit_list[nxt])	#send on next commit sha
		conn.send(commit_list[nxt].encode())
		msg_decode(conn,addr,nxt)	#recive reply
		
def laod_commits():
	token='XXXX' #removed for security
	payload = {'access_token': token}
	repo= requests.get('https://api.github.com/repos/nolanev/Distributed-File-System/commits', payload)
	
	#add commit sha to list
	while 'next' in repo.links: 
		for item in repo.json():
			commit_list.append(item['sha'])  
		print(repo.links['next']['url'])
		repo = requests.get(repo.links['next']['url'])
	for item in repo.json():
			commit_list.append(item['sha'])
	print(len(commit_list))
	
if __name__ == "__main__":
	run()