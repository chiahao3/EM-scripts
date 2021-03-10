# This script take the emd file with DCFI dataset and output the shift vectors of it
# Script should be applied to a single Velox emd file, where the file contains only raw image stack and DCFI stack
# Modified from https://gist.github.com/thomasaarholt/768799db8c6f6e344a9b67f9561bccef 
# Chia-Hao Lee, 2021.03.10

import json
import h5py
import numpy as np
import os
from tifffile import imsave

def encoded_json_to_string(encoded):
    #Decodes json encoded as uint8 into string, then removes whitespace at end
    words = "".join(map(chr, encoded))
    word, _ = words.split('\n')
    return word

def get_shifts(filename):
    #Loops through a list of signals, grabs first DCFI signal found, gets shift from it
    with h5py.File(filename, 'r') as f:
        # Loops through available datasets, looking 
        for key in f['Data/Image'].keys():
            encoded = f['Data/Image/{}/Metadata'.format(key)][:].T
            first_frame = encoded[0]
            word = encoded_json_to_string(first_frame)
            if "ShiftMeasureResult" in word:
                break
        
        shiftsX = np.zeros(len(encoded))
        shiftsY = np.zeros(len(encoded))
        for i, frame in enumerate(encoded):
            word = encoded_json_to_string(frame)
            parsed = json.loads(word)

            x = float(parsed['CustomProperties']['ShiftMeasureResult.dx']['value'])
            y = float(parsed['CustomProperties']['ShiftMeasureResult.dy']['value'])
            shiftsX[i] = -x # We need how much to shift by, not how much it has been shifted
            shiftsY[i] = -y          
    f.close()
    return shiftsX, shiftsY

def getFilename(path):
    #This function go through the specified folder and return a list of emd filenames
    
    f_list = os.listdir(path)
    emdfile_list=[]
    # print f_list
    for i in f_list:    
        if os.path.splitext(i)[1] == '.emd':
            emdfile_list.append(os.path.splitext(i)[0])
    return emdfile_list

if __name__ == "__main__":
    '''
    This is the main body/entry of the script
    Go through the folder, get emd filenames
    Run the GetShift function for all emd file and output the vertical and horizontal shift
    '''
    path = "data//"
    fn_list = getFilename(path)
    shiftsX_list = []
    shiftsY_list = []

    for i, fn in enumerate(fn_list):
        fpath = path + fn + ".emd"
        print("Analyzing {}.".format(fpath))
        shiftsX, shiftsY = get_shifts(fpath)
        
        shiftsX_list.append(shiftsX)
        shiftsY_list.append(shiftsY)        
        
    imsave('Vertical_DCFI_shift.tif', np.float32(shiftsY_list))
    imsave('Horizontal_DCFI_shift.tif', np.float32(shiftsX_list))
    print("All done, shift vectors are saved!")	
