# Authors: Michael Hong, Luis Ramirez
# Description: This file contains the functions that process the commands sent by the client


import generalFunctionsServer as generalFunctions
def generateErrorResponse(dict_in): # for put and change 

    response = bytearray()
    if (dict_in['success'] == True): # if successful
        response.append(0b00000000) # append 
    else:
        # print("Error detected in put and change response")
        response.extend(handleError(dict_in))
    return response
def generatePutAndChangeResponse(dict_in): # for put and change 

    response = bytearray()
    if (dict_in['success'] == True): # if successful
        response.append(0b00000000) # append 
    else:
        print("Error detected in put and change response")
        response.extend(handleError(dict_in))
    return response

def generateGetResponse(dict_in): # for get request 
    response = bytearray()
    if (dict_in['success'] == True):
        op_code = (1 << 5 | (len(dict_in['filename']) + 1)) # shift left 5 bits and add the length of the filename + 1
        response.append(op_code) # append the opcode 
        response.extend(dict_in['filename'].encode()) # append the filename
        response.extend(generalFunctions.convertIntInto32bit(dict_in['fileSize'] + 1))  # append the filesize + 1
        response.extend(dict_in['fileData'].encode()) # append the filedata
        
    else:
        print("Error detected in get response")
        response.extend(handleError(dict_in))
    return response

def generateStatResponse(dict_in): # for stat request for file summary
    response = bytearray()
    if (dict_in['success'] == True):
        op_code = (1 << 6 | (len(dict_in['filename']) + 1))
        response.append(op_code)
        response.extend(dict_in['filename'].encode())
        response.extend(generalFunctions.convertIntInto32bit(dict_in['fileSize'] + 1)) 
        response.extend(dict_in['fileData'].encode())
    else:
        print("Error detected in stat response")
        response.extend(handleError(dict_in))
    return response

def generateHelpResponse(): # for help request
    command_help_string = """
        Command: put filename
        Description: Instructs the client to send a put request to the server, initiating the transfer of a file from the client machine to the server machine.
        Format: put <filename>
        Example: put file.txt

        Command: get filename
        Description: Instructs the client to send a get request to the server, retrieving a file from the server machine to the client machine.
        Format: get <filename>
        Example: get file.txt

        Command: summary filename
        Description: Instructs the client to send a summary request to the server, generating a statistical summary (maximum, minimum, and average) of a specific numeric file on the server. The server responds by sending a file containing the summary to the client.
        Format: summary <filename>
        Example: summary numbers.txt

        Command: change OldFileName NewFileName
        Description: Instructs the client to send a change request to the server, renaming a file on the server machine.
        Format: change <OldFileName> <NewFileName>
        Example: change oldfile.doc newfile.doc

        Command: help
        Description: Instructs the client to send a help request to the server, receiving a list of supported commands.
        Format: help
        Example: help

        Command: bye
        Description: Instructs the client to break the connection with the server and exit.
        Format: bye
        Example: bye
        """
    command_help_string = """
        put: Send file to server
        get: Retrieve file from server
        summary: Get stats of numeric file
        change: Rename a file on server
        help: Get list of commands   
        bye: Disconnect and exit
        """
    command_help_string = command_help_string.replace("        ", "")
    command_help_string = "put\nget\nsummary\nchange\nhelp\nbye"
    print(len(command_help_string)) 

    response = bytearray()
    response.append(generalFunctions.generate8bits(0b110, len(command_help_string))) #change the lenght parameter 
    response.extend(command_help_string.encode())
    return response


def handleError(dict_in): # handles errors
    errorCode = dict_in['error']
    if (errorCode == "011"): # file not found
        response = bytearray()
        response.append(0b01100000)
        return response
    elif (errorCode == "101"): # Unsuccessful change
        response = bytearray()
        response.append(0b10100000)
        return response
    elif (errorCode == "100"): # unkown request
        response = bytearray()
        response.append(0b10000000)
        return response
    else:
        response = bytearray()
        response.append(0b11111111)
        return response
    
        