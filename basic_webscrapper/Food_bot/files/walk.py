from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime
from time import sleep
import csv
import shutil
import glob

#Stor ändring i deras hemsida. fungerar inte nu.
url = "https://www.coop.se/butiker-erbjudanden"

os.environ['PATH'] += r"Root\GoogleChrome\chromedriver.exe"

options=webdriver.ChromeOptions()
options.add_experimental_option("detach",True)

driver = webdriver.Chrome(options=options)

    

class FetchItems():
    def __init__(self) -> None:  
        super(FetchItems,self).__init__()
    
    def fetch_website(self):
        driver.get(url)
    
    def check_date(self):
        current_year=datetime.datetime.now()
        try:
            check_date= driver.find_element(By.XPATH,value="//h3[@class='YA_SIqwI']")
            weekdate=check_date.get_attribute("innerHTML")
            weekdate1= weekdate[:17].rstrip('\n')
            weekdate2= weekdate[17:].lstrip()
            new_weekdate= weekdate1 + " "+ weekdate2
            weekly_subscription=new_weekdate + " " + str(current_year.year)
            return weekly_subscription
        except Exception as e:
            return f"Something went wrong, {e}"
    
    def click_abort(self):
        driver.find_element(By.XPATH,value="//span[@id='cmpbntnotxt']").click()
        sleep(2)
        driver.implicitly_wait(2)

    def click_show_more_buttons(self):
        click_buttons =driver.find_elements(By.XPATH,value="//button[@class='gUGSFhfR CkqGWkRo ucdesrxw JbpuCWgM']")
        for i in click_buttons:
            i.click()
            sleep(0.5)
        sleep(2)

    
    def fetch_item_list(self):
        items=[]

        check_item=driver.find_elements(By.XPATH,value="//div[@class='ProductTeaser-content']")
        for y in check_item:    
                check_price=y.find_element(By.CLASS_NAME,value="Splash-content").get_attribute("innerHTML")
                # check_price=y.find_element(By.CLASS_NAME,value="Splash-priceLarge").get_attribute("innerHTML")
                soup=BeautifulSoup(check_price,"html.parser")
                check_price=soup.get_text()
                # items.append(check_price)
                print(check_price)
                if "förp" in check_price:
                    check_price=self.check_förp(check_price)
                
                elif "för" in check_price:
                    check_price=self.check_amount_for(check_price)

                elif "kg" in check_price:
                    check_price=self.check_kg_price(check_price)

                elif "st" in check_price:
                    check_price=self.convert_st(check_price)

                elif "rabatt" in check_price:
                    pass
                else:
                    check_price=check_price[:-2]
            
                check_tag=y.find_element(By.CLASS_NAME,value="ProductTeaser-heading").get_attribute("innerHTML")
                soup=BeautifulSoup(check_tag,"html.parser")
                check_tag=soup.get_text()

                #Kolla namn på varan. Väldigt dåligt format på coops hemsida
                # check_name=y.find_element(By.XPATH,value="//div[@class='ProductTeaser-brand']").get_attribute("innerHTML")
                # if check_name:
                    
                # soup=BeautifulSoup(check_name,"html.parser")
                # check_name=soup.get_text()
                #     print(check_name)
                # else:
                #      pass
                # print(check_name)

                # items.append([check_price,check_tag,check_name])
                items.append([check_price,check_tag])
        # print(items)
        return items

    def check_förp(self,check_price):
        check_discount = re.sub('/förp', '', check_price)
        if len(check_discount) <=3:
            return int(check_discount[0]) 
        elif len(check_discount) ==4:
            return int(check_discount[:2])
        else:
            return int(check_discount[:3])
        
    def check_amount_for(self,check_price):
        return check_price[:-2]

    def check_kg_price(self,check_price):
        check_kg = re.sub('/kg', '', check_price)
        if len(check_kg) <=3:
            return int(check_kg[0]) , " Kg"
        elif len(check_kg) ==4:
            return int(check_kg[:2]), " Kg"
        else:
            return int(check_kg[:3]), " Kg"
        
    def convert_st(self,check_price):
        check_st = re.sub('/st', '', check_price)
        if len(check_st) <=3:
            return int(check_st[0]) 
        elif len(check_st) ==4:
            return int(check_st[:2])
        else:
            return int(check_st[:3])  

    def send_to_file(self):
        try:
                    
            now=datetime.datetime.now()
            week_year=now.isocalendar()[1]
            filename = f"{week_year}_vecka_coop"

            return_valid_path=self.check_file_valid()
            
            if return_valid_path==True:
                print("Already made a file on that week")
                return "Already made a file on that week"
            else:
                print("sending to file")
                self.move_old_discounts()
                self.add_items_to_file(filename)

            return "Data successfully added!"
        
        except Exception as e:
            return f"Something went wrong {e}"
        
    def add_items_to_file(self,filename:str):

        valid_date=self.check_date()
        get_items=self.fetch_item_list()
           
        file_path=f"basic_webscrapper/discounts/{filename}"

        
        df=pd.DataFrame(get_items)
        df.to_csv(r"RootPath\vecka.csv",index=False)
        
        try:
            with open("basic_webscrapper/discounts/vecka.csv","r") as read_file:
                reader=csv.reader(read_file)
                next(reader)
                get_item_list=[]
                get_item_list.append([valid_date])
                for i in reader:
                    get_item_list.append(i)
                
                
            with open(f"{file_path}.csv","w",newline='') as set_file:
                writer=csv.writer(set_file)
                for i in get_item_list:
                    writer.writerow(i)
            
            folder_file='basic_webscrapper/discounts/'
            file=glob.glob(os.path.join(folder_file,"Test.csv"))
    
            if file:
                os.remove(file)
            else:
                pass
            
        except Exception as e:
            return f"Someting went wrong,{e}"


    # kollar ifall det finns en inskriven vecka
    def check_file_valid(self):

        now=datetime.datetime.now()
        week_year=now.isocalendar()[1]
        filename = f"{week_year}_vecka_coop.csv"
        directory='basic_webscrapper/discounts'
        join_file_path=os.path.join(directory,filename)

    
        return os.path.isfile(join_file_path)

    def move_old_discounts(self):
        directory='basic_webscrapper/discounts'
        target_directory='basic_webscrapper/discounts/archive'
        os.makedirs(target_directory, exist_ok=True)
        
        for filename in os.listdir(directory):
            # print(filename)
            if filename.endswith('.csv'):
                source_file=os.path.join(directory,filename)
                target_file=os.path.join(target_directory,filename)
                try:
                    shutil.move(source_file,target_file)
                    print("moved file")
                except Exception as e:
                    print(f"error,{e}")
            else:
                pass

