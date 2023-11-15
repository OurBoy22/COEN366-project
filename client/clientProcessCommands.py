import traceback
import base64
def getFile(dict_in):
    try:
        filename = dict_in['filename']
        file = open(filename, 'wb')
        decoded_data = base64.b64decode(dict_in['fileData'])
        file_contents = file.write(decoded_data)
        # print("LENGTH 2 :",len(file_contents))
        file.close()
        return True
    except:
        print("Error Writing File into client")
        traceback.print_exc()
        return False
    
