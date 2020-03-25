import json
import re
from collections import defaultdict
from itertools import zip_longest



def swapvalues(val:list):
    for i in range(0,len(val)-1,2):
        val[i],val[i+1]=val[i+1],val[i]
    return val

def pre_proc_list(val_list,form_type):
    form_keys = []
    if form_type == "formb":
        form_keys = ["Operational Creditor",
                        "Identification Number",
                        "Address  Email",
                        "Total amount",
                        "Documents  reference",
                        "Details dispute",
                        "Debt Incurred",
                        "Mutual Credit",
                        "Retention Title",
                        "Bank Account",
                        "Documents Attached"
                    ]
    if form_type == "formc":
        form_keys = ["Financial Creditor",
                    "identification number",
                    "address email",
                    "amount claim",
                    "details documents debt substantiated",
                    "debt incurred",
                    "mutual credit",
                    "security held",
                    "bank account",
                    "documents attached claim existence"]
    if form_type == "formd":
        form_keys = ["name workman",
                    "pan passport identity",
                    "address email",
                    "total amount claim",
                    "details documents reference",
                    "details dispute pendency",
                    "details claim arose",
                    "mutual credit",
                    "bank account",
                    "documents attached proof"
                    ]
    if form_type == "formf":
        form_keys = ["name creditor",
                    "identification number",
                    "address email",
                    "description claim isolvency",
                    "details documents reference substantiated",
                    "details claim arose",
                    "mutual credit",
                    "details security held retention title arrangement",
                    "bank account",
                    "documents attached prove",
                    ]
                        
    i= 0
    j= 0
    
    val_dic = []
    while i<len(val_list) and j<len(form_keys):
        
        print("inside loop")
        keyword = form_keys[j].split()
        print(keyword)
        search_words = val_list[i]
        print(search_words)
        word = re.compile(rf'\b{keyword[0]}\b|\b{keyword[1]}\b',flags=re.I|re.X)
        y = re.findall(word,search_words)        
        print(y)
  


        if (i == 0) and (len(y)>=2):
            # val_dic.append("")
            j += 1
            i += 1
            val_dic.append(val_list[i].upper())
            continue

        if (i==0) and (len(y)<2):
            val_dic.append("")
            # i+=1
            # val_list[i],val_list[i+1] = val_list[i+1],val_list[i]
            val_list = swapvalues(val_list)
            val_list.insert(i,"")
            val_list = swapvalues(val_list)
            i+=1
            j+=1
            
            if (i%2 == 1) and (len(y)>=2):
                print("inside if")
                val_dic.append(val_list[i-1].upper())
                # val_dic.append("")
            
            elif (i%2 == 0) and (len(y)>=2):
                val_dic.append(val_list[i-1].upper())
                # val_dic.append("")
                print("inside elif")            




        if (i%2 == 1) and (len(y)>=2):
            print("inside if")
            val_dic.append(val_list[i-1].upper())
            # val_dic.append("")
        
        elif (i%2 == 0) and (len(y)>=2):
            val_dic.append(val_list[i+1].upper())
            # val_dic.append("")
            print("inside elif")

        else:
            i+=1
            if (i == len(val_list)) and (j < len(form_keys)):    
                j += 1
                i == 0
                val_dic.append("")
                continue  
            continue
        j += 1
        

    
    return val_dic






# def remove_spaces(text):
#     x = text.split()
#     y = ""
#     for i,val in enumerate(x,start=0):
#         y += x[i].lower()
#     return y    



def WriteToJSONFile(path, fileName, data):
    print
    filePathNameWithExt = path + "/" + fileName + ".json"
    with open(filePathNameWithExt, "a") as fp:
            json.dump(data, fp, ensure_ascii=False, indent=4)
            #3print(json.dumps(data))

def JSON_Create_Form(foldPath,file_name,form_type,val_list):
    path = foldPath
    fileName = "data"
    data = {}
    Form = {}
    Form_1 = {}
    Form_2 = {}

    '''
        list = []
       iterate over list 
       check val[i] == key[j]
        if true key1 == ""
        else if check val[i+1] == key[j]
            if true key[j] == val[i]
        else:
            j += 1
            continue
        i = i+1
    '''
    print(val_list)
    val_dic = pre_proc_list(val_list,form_type)
    print("printing final dictionary")
    print(val_dic)
    
   
    if form_type == "formb":
        Form_2["NameOperationalCreditor"] = ""    
        Form_2["IdentificationNumber"] = ""
        Form_2["AddressEmail"] = ""
        Form_2["TotalAmount"] = ""
        Form_2["DetailsDocuments"] = ""
        Form_2["DetailsDispute"] = ""
        Form_2["DetailsDebtIncured"] = ""
        Form_2["DetailsMutual"] = ""
        Form_2["DetailsRetention"] = ""
        Form_2["DetailsBankAccount"] = ""
        Form_2["ListDocumentsAttached"] = ""
        Form_2["NameBlock"] = ""
        Form_2["Relation"] = ""
        Form_2["AddressPersonSigning"] = ""
    if form_type == "formc":
        Form_2["NameFinancialCreditor"] = ""
        Form_2["IdentificationNumber"] = ""
        Form_2["AddressEmail"] = ""
        Form_2["TotalAmount"] = ""
        Form_2["DetailsDocuments"] = ""
        Form_2["DetailsDebtIncured"] = ""
        Form_2["DetailsMutual"] = ""
        Form_2["DetailsSecurity"] = ""
        Form_2["DetailsBankAccount"] = ""
        Form_2["ListDocumentsAttached"] = ""
        Form_2["NameBlock"] = ""
        Form_2["Relation"] = ""
        Form_2["AddressPersonSigning"] = ""
    if form_type == "formd":
        Form_2["NameWorkman"] = ""
        Form_2["DocumentsWorkman"] = ""
        Form_2["AddressWorkman"] = ""
        Form_2["TotalAmount"] = ""
        Form_2["DetailsDocuments"] = ""
        Form_2["DetailsDispute"] = ""
        Form_2["DetailsClaimArose"] = ""
        Form_2["DetailsMutual"] = ""
        Form_2["DetailsBankAccount"] = ""
        Form_2["ListDocumentsAttached"] = ""
        Form_2["NameBlock"] = ""
        Form_2["Relation"] = ""
        Form_2["AddressPersonSigning"] = ""
    if form_type == "formf":
        Form_2["NameCreditor"] = ""
        Form_2["IdentificationNumber"] = ""
        Form_2["AddressEmail"] = ""
        Form_2["TotalAmount"] = ""
        Form_2["DetailsDocuments"] = ""
        Form_2["DetailsClaimArose"] = ""
        Form_2["DetailsMutual"] = ""
        Form_2["DetailsSecurity"] = ""
        Form_2["DetailsBankAccount"] = ""
        Form_2["ListDocumentsAttached"] = ""
        Form_2["NameBlock"] = ""
        Form_2["Relation"] = ""
        Form_2["AddressPersonSigning"] = ""
    form_name = re.compile(rf'\Aform').split(form_type)
    # form_name = form_type.split("form")
    print(form_name)
    if len(form_name)>1:
        form_name_text = "FORM_"+form_name[1].upper()  

        form_type ="FORM"+" "+form_name[1].upper()
    else:
         form_name_text = "FORM_"+form_name[0].upper()


    Form_1["FileName"] = file_name
    Form_1["FormType"] = form_type
    Form_1["CaseName"] = ""



     
    Form_2 = dict(zip_longest(Form_2,val_dic,fillvalue = ""))
    print(Form_2)
    Form = {**Form_1,**Form_2}

    data[form_name_text] = Form
    WriteToJSONFile(path, fileName, data)



    
# def JSON_Create_Form_C(foldPath,file_name,form_type,val_dict):
#     path = foldPath
#     fileName = "data"
#     data = {}
#     Form = {}
#     Form_1 = {}
#     Form_2 = {}
#     convert_to_list = [val for val in val_dict.values()]

#     Form = {}
    
#     Form_1["FileName"] = file_name
#     Form_1["FormType"] = form_type
#     Form_1["CaseName"] = ""
    
#     Form_2["NameFinancialCreditor"] = ""
#     Form_2["IdentificationNumber"] = ""
#     Form_2["AddressEmail"] = ""
#     Form_2["TotalAmount"] = ""
#     Form_2["DetailsDocuments"] = ""
#     Form_2["DetailsDebtIncured"] = ""
#     Form_2["DetailsMutual"] = ""
#     Form_2["DetailsSecurity"] = ""
#     Form_2["DetailsBankAccount"] = ""
#     Form_2["ListDocumentsAttached"] = ""
#     Form_2["NameBlock"] = ""
#     Form_2["Relation"] = ""
#     Form_2["AddressPersonSigning"] = ""

#     Form_2 = dict(zip(Form_2,convert_to_list))
#     Form = {**Form_1,**Form_2}


#     data["Form_C"] = Form
#     WriteToJSONFile(path, fileName, data)



# def JSON_Create_Form_F(foldPath,file_name,form_type,val_dict):
#     path = foldPath
#     fileName = "data"
#     data = {}
#     Form = {}
#     Form_1 = {}
#     Form_2 = {}
#     convert_to_list = [val for val in val_dict.values()]

#     Form = {}
#     Form_1["FileName"] = file_name
#     Form_1["FormType"] = form_type
#     Form_1["CaseName"] = ""
    
#     Form_2["NameCreditor"] = ""
#     Form_2["IdentificationNumber"] = ""
#     Form_2["AddressEmail"] = ""
#     Form_2["TotalAmount"] = ""
#     Form_2["DetailsDocuments"] = ""
#     Form_2["DetailsClaimArose"] = ""
#     Form_2["DetailsMutual"] = ""
#     Form_2["DetailsSecurity"] = ""
#     Form_2["DetailsBankAccount"] = ""
#     Form_2["ListDocumentsAttached"] = ""
#     Form_2["NameBlock"] = ""
#     Form_2["Relation"] = ""
#     Form_2["AddressPersonSigning"] = ""

#     Form_2 = dict(zip(Form_2,convert_to_list))
#     Form = {**Form_1,**Form_2}

#     data["Form_F"] = Form
#     WriteToJSONFile(path, fileName, data)

# def JSON_Create_Form_D(foldPath,file_name,form_type,val_dict):
#     path = foldPath
#     fileName = "data"
#     data = {}
#     Form = {}
#     Form_1 = {}
#     Form_2 = {}
#     convert_to_list = [val for val in val_dict.values()]

#     Form = {}
#     Form_1["FileName"] = file_name
#     Form_1["FormType"] = form_type
#     Form_1["CaseName"] = ""

#     Form_2["NameWorkman"] = ""
#     Form_2["DocumentsWorkman"] = ""
#     Form_2["AddressWorkman"] = ""
#     Form_2["TotalAmount"] = ""
#     Form_2["DetailsDocuments"] = ""
#     Form_2["DetailsDispute"] = ""
#     Form_2["DetailsClaimArose"] = ""
#     Form_2["DetailsMutual"] = ""
#     Form_2["DetailsBankAccount"] = ""
#     Form_2["ListDocumentsAttached"] = ""
#     Form_2["NameBlock"] = ""
#     Form_2["Relation"] = ""
#     Form_2["AddressPersonSigning"] = ""

#     Form_2 = dict(zip(Form_2,convert_to_list))
#     Form = {**Form_1,**Form_2}

#     data["Form_D"] = Form
#     WriteToJSONFile(path, fileName, data)

# def JSON_Create_Form_E(foldPath,file_name,form_type,val_dict):
#     path = foldPath
#     fileName = "data"
#     data = {}
#     Form = {}
#     Form_1 = {}
#     Form_2 = {}
#     convert_to_list = [val for val in val_dict.values()]

#     Form = {}
        
#     Form_1["FileName"] = file_name
#     Form_1["FormType"] = form_type
#     Form_1["CaseName"] = ""
    
#     Form_2["NameAuthRep"] = ""
#     Form_2["Address"] = ""
#     Form_2["DetailsDebtIncured"] = ""
#     Form_2["DetailsMutual"] = ""

    
#     Form_2 = dict(zip(Form_2,convert_to_list))
#     Form = {**Form_1,**Form_2}

#     data["Form_E"] = Form
#     WriteToJSONFile(path, fileName, data)
