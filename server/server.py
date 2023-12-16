# Authors: Michael Hong, Luis Ramirez
# Description: This file contains the functions that process the commands sent by the client

import socket
import time
import traceback
import requestParseCommands
import serverProcessCommands
import generalFunctionsServer
import serverResponseGen
serverName = "127.0.0.1" # IP address of the server, can be changed to any IP address
serverPort = 12000 # Port number of the server, can be changed to any port number

connectionType = "TCP"
while True: # while loop to get the connection type
    connectionType = input("Enter type of connection (TCP or UDP): ")
    if (connectionType.upper() == "TCP"): # if TCP, create a TCP socket
        connectionType = socket.SOCK_STREAM
        serverSocket = socket.socket(socket.AF_INET, connectionType)
        serverSocket.bind((serverName, serverPort))
        break
    elif (connectionType.upper() == "UDP"): # if UDP, create a UDP socket
        connectionType = socket.SOCK_DGRAM
        serverSocket = socket.socket(socket.AF_INET, connectionType)
        serverSocket.bind((serverName, serverPort))
        break
    else:
        print("Invalid input, please try again")
  
print("The server is now listening for connections on port " + str(serverPort) + " on IP address " + serverName)

def getOpcode(commandIn): # function to get the opcode from the command
    #get the first three bits of the command
    opcode = commandIn>>5
    print("OPCode is: " + bin(opcode))
    return opcode

def execCommand(commandIn): # function to execute the command
    # print("executing command" + str(commandIn))
    opcode = getOpcode(commandIn[0])
    if (opcode == 0b000):  # put filename
        print("put filename")
        dictOut = requestParseCommands.parsePutFilename(commandIn, getFilenameLength(commandIn[0]), opcode)
        # print(dictOut)
        response_dict = serverProcessCommands.putFilename(dictOut)
        # print(response_dict)
        return serverResponseGen.generatePutAndChangeResponse(response_dict)


    elif (opcode == 0b001): # get filename
        print("get filename")
        dictOut = requestParseCommands.parseGetFilename(commandIn, getFilenameLength(commandIn[0]), opcode)
        # print(dictOut)
        response_dict = serverProcessCommands.getFilename(dictOut)
        # print(response_dict)
        return serverResponseGen.generateGetResponse(response_dict)

        
    elif (opcode == 0b010): # change oldFilename newFilename
        print("Change oldFilename newFilename")
        dictOut = requestParseCommands.changeOldFilenameNewFilename(commandIn, getFilenameLength(commandIn[0]), opcode)
        # print(dictOut)
        response_dict = serverProcessCommands.changeFilename(dictOut)
        # print(response_dict)
        return serverResponseGen.generatePutAndChangeResponse(response_dict)
        


    elif (opcode == 0b011): # summary filename
        print("Summary filename")
        dictOut = requestParseCommands.summaryFilename(commandIn, getFilenameLength(commandIn[0]), opcode)
        # print(dictOut)
        response_dict = serverProcessCommands.summaryFile(dictOut)
        # print(response_dict)
        return serverResponseGen.generateStatResponse(response_dict)

    elif (opcode == 0b100): # help
        print("help")
        return serverResponseGen.generateHelpResponse()


       
    else: # invalid opcode
        print("Invalid opcode")
        # test = serverResponseGen.handleError({'success': False, 'error': '100'})
        test = serverResponseGen.generateErrorResponse({'success': False, 'error': '100'})
        # print(test)
        return test




def getFilenameLength(commandIn): # function to get the filename length from the command
    fileNameLen = commandIn & 0b00011111
    print("Filename length is: " + bin(fileNameLen))
    return fileNameLen



    
if (connectionType == socket.SOCK_STREAM): # TCP
    serverSocket.listen(1)
    while True:

            print('\n\n --------------Server listening for Connections-----------------')
            connectionSocket, addr = serverSocket.accept() # Accepts the connection
            
            
            request = ''
            i = 0
            while True:  # while loop to receive the client request
                chunk = connectionSocket.recv(1024).decode(encoding='latin-1') # receive the client request
                # print("Chunk: ", i)
                # print(len(chunk)) 
                if not chunk:  # if the chunk is empty, break
                    break
                elif (len(chunk) < 1024): # if the chunk is less than 1024, break
                    request += chunk
                    break
                request += chunk
                time.sleep(0.01)
        
            bytearray1 = bytearray() 
            # request = request.decode() # decode the client response
            my_bytes = request
            bytearray1.extend(request.encode(encoding='latin-1'))
            # request = connectionSocket.recv(1024)
            # print(request)
            # bytearray1 = bytearray()
            # request = request.decode() # decode the client response
            # my_bytes = request
            # bytearray1.extend(request.encode(encoding='latin-1'))
            print('\n\n --------------Received Client Message-----------------')
            # print(request)
            # for byt in bytearray1:
            #     print(byt)
            # fileToSend = open("HelloServer.txt").read()  # open the html file and assign
            # fileLen = len(fileToSend)   # get the length of the html file
            # # response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: %i\r\n\r\n%s' % (fileLen, fileToSend) # double spacing at the end needed
            # response = fileToSend
            if (request == 'ping'): # if the client sends a ping, send a pong
                print("Received ping from client")
                connectionSocket.sendall("pong".encode())
            else: # otherwise, execute the command
                reponse = execCommand(bytearray1)
                # print("Response is: " + str(reponse))
                # print(reponse)
                # print("length of response is: " , len(reponse))
                connectionSocket.sendall(reponse) # Use send all if needed
            # print('\n\nSending Response') 
            # print(response)
            connectionSocket.close()
        # elif (userin == "2"):
        #     print("Deactivating server")
        #     break
        # else:
        #     print("Invalid input, Please try again")




else: # UDP
        while True:

            

            print('\n\n --------------Server listening for Connections-----------------')
            
            length_to_receive, client_address = serverSocket.recvfrom(1024)
            length_to_receive = (length_to_receive.decode(encoding='latin-1'))
            if (length_to_receive == 'ping'):
                print("Received ping from client")
                serverSocket.sendto("pong".encode(), client_address)
            else:
                
                
                length_to_receive = int(length_to_receive)
                print("LENGTH TO RECEIVE: ", length_to_receive)
                data = ''
                current_count = 0
                while len(data) < length_to_receive: # while loop to receive the client request
                    chunk, server_address = serverSocket.recvfrom(1024)
                    # print('/n CHUNK: ', current_count)
                    # print(chunk)
                    # time.sleep(0.5)
                    serverSocket.sendto("0".encode(), client_address)
                    data += chunk.decode(encoding='latin-1')
                    current_count += 1
                
                bytearray1 = bytearray()
                # request = request.decode() # decode the client response
                bytearray1.extend(data.encode(encoding='latin-1'))

                reponse = execCommand(bytearray1)
                # print("Response is: " + str(reponse))
                

                bytesSend = bytearray()
                bytesSend.extend(str(len(reponse)).encode(encoding='latin-1'))
                serverSocket.sendto(bytesSend, client_address)
                # next_index, client_address = serverSocket.recvfrom(1024)
                for i in range(0, len(reponse), 1024): # while loop to send the response to the client in chunks of 1024 bytes
                    chunk = reponse[i:i + 1024]
                    serverSocket.sendto(chunk, client_address)
                    ack, client_address = serverSocket.recvfrom(1024)
                    # print(ack)
                # request = data.decode(encoding='latin-1')
            
               
                # print(reponse)
                # print("length of response is: " , len(reponse))
                # request = connectionSocket.recv(1024)
                # print(request)
                # bytearray1 = bytearray()
                # request = request.decode() # decode the client response
                # my_bytes = request
                # bytearray1.extend(request.encode(encoding='latin-1'))
                # print('\n\n --------------Received Client Message-----------------')
                # print(request)
                # for byt in bytearray1:
                #     print(byt)
                # fileToSend = open("HelloServer.txt").read()  # open the html file and assign
                # fileLen = len(fileToSend)   # get the length of the html file
                # # response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: %i\r\n\r\n%s' % (fileLen, fileToSend) # double spacing at the end needed
                # response = fileToSend
            
                    # serverSocket.sendto(reponse, client_address)
                # print('\n\nSending Response') 
                # print(response)
                # connectionSocket.close()
       




