import socket
import time
import traceback
import generalFunctionsClient as generalFunctions
import responseParseCommands
import clientProcessCommands
import base64

serverName = "localhost"
serverPort = 12000

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
            fileToRead = open(splitUserin[1], 'rb')
            file_contents = fileToRead.read()
            file_contents = base64.b64encode(file_contents).decode('utf-8')
            print("LENGTH 1: ", len(file_contents))
            fileToRead.close()
            request.extend(generalFunctions.convertIntInto32bit(len(file_contents) + 1))  #file size
            request.extend(file_contents.encode()) #file data
            return request
        elif (splitUserin[0] == "get"):
            request.append(generalFunctions.generate8bits(0b001, len(splitUserin[1]) + 1))
            request.extend(splitUserin[1].encode())
            return request
        elif (splitUserin[0] == "summary"):
            request.append(generalFunctions.generate8bits(0b011, len(splitUserin[1]) + 1))
            request.extend(splitUserin[1].encode())
            return request
       
    elif (len(splitUserin) == 3):
        if (splitUserin[0] == "change"):
            request.append(generalFunctions.generate8bits(0b010, len(splitUserin[1]) + 1)) # opcode + old filename length
            request.extend(splitUserin[1].encode()) # old filename
            request.append(len(splitUserin[2]) + 1) # new filename length
            request.extend(splitUserin[2].encode()) # new filename
            return request
    elif (len(splitUserin) == 1):
        if (splitUserin[0] == "help"):
            request.append(generalFunctions.generate8bits(0b110, 0))
            return request
        elif (splitUserin[0] == "bye"):
            return "quit"
    else:
        print("invalid input")
        return False
            

def getOpcode(commandIn):
    #get the first three bits of the command
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
        #TODO: print help command
    else:
        print("Invalid opcode")





def getFilenameLength(commandIn):
    fileNameLen = commandIn & 0b00011111
    print("Filename length is: " + bin(fileNameLen))
    return fileNameLen


            

while True:
    print("\n\n------------------------------- Main Menu -------------------------------------")
    print("Select your option: ")
    userin = input()
    request = validateInput(userin)
    if (request == "quit"):
        break

    elif (request != False):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
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
            if not chunk:
                break
            data += chunk
        
        # print("LENGHT1: " ,len(data))
        # data = clientSocket.recv(1024).decode(encoding='latin-1')

        


        print("----------------------Data received from server: ----------------------")
        
        bytearray1 = bytearray()
        bytearray1.extend(data.encode())
        # print(bytearray1)
       
        # print("LENGHT1: " ,len(data))

        clientSocket.close()
