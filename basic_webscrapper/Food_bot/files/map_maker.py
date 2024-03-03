from datetime import date
import datetime 
import os


class Sorter():
    def __init__(self) -> None:
        self.list=[]


    def check_month_item(self):
        
        now=datetime.datetime.now()
        week_year=now.isocalendar()[1]
        year=now.isocalendar()[0]
        date = datetime.date.fromisocalendar(year,week_year,1)
        month = date.strftime('%B')[0:3]        

        return month

    def make_dirs(self):
        folder_file='basic_webscrapper/discounts/archive'
        check_months=1
        while check_months<=12:
            month_name = datetime.date(2024,check_months,1).strftime('%B')[0:3]
            dir_path=os.path.join(folder_file,month_name)
            os.makedirs(dir_path,exist_ok=True)
            check_months+=1


init = Sorter()
# init.check_month_item()
# init.make_dirs()