from PIL import Image
import soundfile
import os
import struct

from utils import *

def read_file():
    filename = input("File to probe: ")

    file_found = False
    
    try:
        file = open(filename, "rb")
        file_found = True
    except:
        for extension in common_extensions:
            
            try:
                file = open(filename + extension, "rb")
                filename = filename + extension
                file_found = True
                break
            except FileNotFoundError:
                pass

    if not file_found:
        print("Can not find or open file.")
        quit()

    filesize = os.path.getsize(filename)

    data = []
    i = 0
    while i < filesize:
        try:
            data.append(file.read(1))
            i += 1
        except:
            break

    file.close()

    return data, filename

def write_audio(data, filename):
    sample_rate = 10500
    sample_rate_inp = input("Sample rate (default 10500):")

    if sample_rate_inp:
        try:
            sample_rate = int(sample_rate_inp)
        except:
            print("Could not interpret sample rate input. Defaulting to 42000...")
            pass
    
    exp_data = []
    max_float = 0

    for element_idx in range(0, len(data), 4):
        try:
            e = data[element_idx] + data[element_idx+1] + data[element_idx+2] + data[element_idx+3]
            exp_data.append(float(struct.unpack('f', e)[0]))

            if float(struct.unpack('f', e)[0]) > max_float:
                max_float = float(struct.unpack('f', e)[0])
                
        except:
            left_to_encode = len(data) - element_idx

            while left_to_encode > 0:
                e = data[element_idx]
                left_to_encode -= 1
                element_idx += 1
                
            e += bytearray(4 - len(e))
            exp_data.append(float(struct.unpack('f', e)[0]))
                
            if float(struct.unpack('f', e)[0]) > max_float:
                max_float = float(struct.unpack('f', e)[0])

    normalized_exp_data = []
    for element in exp_data:
        normalized_exp_data.append(element / max_float)

    filename = filename + ".wav"
        
    soundfile.write(filename, normalized_exp_data, sample_rate)

rawdata, filename = read_file()
write_audio(rawdata, filename)
