# Authors : Michael Hong, Luis Ramirez
# Description: This file contains the functions that process the commands sent by the client
def convertIntInto32bit(intIn): # converts an integer into a 32 bit bytearray
    x = bytearray()
    for i in range(0,4):
        shifted = ( (intIn >> (8*(3-i))) & 0x000000FF)
        x.append(shifted)
        # print("shifted is: ", shifted)
    # print("the 32 bit is: ", x)
    # for i in x:
    #     print(hex(i))
    return x

def generate8bits(opcode, size): # generates an 8 bit opcode and size
    if (opcode | size > 255):
        print("opcode and size must be 8 bits")
        return None
    else:
        return (opcode << 5 | size)