# Authors: Michael Hong and Luis Ramirez
# Description: This file contains the client side of the program. It will send requests to the server and receive responses from the server. It will also display the responses to the user.


import socket
import time
import traceback
import generalFunctionsClient as generalFunctions
import responseParseCommands
import clientProcessCommands
import base64
import sys


def validateInput(userin): #returns a bytearray with the request or False if the input from the user is invalid
    splitUserin = userin.split(" ") #split the user input into a list
    request = bytearray() #create the bytearray to be returned
    if (len(splitUserin) > 3): #if the user input is more than 3 words, it is invalid
        print("invalid input")
        return False
    elif (len(splitUserin) == 2): #if the user input is 2 words
        if (splitUserin[0] == "put"): #if the first word is put, create packet for put request
            request.append(generalFunctions.generate8bits(0b000, len(splitUserin[1]) + 1)) #opcode + filename length
            request.extend(splitUserin[1].encode()) #filename
            try:
                fileToRead = open(splitUserin[1], 'rb') #open the file to read
                file_contents = fileToRead.read()
                file_contents = base64.b64encode(file_contents).decode('utf-8') #encode the file contents in base64
                # print("LENGTH 1: ", len(file_contents))
                fileToRead.close()
                request.extend(generalFunctions.convertIntInto32bit(len(file_contents) + 1))  #file size
                request.extend(file_contents.encode()) #file data
                return request
            except: #if the file does not exist, return false and printout message
                print("This file does not exist locally")
                return False
        elif (splitUserin[0] == "get"): #if the first word is get, create packet for get request
            request.append(generalFunctions.generate8bits(0b001, len(splitUserin[1]) + 1)) #opcode + filename length
            request.extend(splitUserin[1].encode()) #filename
            return request
        elif (splitUserin[0] == "summary"): #if the first word is summary, create packet for summary request
            request.append(generalFunctions.generate8bits(0b011, len(splitUserin[1]) + 1)) #opcode + filename length
            request.extend(splitUserin[1].encode()) #filename
            return request
        else:
            request.append(generalFunctions.generate8bits(0b111, 0)) #if the first word is not put, get, or summary, return invalid opcode
            return request
       
    elif (len(splitUserin) == 3): 
        if (splitUserin[0] == "change"): #if the first word is change, create packet for change request
            request.append(generalFunctions.generate8bits(0b010, len(splitUserin[1]) + 1)) # opcode + old filename length
            request.extend(splitUserin[1].encode()) # old filename
            request.append(len(splitUserin[2]) + 1) # new filename length
            request.extend(splitUserin[2].encode()) # new filename
            return request
        else:
            request.append(generalFunctions.generate8bits(0b111, 0)) #if the first word is not change, return invalid opcode
            return request
    elif (len(splitUserin) == 1):
        if (splitUserin[0] == "help"): #if the first word is help, create packet for help request
            request.append(generalFunctions.generate8bits(0b100, 0)) #opcode
            return request
        elif (splitUserin[0] == "bye"): #if the first word is bye, create packet for bye request
            return "quit"
        else:
            request.append(generalFunctions.generate8bits(0b111, 0)) #if the first word is not help or bye, return invalid opcode
            return request
    else: #if the user input is 0 words, it is invalid
        print("invalid input")
        return False
            

def getOpcode(commandIn):
    #get the first three bits of the command
    hexCommand = hex(commandIn)
    # print("command in is: ", hexCommand)
    opcode = commandIn>>5
    # print("OPCode is: " + bin(opcode))
    return opcode

def execCommand(commandIn): #executes the command received from the server
    opcode = getOpcode(commandIn[0])
    if (opcode == 0b000): #if the opcode is 0, it is a put or change request
        print("Put or change request was successful")
    elif (opcode == 0b001): #if the opcode is 1, it is a get request
        print("Response to get request was successful")
        dictOut = responseParseCommands.parseGetFilename(commandIn, getFilenameLength(commandIn[0]), opcode)
        # print(dictOut)
        response_dict = clientProcessCommands.getFile(dictOut) 
    elif (opcode == 0b010): # if the opcode is 2, it is a response with a file containing a summary
        print("Receive Summary")
        dictOut = responseParseCommands.parseGetFilename(commandIn, getFilenameLength(commandIn[0]), opcode)
        # print(dictOut)
        response_dict = clientProcessCommands.getFile(dictOut)
    elif (opcode == 0b011): #if the opcode is 3, it means that the file requested does not exist
        print("Error File not found")
    elif (opcode == 0b100): #if the opcode is 4, it means that it is not a valid request
        print("error unknown request")
    elif (opcode == 0b101): # if the opcode was 5, it means that the file name change was unsuccessful
        print("Unsuccessful change")
    elif (opcode == 0b110): #response for help command
        print("help command")
        dictOut = responseParseCommands.parseHelpResponse(commandIn, getFilenameLength(commandIn[0]), opcode)
        # print(dictOut)
        print("The supported commands are: ")
        print(dictOut['fileData'])

    else: #if the opcode is not 0, 1, 2, 3, 4, or 5, it is an invalid opcode
        print("Invalid opcode")

def getFilenameLength(commandIn): #gets the filename length from the command
    fileNameLen = commandIn & 0b00011111
    print("Filename length is: " + bin(fileNameLen))
    return fileNameLen


#This code below is to initiate and test that the connection is successful and that the server is running
clientSocket = None
serverName = ''
serverPort = ''
connectionType = ''

while True: #loop to get the server name, port, and connection type from the user
    try: 
        serverName = input("Enter the server name: ")
        serverPort = int(input("Enter the server port: "))
        connectionType = input("Enter the connection type (TCP or UDP): ")
        #convert to uppercase
        if (connectionType.upper() == "TCP"): #if the connection type is TCP, set the connection type to socket.SOCK_STREAM
            connectionType = socket.SOCK_STREAM
        elif (connectionType.upper() == "UDP"): #if the connection type is UDP, set the connection type to socket.SOCK_DGRAM
            connectionType = socket.SOCK_DGRAM
        else:
            raise TypeError("Invalid connection type")

    except:
        print("Invalid input")  

    try:
        # clientSocket
        if (connectionType == socket.SOCK_STREAM): #attempt to create a TCP connection
            clientSocket = socket.socket(socket.AF_INET, connectionType)
            clientSocket.connect((serverName, serverPort))
            clientSocket.send("ping".encode())
            if (clientSocket.recv(1024).decode(encoding='latin-1') == "pong"): #if the server responds with pong, the connection was successful
                clientSocket.close()
                print("Connection established")
                break
            else:
                print("Connection failed")
                clientSocket.close()
                raise TypeError("Connection failed")
        else:
            print("UDP")
            clientSocket = socket.socket(socket.AF_INET, connectionType)
            clientSocket.sendto("ping".encode(), (serverName, serverPort))
            data, server_address = clientSocket.recvfrom(1024)
            if (data.decode(encoding='latin-1') == "pong"): #if the server responds with pong, the connection was successful
                clientSocket.close()
                print("Connection established")
                break
            else:
                print("Connection failed")
                clientSocket.close()
                raise TypeError("Connection failed")
    except: #if the connection fails, print out error message and traceback
        print("Failed to establish connection with the server")
        traceback.print_exc()


if (connectionType == socket.SOCK_STREAM): #if the connection type is TCP, enter the TCP loop to send requests to the server
    while True:
    
        print("\n\n------------------------------- Main Menu -------------------------------------")
        print("Select your option: ")
        userin = input()
        request = validateInput(userin)
        if (request == "quit"): # if the validation of the user input returns quit, break out of the loop
            break

        elif (request != False):
            # clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # clientSocket.connect((serverName, serverPort))
            clientSocket = socket.socket(socket.AF_INET, connectionType)
            clientSocket.connect((serverName, serverPort))
            # print(clientSocket)
            # # clientSocket.sendall(b"Hello from the Client")
            # my_bytes = bytearray()
            # # my_bytes.append(0b00010000)
            # my_bytes.append(0b01101100)
            # # my_bytes.append(0b01101100)
            # print(my_bytes)
            # fileName = 'numbers.txt'
            # my_bytes.extend('numbers.txt'.encode())
            # # a = 'File Modified'
            # # my_bytes.extend(generalFunctions.convertIntInto32bit(len('numbers.txt') + 1)) 
            # # my_bytes.extend(a.encode())
            # print(my_bytes)
            # for byt in my_bytes:
            #     print(hex(byt))
            print("----------------------Sending data to server: ----------------------")
            print(request)

            clientSocket.sendall(request) #send the request to the server

            data = ''
            while True:
                chunk = clientSocket.recv(1024).decode(encoding='latin-1') #receive the data in chunks of 1024 bytes
                # print(chunk)
                # if not chunk:
                #     break
                # elif (len(chunk) < 1024):
                #     data += chunk
                #     break
                if not chunk: #if the chunk is empty, break out of the loop
                    break 
                data += chunk #add the chunk to the data
            
            
            # print("LENGHT1: " ,len(data))
            # data = clientSocket.recv(1024).decode(encoding='latin-1')

            


            print("----------------------Data received from server: ----------------------")
            bytearray1 = bytearray()
            bytearray1.extend(data.encode(encoding='latin-1'))
            # print(bytearray1)
            execCommand(bytearray1)
            # print(bytearray1)
        
            # print("LENGHT1: " ,len(data))

            clientSocket.close()


else: #if the connection type is UDP, enter the UDP loop to send requests to the server
    clientSocket = socket.socket(socket.AF_INET, connectionType)
    while True:
        # print("UDP")
        print("\n\n------------------------------- Main Menu -------------------------------------")
        print("Select your option: ")
        userin = input()
        request = validateInput(userin)
        if (request == "quit"): # if the validation of the user input returns quit, break out of the loop
            break

        elif (request != False):
            clientSocket = socket.socket(socket.AF_INET, connectionType)
            clientSocket.connect((serverName, serverPort))
  
            print("----------------------Sending data to server: ----------------------")
            print(request)

            # clientSocket.sendto(request, (serverName, serverPort))
            bytesSend = bytearray()
            bytesSend.extend(str(len(request)).encode(encoding='latin-1'))
            clientSocket.sendto(bytesSend, server_address)
            # next_index, client_address = serverSocket.recvfrom(1024)
            for i in range(0, len(request), 1024): #send the request in chunks of 1024 bytes
                chunk = request[i:i + 1024]
                clientSocket.sendto(chunk, server_address)
                ack, server_address = clientSocket.recvfrom(1024)
                # print(ack)

            data = ''
            # while True:
            #     chunk = clientSocket.recv(1024).decode(encoding='latin-1')
            #     # print(chunk)
            #     # if not chunk:
            #     #     break
            #     # elif (len(chunk) < 1024):
            #     #     data += chunk
            #     #     break
            #     if not chunk:
            #         break
            #     data += chunk
            current_count = 0
            length_to_receive, server_address = clientSocket.recvfrom(1024)
            length_to_receive = int(length_to_receive.decode(encoding='latin-1'))
            # print("LENGTH TO RECEIVE: ", length_to_receive)
            while len(data) < length_to_receive: #while the length of the data received is less than the length of the data to receive
                chunk, server_address = clientSocket.recvfrom(1024)
                # print('/n CHUNK: ', current_count)
                # print(chunk)
                # time.sleep(0.5)
                clientSocket.sendto("1".encode(), server_address)
                data += chunk.decode(encoding='latin-1')
                current_count += 1
            # data, server_address = clientSocket.recvfrom(1024)
            # data = data.decode(encoding='latin-1')
            
            
            # print("LENGHT1: " ,len(data))
            # data = clientSocket.recv(1024).decode(encoding='latin-1')

            


            print("----------------------Data received from server: ----------------------")
            bytearray1 = bytearray()
            bytearray1.extend(data.encode(encoding='latin-1'))
            # print(bytearray1)
            execCommand(bytearray1) #execute the command received from the server
            # print(bytearray1)
        
            # print("LENGHT1: " ,len(data))

            clientSocket.close()
    clientSocket.close()

