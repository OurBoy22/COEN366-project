import traceback
import generalFunctionsServer
import os
import base64
def putFilename(dict_in):
    #save the file into the server
    dict_out = {'success': False, 'error': ''}
    try:
        filename = dict_in['filename']
        print("FILE DATA:", dict_in['fileData'])
        #write into a file and save
        file = open(filename, 'wb')
        decoded_data = base64.b64decode(dict_in['fileData'])
        print(len(decoded_data))
        file.write(decoded_data)
        file.close()
        dict_out['success'] = True
        return dict_out
    except:
        print("Error saving file")
        traceback.print_exc()
        return dict_out

def getFilename(dict_in):
    dict_out = {'success': False, 'error': '', 'filename': '', 'fileData': '', 'filenameLen': '', 'fileSize': ''}
    try:
        filename = dict_in['filename']
        file = open(filename, 'rb')
        file_contents = file.read()
        file_contents = base64.b64encode(file_contents).decode('utf-8')
        file.close()
        dict_out['success'] = True
        dict_out['filename'] = filename
        dict_out['fileData'] = file_contents
        dict_out['fileSize'] = len(file_contents) +1
        dict_out['filenameLen'] = len(filename) + 1
        return dict_out
    except:
        print("Error getting file")
        traceback.print_exc()
        dict_out['error'] = "011"
        return dict_out
    
def changeFilename(dict_in):
    dict_out = {'success': False, 'error': ''}
    try:
        os.rename(dict_in['oldFilename'], dict_in['newFilename'])
        dict_out['success'] = True
        return dict_out
    except:
        print("Error changing file")
        traceback.print_exc()
        dict_out['error'] = "101"
        return dict_out
    
def summaryFile(dict_in):
    #TODO
    dict_out = {'success': False, 'error': '', 'filename': '', 'fileData': '', 'filenameLen': '', 'fileSize': ''}
    try:
        print("Here")
        fileToRead = dict_in["filename"]
        file = open(fileToRead, 'r')
        file_contents = file.read()
        file.close()

        splitContents = file_contents.split(',')
        nums = []
        for char in splitContents:
            nums.append(int(char))
        mininum = min(nums)
        maximum = max(nums)
        average = sum(nums)/len(nums)


        header = dict_in['filename'].split('.')

        newFileName =  header[0] + "_summary." + header[1]
        dict_out['filename'] = newFileName
        dict_out['filenameLen'] = len(newFileName) + 1
        fileToWrite = newFileName
        contentsToWrite = "Max is: " + str(maximum) + ", Min is: " + str(mininum) + ", Average is: " + str(average)
        
        #uncomment this to write the summary file into the server
        # file = open(fileToWrite, 'w')
        # file.write(contentsToWrite)
        # file.close()
        bytes_to_write = bytearray()

        dict_out['fileData'] = base64.b64encode(contentsToWrite.encode()).decode('utf-8')
        dict_out['fileSize'] = len(dict_out['fileData']) +1
        dict_out['success'] = True
        return dict_out
    except:
        print("Failed to generate summary file")
        traceback.print_exc()
        return dict_out



def help(dict_in):
    dict_out = {'success': False, 'error': '', 'message': ''}
    dict_out['success'] = True
    dict_out['message'] = "Help is not implemented yet"


