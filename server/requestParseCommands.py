def parsePutFilename(commandIn, filenameLen, opcode):
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
    print("File size is: " + bin(dictOut["fileSize"]))
    
    for i in range(1+ len(dictOut["filename"]) + 4 , len(commandIn)):
        dictOut["fileData"] += chr(commandIn[i])
    
    # print(dictOut)
    return dictOut

def parseGetFilename(commandIn, filenameLen, opcode):
    dictOut = {"command": commandIn, "filenameLen": filenameLen, "opcode": opcode, "filename": ""}
    filename = ""
    for i in range(1, filenameLen):
        #convert byte to char
        filename += chr(commandIn[i])
        # print(i , " " , chr(commandIn[i]))
    
    dictOut["filename"] = filename
    
    # print(dictOut)
    return dictOut

def changeOldFilenameNewFilename(commandIn, filenameLen, opcode):
    dictOut = {"command": commandIn, "oldFilenameLen": filenameLen, "oldFileName": "", "opcode": opcode, "newFileNameLen": '', "newFilename": ""}
    oldFilename = ""
    for i in range(1, filenameLen):
        #convert byte to char
        oldFilename += chr(commandIn[i])
        # print(i , " " , chr(commandIn[i])
     
    dictOut["oldFilename"] = oldFilename
    dictOut["newFileNameLen"] = int(commandIn[filenameLen])

    newFilename = ""

    for i in range( filenameLen+1 ,filenameLen + dictOut["newFileNameLen"]):
        #convert byte to char
        newFilename += chr(commandIn[i])
        print(i , " " , chr(commandIn[i]))
    dictOut["newFilename"] = newFilename
    # print(dictOut)
    return dictOut

def summaryFilename(commandIn, filenameLen, opcode):
    dictOut = {"command": commandIn, "filenameLen": filenameLen, "opcode": opcode, "filename": ""}
    fileName = ''
    for i in range(1, filenameLen):
        #convert byte to char
        fileName += chr(commandIn[i])
        # print(i , " " , chr(commandIn[i])
    dictOut["filename"] = fileName
    return dictOut