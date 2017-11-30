from socket import *
import sys
import os
import os.path
import time
#import thread  
import threading
from threading import Thread

BUFFER_SIZE=1024

def run():
	
	while True:
		#connect to lock server
		clientSocket=socket(AF_INET,SOCK_STREAM)
		clientSocket.connect((gethostbyname(gethostname()),8001))
		#send request
		msg ="READY"
		clientSocket.send(msg.encode())
		#if reply granted
		reply=clientSocket.recv(BUFFER_SIZE).decode()
		print(reply)
		if "DONE" in reply:
			print("bye!")
			conn.close()
			sys.exit()
		do_work(reply)
		
def do_work(reply):
	print(" I am worker no ", str(reply))
		
if __name__ == "__main__":
	run()