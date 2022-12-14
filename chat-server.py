import socket
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = "localhost"
Port = 65432

server.bind((IP_address, Port))

server.listen(100)

list_of_clients = []

def clientthread(conn, addr):
	conn.send("Bem vindo!\n".encode('UTF-8'))

	while True:
			try:
				message = conn.recv(2048)
				message = message.decode('UTF-8')

				if message:
					print ("<" + addr[0] + "> " + message)
					message_to_send = "<" + addr[0] + "> " + message
					broadcast(message_to_send, conn)

				else:
					remove(conn)

			except:
				continue

def broadcast(message, connection):
	for clients in list_of_clients:
		if clients!=connection:
			try:
				clients.send(message.encode('UTF-8'))
			except:
				clients.close()
				remove(clients)

def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:
	conn, addr = server.accept()
	list_of_clients.append(conn)

	print (addr[0] + " ta ON!")
	start_new_thread(clientthread,(conn,addr))

