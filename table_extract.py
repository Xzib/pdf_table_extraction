import cv2
import numpy as np
from pdf2image import convert_from_path, convert_from_bytes
from tesseract_ocr_test import highlight_text
import os
import pprint
import json

def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)




#https://medium.com/coinmonks/a-box-detection-algorithm-for-any-image-containing-boxes-756c15d7ed26
def extract_table(image_file_path):

    text = []

    #Read the image
    img = cv2.imread(image_file_path,0)
    
    #Thresholding the image
    (thresh,img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)  
    # img_bin = cv2.resize(img_bin,(0,0),fx=3,fy=3)
    # img_bin = cv2.GaussianBlur(img_bin,(11,11),0)
    # img_bin = cv2.medianBlur(img_bin,9)

    #invert the image
    img_bin = 255-img_bin
    # cv2.imwrite("Image_bin.jpg", img_bin)

    #defining kernel length
    kernel_length = np.array(img).shape[1]//80
    print(kernel_length)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,kernel_length))
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length,1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))


    #morphological operations for vertical lines
    img_temp1 = cv2.erode(img_bin, vertical_kernel, iterations=5)
    vertical_lines_img = cv2.dilate(img_temp1, vertical_kernel, iterations=5)
    # cv2.imwrite("vertical_lines.jpg",vertical_lines_img)

    #morphological operations horizontal lines
    img_temp2 = cv2.erode(img_bin, horizontal_kernel, iterations=5)
    horizontal_lines_img = cv2.dilate(img_temp2, horizontal_kernel, iterations=5)
    # cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)

    #Weighting parameters
    alpha = 0.5
    beta = 1.0 - alpha

    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    image_final_bin = cv2.addWeighted(vertical_lines_img,alpha,horizontal_lines_img,beta, 0.0)
    image_final_bin = cv2.erode(~image_final_bin, kernel, iterations=2)
    (thresh,image_final_bin) = cv2.threshold(image_final_bin, 128, 255, cv2.THRESH_BINARY| cv2.THRESH_OTSU)
    # cv2.imwrite("image_final_bin.jpg", image_final_bin)


    # Find contours for image, which will detect all the boxes

    contours, hierarchy = cv2.findContours(image_final_bin,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #sort all the contours from top to bottom
    (contours, boundingBoxes) = sort_contours(contours,method="top-to-bottom")
    #crop all the boxes
    idx = 0
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        if cv2.contourArea(c)<300000:    #(w > 80 and h > 20) and w > 3*h:
            idx += 1
            new_img = img[y:y+h, x:x+w]
            r = 1600/new_img.shape[1]
            dim = (1600,int(new_img.shape[0]*r))
            new_img = cv2.resize(new_img,dim)
            # cv2.imwrite(str(idx) + '.png',new_img)
            val = highlight_text(new_img)
            text.append(val)
    text = list(filter(lambda x: x != " ", text))
    
    
    return text

def pdf_table(file_name):
    counter = 0
    images_from_path = convert_from_path(file_name,dpi=200)
    os.chdir(r".\images_from_pdf")
    for image in images_from_path:
        print(f"######### Converting image = {counter} #######")
        image.save(str(counter)+'_page'+".jpg","JPEG")
        counter += 1    
    os.chdir(r"..")

def table_c(data):
    clean_val = val[5:]
    print(clean_val)
    print(len(clean_val))
    json_c = {key:"" for key in clean_val[:10]}
    json_c = dict(zip(json_c.keys(),clean_val[10:]))
    # json_file = json.dumps(json_c)
    # length = len(json_c)
    with open("form_c.txt", "w") as fp:
        json.dump(json_c,fp,separators=('\n',': '))


if __name__ == "__main__": 
    pdf_table(r".\files\5.pdf")
    form_test = ""
    val= ""
    form_test = highlight_text(r".\images_from_pdf\0_page.jpg")
    form_test = form_test.split()
    print(form_test)
    for i in range(len(form_test)):
        print(i)
        i = str(form_test[i])+str(form_test[i+1])
        print(i)
        if i == "formc":
            print("Form C found")
            val = extract_table(r".\images_from_pdf\0_page.jpg")
            val = list(map(lambda x : x.strip(),val))
            table_c(val)
            break
        
        # else:
        #     print("No form found")
        #     break
    
    # pprint.pprint(json_c)
     

