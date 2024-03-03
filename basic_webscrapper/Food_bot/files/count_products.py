import pandas as pd
import glob
import os

class ProductSorter:
    def __init__(self) -> None:
        pass

    def read_write_new_csv_files(self):
        folder_file='basic_webscrapper/discounts/'
        csv_files=glob.glob(os.path.join(folder_file,"*.csv"))
        df_list=[]
        for i in csv_files:
            df=pd.read_csv(f"{i}",skiprows=1)
            df=df[df.columns[:2]]
            df.columns=['col1','col2']
            df_list.append(df)
        # print(df_list)
        combined_dfs=pd.concat(df_list,ignore_index=True)
        print(combined_dfs)
        value_count=combined_dfs['col2'].value_counts().reset_index()
        
        value_count.columns=["Produkt","Hur ofta produkten varit på rea"]
        # print(value_count)   
        df=pd.DataFrame(value_count)
        df.to_csv(r"RootDir\frequent_product.csv",index=False)

        sort_count=combined_dfs.sort_values('col2').reset_index(drop=True)
        # print(sort_count)
        df=pd.DataFrame(sort_count)
        df.to_csv(r"RootDir\sort_product.csv",index=False)


init = ProductSorter()
init.read_write_new_csv_files()

