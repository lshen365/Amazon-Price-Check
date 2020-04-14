import requests
import urllib.request
import time
import tkinter as tk
import xlwt
from xlwt import Workbook
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
from MailSMTP import MailSMTP

class Amazon():
    # def __init__(self):
    #     self.wb = Workbook()
    #     self.sheet = self.wb.add_sheet('Amazon Data')
    #     self.row = 0
    # def inputToExcel(self,price,r):
    #     self.sheet.write(r,0,price)
    #     self.wb.save('Amazon.xls')
    #     self.row+=1

    def callAmazon(self,link):
        ua = UserAgent()
        header = {"User-Agent": str(ua.chrome)}
        response = requests.get(link,headers=header)
        findPricePattern = '\d{1,}.\d{1,}'
        soup = BeautifulSoup(response.content, 'html5lib')
        print(response)
        if(response):
            priceHTML = soup.find('span',class_='green')
            price = re.search(findPricePattern,str(priceHTML))
            print(priceHTML)
            if price:
                return price.group(0)
            else:
                print("Did not find Price. Check HTML page")
                return None
        else:
            return None

    def createNewUrl(self,url):
        productID = url.split('/')[5]
        newUrl = 'https://camelcamelcamel.com/product/'+productID
        return newUrl,productID

    def returnString(self,val):
        badUrl = val
        url,productID = self.createNewUrl(val)
        price = self.callAmazon(url)
        # print(price)
        # print("Checked: "+url+" with Price $: "+price)
        if (price != None):

            #self.inputToExcel(price,self.row)
            return float(price),productID
        else:
            return False,False


run = Amazon()
websites = []
with open('links.txt') as my_file:
    for line in my_file:
        websites.append(line)
def replace_line(file_name, line_num, text,found):
    if(found):
        lines = open(file_name, 'r').readlines()
        lines[line_num] = text
        out = open(file_name, 'w')
        out.writelines(lines)
        out.close()
    else:
        line = open(file_name,'a')
        line.write(text+"\n")
        line.close()


while True:
    minPrice = []
    with open('minPrice.txt') as my_file:
        for line in my_file:
            minPrice.append(line)
    for x in range(0,len(websites)):
        price,id= run.returnString(websites[x])
        if(price != False and id != False):
            isFound = False
            for i in range(0,len(minPrice)):
                temp = minPrice[i].split(" ")
                if id+'\n' == temp[1]:
                    isFound = True
                    if price < float(temp[0]):
                        MailSMTP(str(temp[0]),str(price),websites[x]).sendMail()
                        print("Price change has been found on line ",i)
                        newLine = str(price)+' '+id+'\n'
                        replace_line('minPrice.txt',i,newLine,True)
            if not isFound:
                print("New Price has been added")
                newLine = str(price) + ' ' + id
                replace_line('minPrice.txt',len(minPrice),newLine,False)
        time.sleep(60)
    # run.returnString(websites[0])
