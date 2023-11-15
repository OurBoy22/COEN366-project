import socket
import time
import traceback
import requestParseCommands
import serverProcessCommands
import generalFunctionsServer
import serverResponseGen
serverName = "localhost"
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

def getOpcode(commandIn):
    #get the first three bits of the command
    opcode = commandIn>>5
    print("OPCode is: " + bin(opcode))
    return opcode

def execCommand(commandIn):
    opcode = getOpcode(commandIn[0])
    if (opcode == 0b000): 
        print("put filename")
        dictOut = requestParseCommands.parsePutFilename(commandIn, getFilenameLength(commandIn[0]), opcode)
        # print(dictOut)
        response_dict = serverProcessCommands.putFilename(dictOut)
        # print(response_dict)
        return serverResponseGen.generatePutAndChangeResponse(response_dict)


    elif (opcode == 0b001):
        print("get filename")
        dictOut = requestParseCommands.parseGetFilename(commandIn, getFilenameLength(commandIn[0]), opcode)
        # print(dictOut)
        response_dict = serverProcessCommands.getFilename(dictOut)
        # print(response_dict)
        return serverResponseGen.generateGetResponse(response_dict)

        
    elif (opcode == 0b010):
        print("Change oldFilename newFilename")
        dictOut = requestParseCommands.changeOldFilenameNewFilename(commandIn, getFilenameLength(commandIn[0]), opcode)
        # print(dictOut)
        response_dict = serverProcessCommands.changeFilename(dictOut)
        # print(response_dict)
        return serverResponseGen.generatePutAndChangeResponse(response_dict)
        


    elif (opcode == 0b011):
        print("Summary filename")
        dictOut = requestParseCommands.summaryFilename(commandIn, getFilenameLength(commandIn[0]), opcode)
        print(dictOut)
        response_dict = serverProcessCommands.summaryFile(dictOut)
        print(response_dict)
        return serverResponseGen.generateStatResponse(response_dict)

    elif (opcode == 0b100):
        print("help")
    else:
        print("Invalid opcode")




def getFilenameLength(commandIn):
    fileNameLen = commandIn & 0b00011111
    print("Filename length is: " + bin(fileNameLen))
    return fileNameLen



    

while True:

    #assuming what you receive is bits
  

    # my_bytes.append(0b00001000)
    # my_bytes.extend('hel.txt'.encode())


    # a=  ":".join("{:02x}".format(ord(c)) for c in a)
    #get bytes of the string
    



    # print("\n\n------------------------------- Main Menu -------------------------------------")
    # print("Select your option: ")
    # print("1. Activate server")
    # print("2. Deactivate server")
    # userin = input()
    # if (userin == "1"):

        print('\n\n --------------Server listening for Connections-----------------')
        connectionSocket, addr = serverSocket.accept() # Accepts the connection
        
        
        request = ''
        while True:
            chunk = connectionSocket.recv(1024).decode(encoding='latin-1')
            print(chunk)
            if not chunk:
                break
            elif (len(chunk) < 1024):
                request += chunk
                break
            request += chunk
       
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
        print(request)
        # for byt in bytearray1:
        #     print(byt)
        # fileToSend = open("HelloServer.txt").read()  # open the html file and assign
        # fileLen = len(fileToSend)   # get the length of the html file
        # # response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: %i\r\n\r\n%s' % (fileLen, fileToSend) # double spacing at the end needed
        # response = fileToSend
        reponse = execCommand(bytearray1)
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










# def parseRequest(request):
#     print("\n\nParsing dictionary: ")
#     split_req = request.split('\r\n')
#     # print(split_req)

#     contentsArr = [] # stores the contents of dictionary
#     headersArr = [] # stores the keys of dictionary
#     for line in split_req: # Loop through every line of the request
#         header = ''
#         content = ''
#         headerFound = False
#         if ("GET" in line): # If the line contains GET, then it is the first line of the request
#             header = "GET"
#             content = line.replace("GET", "")
#         else:
#             for char in line: # Loop through every character of the line
#                 if (not headerFound): # If the header has not been found yet, then add the character to the header
#                     if char == ':': # If the character is a colon, then the header has been found
#                         headerFound = True
#                     else:
#                         header += char
#                 else:
#                     content += char
#                 # print("Header is: " + header)
#                 # print("Content is: " + content)
#         if (header != '' and content != ''): # If the header and content are not empty, then add them to their respective arrays
#             contentsArr.append(content)
#             headersArr.append(header)

#     # print("---------------CONTENTSARR---------")
#     # for x in contentsArr:
#     #     print(x)


#     # print("---------------HEADERSARR---------")
#     # for x in headersArr:
#     #     print(x)

#     print("\n\n----------DICTIONARY----------")
#     dictionary = {}
#     for i in range(0, len(contentsArr)): # Loop through the contents array and add the contents to the dictionary
#         dictionary[headersArr[i].strip()] = contentsArr[i].strip()

#     for key in dictionary: # Print the dictionary
#         print(key + ": " + dictionary[key])

#     return dictionary

# def checkDesiredFile(dictionary): # fetches the required file 
#     print("\n\nChecking desired file: ")
#     try:       
#         s ='' # stores the path of the request
#         for char in dictionary["GET"]: # Loop through every character of the GET request
#             if (char == " "): # If the character is a space, then the link has been found
#                 break
#             else:
#                 s += char

#         # as it is now, the s variable contains the path of the request in the form "/COEN366"
#         s = s.replace('/','') # remove the first slash
#         print(s)
#         return s
#     except (Exception):
#         print("Could not resolve the link of the request")
#         print(traceback.format_exc())



# while True:
#     connectionSocket, addr = serverSocket.accept() # Accepts the connection
#     print('accepting connection') 
#     request = connectionSocket.recv(1024).decode() # decode the client response
#     print('\n\nReceived Client Message')
#     print(request)

#     if (request != ''): # if the response is valid

#         dictionary = parseRequest(request) # parse the request and assign it to a dictionary
#         desiredFile = checkDesiredFile(dictionary) # check the desired path to reach (/COEN366 in this case)
       
#         try: # try to open the html file
#             print(desiredFile)
#             html_code = open(desiredFile +  ".html").read()  # open the html file and assign
#             html_len = len(html_code)   # get the length of the html file
#             response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: %i\r\n\r\n%s' % (html_len, html_code) # double spacing at the end needed
#         except: # if the file is not found, then send a not_found response
#             print("\n\nCould not locate the file based on the requested path") 
#             response = 'HTTP/1.1 404 Not Found\r\n'

#     else: # send not_found response if the request is invalid
#         print("\n\nInvalid response received")
#         response = 'HTTP/1.1 400 Bad Request\r\n'

#     #send response back and close connection
#     connectionSocket.send(response.encode()) # Use send all if needed
#     print('\n\nSending Response') 
#     print(response)
#     connectionSocket.close()
#     # time.sleep(4)