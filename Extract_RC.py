



#Importing Essential Libraries
import pytesseract
import pandas as pd
from PIL import Image,ImageEnhance
import os

#assigning the directory link of Tesseract.exe
pytesseract.pytesseract.tesseract_cmd=r"Tesseract-OCR\tesseract.exe"





Rc_list=os.listdir('RC')
for i in range(len(Rc_list)):
    print(i,Rc_list[i])




data=[]
j=0
for pictures in Rc_list:
    
     # 'RC/'+pictures is the directory of test images. 
    # Pictures are taken one at a time
    img=Image.open('RC\\'+pictures)                              
    
    # ImageEnhance helps the images to be processed in a better way.
    
    #Enhancing Brightnesss
    enhanced_img=ImageEnhance.Brightness(img)                         
    img=enhanced_img.enhance(1.2)
    
    #Enhancing Color
    enhanced_img=ImageEnhance.Color(img)
    img=enhanced_img.enhance(0.0)
    
    #Converting Image to string
    text=pytesseract.image_to_string(img)
    
    # spliting the text according the spaces
    new_str=text.split()                                   
    
    #initializing a list which holds the required 6 values needed from a image
    info_list=[None]*6                                            
    data.append(info_list)
    two=0
    for i in range(len(new_str)-6):
        
     #Exctracting the "License plate number or Regn number"  
        if new_str[i]=='REGN':
            if len(new_str[i+4])<9:
                    a=new_str[i+4]+new_str[i+5]
                    data[j][0]=a
            else:
                data[j][0]=new_str[i+4]
        else:
            if new_str[i]=='REGN.':
                if len(new_str[i+3])<9:
                    a=new_str[i+3]+new_str[i+4]
                    data[j][0]=a
                else:
                    data[j][0]=new_str[i+3]
        if new_str[i]=="Registration":
            if new_str[i+1]=="No.":
                if len(new_str[i+2])<9:
                    a=new_str[i+2]+new_str[i+3]
                    data[j][0]=a
                else:
                    data[j][0]=new_str[i+2]
                
        if 'HR' in new_str[i]:
            data[j][0]==new_str[i]
        
            
    # Extracting the "VIN number or Chassis number (Typically 17 digit long)"   
        if new_str[i]=='CH.' or new_str[i]=='CH' :    
            data[j][1]=new_str[i+3]
            
        if new_str[i]=="Chassis" or new_str[i]=="Chasis":
            if new_str[i+1]=="No.":
                data[j][1]=new_str[i+2]
        
        
    #Extracting the "Name"  
        if new_str[i]=='NAME' or new_str[i]=='Name' or new_str[i]=='name':
            if '_' or '-' in new_str[i+1]:
                if new_str[i+2]==':' or new_str[i+1]==':.':
                    if new_str[i+3]=='MR' or new_str[i+3]=='mr' or new_str[i+3]=='Mr' or new_str[i+3]=='MR.' or new_str[i+3]=='mr.' or new_str[i+3]=='Mr.':
                        name=new_str[i+4]
                    else:
                        name=new_str[i+3]
                else:
                    if new_str[i+2]=='MR' or new_str[i+2]=='mr' or new_str[i+2]=='Mr' or new_str[i+2]=='MR.' or new_str[i+2]=='mr.' or new_str[i+2]=='Mr.':
                        name=new_str[i+3]
                    else:
                        name=new_str[i+2]
                    
            elif new_str[i+1]==':' or new_str[i+1]==':.':
                    if new_str[i+2]=='MR' or new_str[i+2]=='mr' or new_str[i+2]=='Mr' or new_str[i+2]=='MR.' or new_str[i+2]=='mr.' or new_str[i+2]=='Mr.':
                        name=new_str[i+3]
                    else:
                        name=new_str[i+2]
            elif new_str[i+1]=='MR' or new_str[i+1]=='mr' or new_str[i+1]=='Mr' or new_str[i+1]=='MR.' or new_str[i+1]=='mr.' or new_str[i+1]=='Mr.' :
                name=new_str[i+2]
            
            elif new_str[i-1]=="Owner's":
                name=new_str[i+1]
            elif "&" in new_str[i+1]:
                name=new_str[i+4] #i+4
            else:
                name=new_str[i+1]
            if two==0:
                data[j][2]=name
                two=1
                
                
    #Extracting the "Engine number" 
        if new_str[i]=='ENO':
            if new_str[i+1]=='-' or new_str[i+1]=='_':
                data[j][3]=new_str[i+3]
            else:
                if new_str[i+2][-1]=='-':
                    a=str(new_str[i+2])+str(new_str[i+3])
                    data[j][3]=a
                else:
                    data[j][3]=new_str[i+2]
        if new_str[i]=="Engine":
            if len(new_str[i+2])<11:
                a=new_str[i+2]+new_str[i+3]
                data[j][3]=a
            else:
                data[j][3]=new_str[i+2]
                


    # Extracting the "Registration date" 
        if new_str[i]=="REG." or new_str[i]=="REGN":
            if "DT" in new_str[i+1]:
                if new_str[i+2]==":":
                    reg_date=new_str[i+3]
                else:
                    reg_date=new_str[i+2]
                length=len(reg_date)
                reg_date=reg_date[:length-8]+" / "+reg_date[length-7:length-5]+" / "+reg_date[length-4:]        
            
                data[j][4]=reg_date
        
        
        
    #Extracting the "Mfg. date" 
        if new_str[i]=="Year":
            if new_str[i+1]=="of":
                if "Manu" in new_str[i+2]:
                    manufacture_date=new_str[i+3]
            length=len(manufacture_date)
            manufacture_date=manufacture_date[:length-5]+" / "+manufacture_date[length-4:]
            data[j][5]=manufacture_date
            
        if new_str[i]=="Yr":
            if new_str[i+1]=="of":
                manufacture_date=new_str[i+2]
            length=len(manufacture_date)
            manufacture_date=manufacture_date[:length-5]+" / "+manufacture_date[length-4:]
            data[j][5]=manufacture_date
        
        
        
        if new_str[i]=="Month":
            if new_str[i+3]=="of":
                if new_str[i+4]=="Mfg." or new_str[i+4]=="Mfg" or new_str[i+4]=="Mig." or new_str[i+4]=="Mig":
                    manufacture_date=new_str[i+5]
            length=len(manufacture_date)
            manufacture_date=manufacture_date[:length-5]+"/"+manufacture_date[length-4:]
            data[j][5]=manufacture_date   
        
        if "MFG" in new_str[i]:
            if new_str[i+1]==":":
                manufacture_date=new_str[i+2]
            elif "DT" in new_str[i+1]:
                if new_str[i+2]==":":
                    manufacture_date=new_str[i+3]
                else:
                    manufacture_date=new_str[i+2]
            else:
                manufacture_date=new_str[i+1]
            length=len(manufacture_date)
            manufacture_date=manufacture_date[:length-5]+"/"+manufacture_date[length-4:]
            data[j][5]=manufacture_date
        
        
    j+=1
 





#Creating a Dataframe for the data extracted
df=pd.DataFrame(data)
df.columns=["Regn number","Chassis number","Name","Engine number","Registration date","Mfg. date"]
df




#Converting the Dataframe to csv(excel) file
df.to_csv('RC_info.csv')





#Reading the Data from RC_info.csv
import csv

with open('RC_info.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} Regn number {row[1]} , Chasis Number {row[2]},Name {row[3]},Engine Number {row[4]},Reg. Date {row[5]}, Mfg. Date {row[6]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')






