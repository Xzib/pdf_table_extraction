import os
import sys
from pdf2image import convert_from_path
import time
import cv2 
import json
import numpy as np
import re
from table_extract import extract_table, pdf_table
from tesseract_ocr_test import highlight_text
from Delete_OCR import delete_files
from json_format import JSON_Create_Form#JSON_Create_Form_B, JSON_Create_Form_C, JSON_Create_Form_F,JSON_Create_Form_D,JSON_Create_Form_E


def apply_reg(comp_reg,text_val):
    # print(text_val)
    x = re.search(comp_reg,text_val)
    if x != None:
        # print(x)
        return x.group() 
    # print(x)
    return x
def swapvalues(val:list):
    for i in range(0,len(val)-1,2):
        val[i],val[i+1]=val[i+1],val[i]
    return val

def helper_function(img,flag_image = 0):
    
    if flag_image == 1:
        # os.chdir(r".\cropped")
        text = extract_table(img)
        spaces = re.compile(r'^\d{1,2}\.$')
        # text = list(filter(lambda x : x != " ",text))
        # print(text)
        temp = {}
        val = list(map(lambda x : x.strip(),text)) 
        val = list(filter(lambda x: x!='',val))
        val = list(filter(lambda x : x != apply_reg(spaces,x) ,val))

        print(val)
        if len(val)>0:
            if (val[0] == "particulars") or (val[0] == "relevant particulars"):
                # temp = {val[k]:"" for k in range(1,len(val)) if k%2!=0}
                # val_val = [val[x] for x in range(1,len(val)) if x%2==0]
                val.remove(val[0])
                val = swapvalues(val)
                print(val)
            # else:
                # temp = {val[k]:"" for k in range(0,len(val)) if k%2==0}
                # val_val = [val[x] for x in range(0,len(val)) if x%2!=0]

            # temp = dict(zip(val_val,temp.keys()))
        
        return val
    
    else:
        # os.chdir(r"..\cropped_images")
        text = extract_table(img)
        # os.chdir("..\\images_from_pdf")
        # print(text)
        spaces = re.compile(r'^\d{1,2}\.$')
        # text = list(filter(lambda x : x != " ",text))
        # print(text)
        temp = {}
        val = list(map(lambda x : x.strip(),text)) 
        val = list(filter(lambda x: x!='',val))
        val = list(filter(lambda x : x != apply_reg(spaces,x) ,val))

        print(val)
        if len(val)>0:
            if (val[0] == "particulars") or (val[0] == "relevant particulars"):
                # temp = {val[k]:"" for k in range(1,len(val)) if k%2!=0}
                # val_val = [val[x] for x in range(1,len(val)) if x%2==0]
                val.remove(val[0])
                val = swapvalues(val)
                print(val)
            # else:
                # temp = {val[k]:"" for k in range(0,len(val)) if k%2==0}
                # val_val = [val[x] for x in range(0,len(val)) if x%2!=0]

            # temp = dict(zip(val_val,temp.keys()))
        
        return val
    
def table_helper(file, flag_form = 0, img = None,flag_image = 0):
    if flag_image == 1:
        val = []
        form = ""
        form_test = highlight_text(file,single_val=1)
        form_test = list(map(lambda x : x.strip(),form_test))
        form_test = list(filter(lambda x : x != "" , form_test)) 
        # print(form_test)
        # test_text.append(form_test)
        for i in range(len(form_test[:5])):
            if form_test[i] == "form":
                form = form_test[i]+form_test[i+1]
            print(f"{form_test[i]}")
        val = helper_function(file,flag_image=1)
        return val, form

    
    elif flag_form == 1:
        #list for returning the all the values from images
        val = []
        form = ""
        for _ in os.listdir():
            form_test = highlight_text(_,single_val=1)
            form_test = list(map(lambda x : x.strip(),form_test))
            form_test = list(filter(lambda x : x != "" , form_test)) 
            # print(form_test)
            # test_text.append(form_test)
            for i in range(len(form_test[:5])):
                if form_test[i] == "form":
                    form = form_test[i]+form_test[i+1]
                print(f"{form_test[i]}") 
            temp = helper_function(_)
            val.extend(temp)
        return val,form
    elif flag_form == 0: 
        val = helper_function(img)
        return val

def folder_items(f_name):
    full_path = os.path.abspath(f_name)
    
    json_folder = "Json_files"
    os.chdir(full_path)
    re_exp_file = r"\Aform"
    # pdf_count = 0
    json_val = []
    # image_count = 0
    temp_image_folder = "images_from_pdf"
    temp_cropped_folder = "cropped_images"
    start = time.time()
    
    # form_list = ['formb.pdf','formc.pdf','formd.pdf','forme.pdf','formf.pdf']

    
    
    
    for dirpath, dirnames, filenames in os.walk("."):
        
        
        #Available Directories
        dir_in_path = [dir for dir in dirnames]
        print(f"Available Directories {dir_in_path}")
            
        #Make temprory images folder
        # if temp_image_folder not in dir_in_path:
        try:
            os.mkdir(temp_image_folder)
            # if temp_cropped_folder not in dir_in_path:
            # os.mkdir(temp_cropped_folder)
        
        except FileExistsError as identifier:
            pass
                

        print("Walking dir")
        for file in filenames:
            file_counter = 0 #counter for files
            json_file = [] #Initialize empty dictionary for final json file
            json_file_val = [] #Initialize empty list for dictionaries all values
            form_count = 0 #counter for distinguishing the number of pages to OCR after form has been found
            form_type = ""
            
            '''Preprocess the files for finding the names of files
                if the file name has form in it then OCR the entire file 
                else walk thorugh entire file and look for the initial words to be equal to form  
            '''
            
            print("Looking for files")
            if file.endswith(".pdf"):
                print("found a pdf")
                file_test = re.split(re_exp_file,file.lower())
                print(len(file_test))    
                # if len(file_test)>1:
                #     file_test = str(file_test[0].lower())+str(file_test[1].lower())
                # print(file_test)                
                if len(file_test)>1: #in form_list:
                    print("form found")
                    print(f"found {file}")
                    pdf_table(file)
                    os.chdir(r".\images_from_pdf")
                    json_file_val,form_type = table_helper(file,flag_form = 1)
                    JSON_Create_Form(full_path,file,form_type,json_file_val)
                    os.chdir("..")
                    print(os.getcwd())
                    delete_files(r".\images_from_pdf")
                    # print(json_file)
                    # os.chdir(r".\files")
                else:
                    form_type = ""
                    print(f"found file {file}")
                    print(os.path.abspath(file))
                    pdf_table(os.path.abspath(file))
                    os.chdir(r".\images_from_pdf")
                    for _ in os.listdir():
                        val = highlight_text(_,single_val=1)
                        val = list(map(lambda x : x.strip(),val))
                        val = list(filter(lambda x : x != "" , val)) 
                        # print(val)
                        # test_text.append(val)
                        for i in range(len(val[:5])):
                            print(f"{i} {val[i]}")
                            if form_count == 0:
                                if val[i].lower() == "form":
                                    print(val[i+1])
                                    form_type = val[i]+val[i+1]
                                    json_val = table_helper(file,flag_form=0,img = _)
                                    # print(json_val)
                                    form_count += 1  
                                    break
                            elif form_count > 0:
                                json_val = table_helper(file,flag_form=0,img = _)
                                # print(json_val)
                                break
                            else:
                                break
                        json_file_val.append(json_val)
                        # print(json_file_val)
                    json_file_val = list(filter(lambda x: x != [], json_file_val))
                    print(json_file_val)
                    for i in range(len(json_file_val)):
                        json_file += json_file_val[i]
                    if form_type:
                        JSON_Create_Form(full_path,file,form_type,json_file)
                        

                    os.chdir("..")
                    delete_files(r".\images_from_pdf")
                    # delete_files(r".\cropped_images")
            elif file.endswith(".jpg") or file.endswith(".png"):
                print("found an image")
                print(f"found {file}")
                # os.chdir(r".\images_from_pdf")
                json_file_val,form_type = table_helper(file,flag_form = 1,flag_image = 1)
                if form_type != "" :
                    JSON_Create_Form(full_path,file,form_type,json_file_val)

    end = time.time()
    print(end-start)
    # delete_files(r".\cropped_images")
    # os.rmdir(temp_cropped_folder)
    os.rmdir(temp_image_folder)


if __name__ == "__main__":
    folder_name = sys.argv[1]
    folder_items(folder_name)

    