import generalFunctionsServer as generalFunctions
def generatePutAndChangeResponse(dict_in): # for put and change 
    response = bytearray()
    if (dict_in['success'] == True):
        response.append(0b00000000)
    else:
        handleError(dict_in)
    return response

def generateGetResponse(dict_in): # for get request 
    response = bytearray()
    if (dict_in['success'] == True):
        op_code = (1 << 5 | (len(dict_in['filename']) + 1))
        response.append(op_code)
        response.extend(dict_in['filename'].encode())
        response.extend(generalFunctions.convertIntInto32bit(dict_in['fileSize'] + 1)) 
        response.extend(dict_in['fileData'].encode())
        
    else:
        handleError(dict_in)
    return response

def generateStatResponse(dict_in):
    response = bytearray()
    if (dict_in['success'] == True):
        op_code = (1 << 6 | (len(dict_in['filename']) + 1))
        response.append(op_code)
        response.extend(dict_in['filename'].encode())
        response.extend(generalFunctions.convertIntInto32bit(dict_in['fileSize'] + 1)) 
        response.extend(dict_in['fileData'].encode())
    else:
        handleError(dict_in)
    return response


def handleError(dict_in):
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
    
        