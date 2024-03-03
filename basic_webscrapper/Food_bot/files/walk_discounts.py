import os
import glob
import csv
import re

class WalkBot():
    
    def __init__(self) -> None:
        self.item_display=[]
       
    def ask_person(self):
        print("Vad söker du efter? tryck 1 för att avsluta")
        while True:
            item=input("")
            if item=="1":
                break
            else:
                self.item_display.append(item)
        self.search_discount_file()
        
    def search_discount_file(self):
        
        folder_file='basic_webscrapper/discounts/'
        file=glob.glob(os.path.join(folder_file,"*.csv"))[0]
        try:
            if not file:
                print("Could not find a csv file")
            else:
                with open(file,"r",encoding="utf-8") as f:
                    reader=csv.reader(f)
                    next(reader)
                    for i in reader:
                        price,name = i
                        has_för=False
                        if "för" in price:
                            one_price=[]
                            has_för=True
                            check_price_for_one = re.sub('för', '', price)
                            check_price_for_one.split(" ")
                            amount=int(check_price_for_one[0])
                            price=int(check_price_for_one[1:])
                            total_for_one=price/amount
                            one_price.append(total_for_one)
                        else:
                            pass
                        for item in self.item_display:
                            if item.lower() in name.lower():
                                if has_för==True:
                                    print(i)
                                    print(f"priset för en är {total_for_one}")
                                    has_för=False
                                else:
                                    print(i)
        except Exception as e:
            return f"Something went wrong,{e}"
        

inst = WalkBot()
inst.ask_person()
