import socket

for i in range(10)
	sock+str(i) = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	sock+str(i).bind(('10.10.2.10', 4000+str(i)))
	sock+str(i).listen()
	conn_sock+str(i), conn_addr+str(i) = sock+str(i).accept()
