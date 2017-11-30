from socket import *
import sys
import os
import os.path
#import thread  
import threading
from threading import Thread
#inc=0
def run():
	port=8001
	max_conn=5
	BUFFER_SIZE=1024
	
	
	#SETUP
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	#do i need to have threads here so the server is listening to every client node??
	serverSocket.bind((gethostbyname(gethostname()), port))
	#ip=(gethostbyname(gethostname()))
	
	
	#WAIT FOR CONNECTION
	print( 'The server is ready to listen \n')	  
	
	serverSocket.listen(max_conn)
	while True:	
		
	#ACCEPT CONNECTION
		try:
				  
			#START THREAD FOR CONNECTION
			conn, addr = serverSocket.accept() #acept connection from browser
			threading.Thread(target=new_worker, args=(conn, addr)).start()
		
		except Exception as e:
			if serverSocket:
				serverSocket.close()
				#print "Could not open socket:", message
			sys.exit(1) 
	
	#CLOSE CONNECTION 
		serverSocket.close()
	
def new_worker(conn,addr):
	inc=1
	conn.send(str(inc).encode())
	inc=inc +1
	
if __name__ == "__main__":
	run()