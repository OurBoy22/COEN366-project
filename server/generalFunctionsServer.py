def convertIntInto32bit(intIn):
    x = bytearray()
    for i in range(0,4):
        shifted = ( (intIn >> (8*(3-i))) & 0x000000FF)
        x.append(shifted)
        # print("shifted is: ", shifted)
    # print("the 32 bit is: ", x)
    # for i in x:
    #     print(hex(i))
    return x

def generate8bits(opcode, size):
    if (opcode | size > 255):
        print("opcode and size must be 8 bits")
        return None
    else:
        return (opcode << 5 | size)