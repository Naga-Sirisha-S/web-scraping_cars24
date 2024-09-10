
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def load_the_complete_webpage(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if height == new_height:
            break
        else :
            height = new_height
    
    return driver


def get_data(website,Kilometers_Driven,Year_of_Manufacture,Fuel_Type,Transmission,Price,Model,Company_Name):
    driver=load_the_complete_webpage(website)
    soup=BeautifulSoup(driver.page_source,"html.parser")
    results=soup.find_all("a",{'class':"IIJDn"})
    for i in results:
        Company_Name.append(i.find('h3',{'class':'_11dVb'}).get_text().split(" ")[1])
        Model.append(i.find('h3',{'class':'_11dVb'}).get_text().split(" ",2)[2])
        Year_of_Manufacture.append(i.find('h3',{'class':'_11dVb'}).get_text().strip(" ")[:4])
        Price.append(i.find('strong',{"class":"_3RL-I"}).get_text().replace('₹','').split(" ")[0])
        ultag=i.find('ul',{'class':'_3J2G-'})
        text = list(ultag.descendants)
        for i in range(1, len(text),3): 
            if(i%4==0):
                Fuel_Type.append(text[i])
            elif(i%7==0):
                Transmission.append(text[i])
            else:
                Kilometers_Driven.append(text[i].split(" ",2)[0].replace(",",''))

Kilometers_Driven=[]
Year_of_Manufacture=[]
Fuel_Type=[]
Transmission=[]
Price=[]
Model=[]
Company_Name=[]
places=["new-delhi","bangalore","mumbai","hyderabad","ahmedabad","gurgaon","chennai","noida","pune"]
companies=["hyundai",'honda','tata','mahindra','renault','ford','kia','mg','jeep','datsun','volkswagen']
for place in places:
    for company in companies:
        website="https://www.cars24.com/buy-used-"+company+"-cars-"+place+"/"
        get_data(website,Kilometers_Driven,Year_of_Manufacture,Fuel_Type,Transmission,Price,Model,Company_Name)
        
        
YOM=[int(yom) for yom in Year_of_Manufacture]
KM=[int(km) for km in Kilometers_Driven]
P=[float(price) for price in Price]
Data=pd.DataFrame({'Company_Name':Company_Name,'Model':Model,'Year_of_Manufacture':YOM,'Price (in lakhs)':P,'Kilometers_Driven':KM,'Fuel_Type':Fuel_Type,'Transmission':Transmission})

Data.to_csv('cars.csv',index=False)
