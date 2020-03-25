def highlight_text(page,single_val = 0):
    import pytesseract
    from pytesseract import Output
    import os
    import cv2
    import pandas as pd
    # print(path,pdffile)
    
    text = ''
    text_list = []
    
    
    '''
    Sort all pages in order in pdf to image folder
    '''
    # def sort_list(list_name):
    #     temp = ""
    #     for i in range(len(list_name)):
    #         for j in range(i+1,len(list_name)):
    #             if int(list_name[i].split("_")[0])>int(list_name[j].split("_")[0]):
    #                 temp= list_name[j]
    #                 list_name[j]=list_name[i]
    #                 list_name[i] = temp
    #     return list_name 
    
    #dir_path= r'.\pdf_to_jpg'
    #os.chdir(dir_path)
    #vocab = ['land','  lease','acres']
    
    '''
    Tesseract configuration
    '''
    tessdata_dir_config = "--tessdata-dir 'C:\\Program Files\\Tesseract-OCR\\tessdata'"
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    
    
    '''
    Sorting the images
    '''
    # name_list = [name for name in os.listdir(".")]
    # #sorted_names = list(map(sort_list,name_list))
    # sorted_list = sort_list(name_list)
    
    #page counter
    page_count = 0
    #Data for csv
    
    '''
    Looking for the key_word in all the images
    '''

    # for page in sorted_list:
        # print(page_count)
    row_count=0
    # img = cv2.imread(page)
    
    try:
        print(f"reading image {page_count}")
        d = pytesseract.image_to_data(page,output_type=Output.DICT,lang='eng', config=tessdata_dir_config)
        n_boxes = len(d['level'][:20])
        # overlay = img.copy()
        # user_input = input("What are you looking for: ")
        # df = pd.DataFrame({})
        if single_val == 1:
            for i in range(n_boxes):        
                text_list.append(d['text'][i].lower())
                # print(text_list)
            return text_list
        else:
            for i in range(n_boxes):
                text += d['text'][i].lower()+" "
                #print(text)
                # if text=="form":
                    # row_count+=1
                
                    # #highlight the text
                    # #print('inside if')
                    
                    # '''
                    # Take the co-ordinates of the text
                    # '''
                    # (x,y,w,h) = (d['left'][i],d['top'][i],d['width'][i],d['height'][i])

                    # '''
                    # In order to highlight the coressponding text we will increment the counter by 1
                    # '''
                    # (x1,y1,w1,h1) = (d['left'][i],d['top'][i],d['width'][i],d['height'][i])
                    
                    # cv2.rectangle(overlay, (x,y),(x1+w1,y1+h1),(255,0,0),-1)
                    # alpha  = 0.4 
                    # img_new = cv2.addWeighted(overlay,alpha, img, 1-alpha,0)
                    # r=1000.0/img_new.shape[1]
                    # dim=(1000,int(img_new.shape[0]*r))
                    # resized = cv2.resize(img_new,dim,interpolation=cv2.INTER_AREA)
                    # cv2.imshow('img',resized)
                    # cv2.waitKey(500)
                    # cv2.destroyAllWindows()
                    # cv2.imwrite(page,img_new)
            page_count+=1
            # if row_count>0:
            #     data['File_Name'].append(pdffile)
            #     data['Key_Word'].append(highlight_val)
            #     data['Page_Num'].append(page_count)
            #     data['Number_Of_Occurances'].append(row_count)
            #     data['Full_File_Path'].append(os.path.join(os.path.abspath(path),pdffile))
            #initializing dataframe
            # df = pd.DataFrame(data)
            # df.to_csv('..\\key_words.csv', mode = 'a', header=True)
            
            return text
    except:
        print("error while processing the file")
        return text




if __name__ == "__main__":
    val = highlight_text(r"D:\Zohaib\Documents\Letter of Recommendation.jpg")
    print(val)



