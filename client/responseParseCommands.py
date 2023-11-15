def parseGetFilename(commandIn, filenameLen, opcode):
    #get the first three bits of the command
    dictOut = {"command": commandIn, "filenameLen": filenameLen, "opcode": opcode, "filename": "", 'fileData' : '', 'fileSize': ''}

    filename = ""
    for i in range(1, filenameLen):
        #convert byte to char
        filename += chr(commandIn[i])
        # print(i , " " , chr(commandIn[i]))

    dictOut["filename"] = filename   

    # dictOut["filename"] = filename
    filesize = 0
    for i in range(filenameLen ,1+ len(dictOut["filename"])+4):
        filesize += commandIn[i]
    dictOut["fileSize"] = filesize 
    # print("File size is: " + bin(dictOut["fileSize"]))
    
    for i in range(1+ len(dictOut["filename"]) + 4 , len(commandIn)): #TODO: fix boundary with the -1
        # print(chr(commandIn[i]))
        dictOut["fileData"] += chr(commandIn[i])
    
    # print(dictOut)
    return dictOut

