import sys, socket, os

def socket_to_screen(socket, sock_addr):
	"""Reads data from a passed socket and prints it on screen.

	Returns either when a newline character is found in the stream or the connection is closed.
    The return value is the total number of bytes received through the socket.
	The second argument is prepended to the printed data to indicate the sender.
	"""

	print(sock_addr + ": ", end="", flush=True) # Use end="" to avoid adding a newline after the communicating partner's info, flush=True to force-print the info

	data = bytearray(1)
	bytes_read = 0
	print('socket to screen invoked')

	"""
	 Loop for as long as data is received (0-length data means the connection was closed by
	 the client), and newline is not in the data (newline means the complete input from the
	 other side was processed, as the assumption is that the client will send one line at
	 a time).
	"""
	while len(data) > 0 and "\n" not in data.decode():
		"""
		 Read up to 4096 bytes at a time; remember, TCP will return as much as there is
		 available to be delivered to the application, up to the user-defined maximum,
		 so it could as well be only a handful of bytes. This is the reason why we do
		 this in a loop; there is no guarantee that the line sent by the other side
		 will be delivered in one recv() call.
		"""
		data = socket.recv(4096)

		print(data.decode(), end="") # Use end="" to avoid adding a newline per print() call
		bytes_read += len(data)
	return bytes_read

def keyboard_to_socket(socket):
	"""Reads data from keyboard and sends it to the passed socket.
	
	Returns number of bytes sent, or 0 to indicate the user entered "EXIT"
	"""
	print("You: ", end="", flush=True) # Use end="" to avoid adding a newline after the prompt, flush=True to force-print the prompt

	# Read a full line from the keyboard. The returned string will include the terminating newline character.
	user_input = sys.stdin.readline()
	if user_input == "EXIT\n": # The user requested that the communication is terminated.
		return 0
	# find out if the client wants to use a put, get, or list command
	# in each case close out this function and call the respective function for the command
	user_input=user_input.strip('\n')
	userInputList=user_input.split(' ')
	if userInputList[0]=='put':
		put(socket, userInputList[1])
		return 0
	elif userInputList[0]=='get':
		get(socket, userInputList[1])
		return 0
	elif userInputList[0]=='list':
		list(socket)
		return 0

	# Send the whole line through the socket; remember, TCP provides no guarantee that it will be delivered in one go.
	bytes_sent = socket.sendall(str.encode(user_input))
	return bytes_sent

''' this function handles sending files to Server.py
# Parem0: cliSock -> the client socket
# Parem1: serSock -> the server socket
# Param2: fname -> the file name
# Param3: cliToSer -> client to server, to specify the direction of information

Param3 -- True by defualt, means that the information is being sent by the client to the server
If set to False -> the direction is inverted and the information is going the other way around
'''
def put(cliSock, serSock, fname, cliToSer=True) -> True:
# TODO: open the file in binary mode when this method is invoked
# 		read the data, send it to the server
#		close the connection

	''' 
	First we need to get the path of the file, to do this 
	we can do this by getting the parent path using the os library 
	and then check if the file is in the server or hte client folder
	to do this we can use the cliToServer argument and then we can 
	merger the path repectively
	'''

	# getting the path
	filePath=os.getcwd()
	filePath=os.path.dirname(filePath)

	# merge the paths
	if cliToSer: 
		filePath+='/client'
		print(filePath)
	else: 
		filePath+='/server' 
		print(filePath)

	if not (doesFileExist(fname)):
		with open(fname, 'wb') as f:
			f.write(fname.encode())
		f.close()

# this function handles recieveing files from Server.py
# Parem0: fname -> file name
# Parem1: socket -> socket
def get(socket, fname) -> True:
# TODO: create the file in binary mode when this method is invoked
# 		read the data sent by the server, store it in the file
# 		make sure not to overwrite the files that already exist
#		close the connection
	pass

# this function handles listing all the files in Server.py
# Parem0: socket -> socket
def list(socket) -> True:
	currentDir=os.getcwd()
	currentDir=os.path.dirname(currentDir)
	directories=os.listdir(currentDir)
	for i in directories: print(i)

# this function makes sure that the file does not exist when the get function is invoked
# Param0: fname -> file name
def doesFileExist(fname) -> bool:
	currentDir=os.getcwd()
	directories=os.listdir(currentDir)
	return (fname in directories)