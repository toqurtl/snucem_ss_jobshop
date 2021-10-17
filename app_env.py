import os
import sys
import shutil

mode = sys.argv[1]
dir_name = sys.argv[2]
dir_path = "experiment/"+dir_name
if mode=="create":    
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            os.makedirs(dir_path+"/input")
            os.makedirs(dir_path+"/output")
            os.makedirs(dir_path+"/result")
            print('input 폴더에 input.xlsx을 넣어야 함')
        else:
            print('already exist')
    except OSError:
        print ('Error: Creating directory. ' +  dir_path)

elif mode=="delete":
    shutil.rmtree(dir_path)