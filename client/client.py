import socket
import time
import traceback
import generalFunctionsClient as generalFunctions
import responseParseCommands
import clientProcessCommands
import base64
import sys



def validateInput(userin):
    splitUserin = userin.split(" ")
    request = bytearray()
    if (len(splitUserin) > 3):
        print("invalid input")
        return False
    elif (len(splitUserin) == 2):
        if (splitUserin[0] == "put"):
            request.append(generalFunctions.generate8bits(0b000, len(splitUserin[1]) + 1)) #opcode + filename length
            request.extend(splitUserin[1].encode()) #filename
            try:
                fileToRead = open(splitUserin[1], 'rb')
                file_contents = fileToRead.read()
                file_contents = base64.b64encode(file_contents).decode('utf-8')
                print("LENGTH 1: ", len(file_contents))
                fileToRead.close()
                request.extend(generalFunctions.convertIntInto32bit(len(file_contents) + 1))  #file size
                request.extend(file_contents.encode()) #file data
                return request
            except:
                print("This file does not exist locally")
                return False
        elif (splitUserin[0] == "get"):
            request.append(generalFunctions.generate8bits(0b001, len(splitUserin[1]) + 1))
            request.extend(splitUserin[1].encode())
            return request
        elif (splitUserin[0] == "summary"):
            request.append(generalFunctions.generate8bits(0b011, len(splitUserin[1]) + 1))
            request.extend(splitUserin[1].encode())
            return request
        else:
            request.append(generalFunctions.generate8bits(0b111, 0))
            return request
       
    elif (len(splitUserin) == 3):
        if (splitUserin[0] == "change"):
            request.append(generalFunctions.generate8bits(0b010, len(splitUserin[1]) + 1)) # opcode + old filename length
            request.extend(splitUserin[1].encode()) # old filename
            request.append(len(splitUserin[2]) + 1) # new filename length
            request.extend(splitUserin[2].encode()) # new filename
            return request
        else:
            request.append(generalFunctions.generate8bits(0b111, 0))
            return request
    elif (len(splitUserin) == 1):
        if (splitUserin[0] == "help"):
            request.append(generalFunctions.generate8bits(0b100, 0))
            return request
        elif (splitUserin[0] == "bye"):
            return "quit"
        else:
            request.append(generalFunctions.generate8bits(0b111, 0))
            return request
    else:
        print("invalid input")
        return False
            

def getOpcode(commandIn):

    #get the first three bits of the command
    #print command in in hex
    hexCommand = hex(commandIn)
    print("command in is: ", hexCommand)
    opcode = commandIn>>5
    print("OPCode is: " + bin(opcode))
    return opcode

def execCommand(commandIn):
    opcode = getOpcode(commandIn[0])
    if (opcode == 0b000): 
        print("Put or change request was successful")
    elif (opcode == 0b001):
        print("Response to get request was successful")
        dictOut = responseParseCommands.parseGetFilename(commandIn, getFilenameLength(commandIn[0]), opcode)
        # print(dictOut)
        response_dict = clientProcessCommands.getFile(dictOut) 
    elif (opcode == 0b010):
        print("Receive Summary")
        dictOut = responseParseCommands.parseGetFilename(commandIn, getFilenameLength(commandIn[0]), opcode)
        # print(dictOut)
        response_dict = clientProcessCommands.getFile(dictOut)
    elif (opcode == 0b011):
        print("Error File not found")
    elif (opcode == 0b100):
        print("error unknown request")
    elif (opcode == 0b101):
        print("Unsuccessful change")
    elif (opcode == 0b110):
        print("help command")
        dictOut = responseParseCommands.parseHelpResponse(commandIn, getFilenameLength(commandIn[0]), opcode)
        # print(dictOut)
        print("The supported commands are: ")
        print(dictOut['fileData'])
        #TODO: print help command
    else:
        print("Invalid opcode")

def getFilenameLength(commandIn):
    fileNameLen = commandIn & 0b00011111
    print("Filename length is: " + bin(fileNameLen))
    return fileNameLen



clientSocket = None
serverName = ''
serverPort = ''
connectionType = ''

while True:
    try:
        serverName = input("Enter the server name: ")
        serverPort = int(input("Enter the server port: "))
        connectionType = input("Enter the connection type (TCP or UDP): ")
        #convert to uppercase
        if (connectionType.upper() == "TCP"):
            connectionType = socket.SOCK_STREAM
        elif (connectionType.upper() == "UDP"):
            connectionType = socket.SOCK_DGRAM
        else:
            raise TypeError("Invalid connection type")

    except:
        print("Invalid input")  

    try:
        # clientSocket
        if (connectionType == socket.SOCK_STREAM):
            clientSocket = socket.socket(socket.AF_INET, connectionType)
            clientSocket.connect((serverName, serverPort))
            clientSocket.send("ping".encode())
            if (clientSocket.recv(1024).decode(encoding='latin-1') == "pong"):
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
            if (data.decode(encoding='latin-1') == "pong"):
                clientSocket.close()
                print("Connection established")
                break
            else:
                print("Connection failed")
                clientSocket.close()
                raise TypeError("Connection failed")
    except:
        print("Failed to establish connection with the server")
        traceback.print_exc()


if (connectionType == socket.SOCK_STREAM):
    while True:
    
        print("\n\n------------------------------- Main Menu -------------------------------------")
        print("Select your option: ")
        userin = input()
        request = validateInput(userin)
        if (request == "quit"):
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
            # print(request)

            clientSocket.sendall(request)

            data = ''
            while True:
                chunk = clientSocket.recv(1024).decode(encoding='latin-1')
                # print(chunk)
                # if not chunk:
                #     break
                # elif (len(chunk) < 1024):
                #     data += chunk
                #     break
                if not chunk:
                    break
                data += chunk
            
            
            # print("LENGHT1: " ,len(data))
            # data = clientSocket.recv(1024).decode(encoding='latin-1')

            


            print("----------------------Data received from server: ----------------------")
            bytearray1 = bytearray()
            bytearray1.extend(data.encode(encoding='latin-1'))
            print(bytearray1)
            execCommand(bytearray1)
            # print(bytearray1)
        
            # print("LENGHT1: " ,len(data))

            clientSocket.close()


else:
    clientSocket = socket.socket(socket.AF_INET, connectionType)
    while True:
        print("UDP")
        print("\n\n------------------------------- Main Menu -------------------------------------")
        print("Select your option: ")
        userin = input()
        request = validateInput(userin)
        if (request == "quit"):
            break

        elif (request != False):
            clientSocket = socket.socket(socket.AF_INET, connectionType)
            clientSocket.connect((serverName, serverPort))
  
            print("----------------------Sending data to server: ----------------------")
            # print(request)

            # clientSocket.sendto(request, (serverName, serverPort))
            bytesSend = bytearray()
            bytesSend.extend(str(len(request)).encode(encoding='latin-1'))
            clientSocket.sendto(bytesSend, server_address)
            # next_index, client_address = serverSocket.recvfrom(1024)
            for i in range(0, len(request), 1024):
                chunk = request[i:i + 1024]
                clientSocket.sendto(chunk, server_address)
                ack, server_address = clientSocket.recvfrom(1024)
                print(ack)

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
            print("LENGTH TO RECEIVE: ", length_to_receive)
            while len(data) < length_to_receive:
                chunk, server_address = clientSocket.recvfrom(1024)
                print('/n CHUNK: ', current_count)
                print(chunk)
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
            print(bytearray1)
            execCommand(bytearray1)
            # print(bytearray1)
        
            # print("LENGHT1: " ,len(data))

            clientSocket.close()
    clientSocket.close()

