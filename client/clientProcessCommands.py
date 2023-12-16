# Authors: Michael Hong, Luis Ramirez
# Description: This file contains the functions that process the commands sent by the client


import traceback
import base64
def getFile(dict_in): # for get request, parses the filename and returns the file data 
    try:
        filename = dict_in['filename']
        file = open(filename, 'wb')
        
        decoded_data = base64.b64decode(dict_in['fileData'])
        chunk_size = 4096  # Adjust the chunk size as needed
        for i in range(0, len(decoded_data), chunk_size):
            file.write(decoded_data[i:i + chunk_size])
        # file_contents = file.write(decoded_data)
        # print("LENGTH 2 :",len(file_contents))
        file.close()
        return True
    except:
        print("Error Writing File into client")
        traceback.print_exc()
        return False
    
