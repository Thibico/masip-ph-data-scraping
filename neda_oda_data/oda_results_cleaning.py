import pandas as pd
import numpy as np
import sqlite3
import time
import re
from datetime import datetime

from helper.gsheet_connector import GSheetConnector
from helper.cleaning_helper import CleaningHelper

class YearlyLoansCleaner:
    def __init__(self, year_url:str) -> None:
        self.gs_db = GSheetConnector(year_url)
        
    def check_last_index_number(self, final_df_row_num:int) -> str:
        last_tab_df = self.dfs[-1]
        no_col = last_tab_df['No.'].astype(int)
        max_no_col = no_col.max()
        return f"Check Last No. : {max_no_col == final_df_row_num}"
    
    def clean_single_year_df(self, sheet_df : pd.DataFrame) -> pd.DataFrame:
        cols_std = None
        ## Clean blank rows and blank columns
        clean_helper = CleaningHelper(sheet_df)
        final_df, final_cols = clean_helper.get_clean_df()
        if cols_std is None:
            cols_std = sorted(final_cols)
            
        ## Return None is two cols aren't equal
        elif cols_std != sorted(final_cols):
            print(f"Not equal header columns : {final_cols}")
            return None
        return final_df
    
    @staticmethod
    def get_page_number(tab_title : str) -> str:
        return tab_title.replace('Sheet', 'Page_')
    
    def get_single_year_data(self) -> pd.DataFrame:
        self.dfs = []
        ## Store list of dfs for different sheets
        for tab in self.gs_db.get_tabs():
            sheet_df = self.gs_db.get_data_as_df(tab)
            if sheet_df.empty:
                raise ValueError(f"sheet_df return Empty : {tab.title}")
            
            final_df = self.clean_single_year_df(sheet_df)
            if final_df is None:
                raise ValueError(f"Check headers from tab : {tab.title}")
            final_df['annex_page_num'] = self.get_page_number(tab.title)
            self.dfs.append(final_df)
            time.sleep(5)
            
        combined_df = pd.concat(self.dfs, ignore_index=True)
        ## check last no. and combined_df rows are the same
        final_row_num = combined_df.shape[0]
        assert self.check_last_index_number(final_row_num), f"Final rows {final_row_num} isn't same as the last sheet's max no."  ## How can I convert into test case?
        
        ## split year_annex name from Gsheet Title
        year_name, annex_name = self.get_spreadsheet_title().split('_')
        combined_df['annex_name'] = annex_name
        combined_df['annex_year'] = int(year_name)
        return combined_df

    def get_spreadsheet_title(self) -> str:
        return self.gs_db.spreadsheet_title

class CleanAllYearsLoans:
    """
    Class to final clean headers and format all year results into correct data type
    Sample dates : 6/30/2009 ,  9/14/2010, 22-Feb-11, 07-Jan-99
    """
    def __init__(self) -> None:
        self.all_sheets_url = "https://docs.google.com/spreadsheets/d/1HSY8-q4LiqtbhIR4fU4Qhn_la3696l1ddqJENB_lQCM/edit#gid=0"
        self.all_sheets_list = GSheetConnector(self.all_sheets_url)
        self.sheets_lst = self.get_all_url_list()
        self.final_df = None
        self.std_headers_dict = None
        
    def get_all_url_list(self) -> list:
        list_sheets = self.all_sheets_list.get_data_as_df("list_sheets")
        list_sheets, _ = CleaningHelper(list_sheets).get_clean_df()
        return list_sheets['URL'].to_list()

    def get_std_headers(self) -> dict:
        std_headers_sh = self.all_sheets_list.get_data_as_df("std_headers")
        std_headers_dict = CleaningHelper(std_headers_sh).get_dict_from_2cols("original_col", "clean_col")
        return std_headers_dict
    
    def clean_headers(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.std_headers_dict is None:
            self.std_headers_dict = self.get_std_headers()
        df.rename(columns = self.std_headers_dict, inplace=True)
        return df
    
    def format_date_column(self, original_date:str):
        ## Return string as formatted : MMM(M)-DD-YYYY : February 18, 2024
        if re.fullmatch(r"^(?:\d{1,2}\/){2}\d{4}$", original_date):
            return datetime.strptime(original_date, "%m/%d/%Y").strftime("%B %d, %Y")
        elif re.fullmatch(r"^\d{1,2}-\w{3}-\d{2}$", original_date):
            return datetime.strptime(original_date, "%d-%b-%y").strftime("%B %d, %Y")
        else:
            print(f"Unknown format : {original_date}")
            return original_date
    
    def format_all_date_columns(self, year_df: pd.DataFrame, selected_cols: list) -> pd.DataFrame:
        year_df[selected_cols] = year_df[selected_cols].replace({np.nan: None})    ## replace np.nan with None value
        for col in selected_cols:
            year_df[col] = year_df[col].apply(lambda date_str : self.format_date_column(str(date_str).strip()) if (date_str and str(date_str) != '1/0/1900') else '')
        return year_df
    
    @staticmethod
    def find_date_columns(all_cols : list) -> list:
        return [col for col in all_cols if re.search(r"_date$", col)]
    
    def allYears_data_cleaning(self):
        dfs = []
        for sheet_url in self.sheets_lst:
            year_df = YearlyLoansCleaner(sheet_url).get_single_year_data()
            ## clean headers for each year
            year_df = self.clean_headers(year_df)
            year_df_date_cols = self.find_date_columns(year_df.columns.to_list())
            year_df = self.format_all_date_columns(year_df, year_df_date_cols)
            
            dfs.append(year_df)
            print("---X---")    
        self.final_df = pd.concat(dfs, ignore_index=True)
        return self.final_df
        
    def export_to_sqlite(self, df: pd.DataFrame):
        conn = sqlite3.connect('oda.db')
        df.to_sql('active_loan', con=conn, if_exists='replace', index=False)
        print("Succesfully imported into sqlite.")

clean = CleanAllYearsLoans()
clean_all_df = clean.allYears_data_cleaning()
print("Cleaning Done!")
print(clean_all_df.shape)
print(clean_all_df.columns)

## Export to csv
clean_all_df.to_csv("active_loans.csv", index=False)
## Export to sqlite
clean.export_to_sqlite(clean_all_df)
print("Exporting to SQL finished.")





    
