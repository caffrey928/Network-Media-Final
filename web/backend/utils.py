def uint8array_from_dict(str_dict):
    byte_array = bytearray(len(str_dict))
    
    for key, value in str_dict.items():
        byte_array[int(key)] = int(value)

    return bytes(byte_array)