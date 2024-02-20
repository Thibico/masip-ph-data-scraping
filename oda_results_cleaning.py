import pandas as pd
import sqlite3

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
    
    def get_single_year_data(self) -> pd.DataFrame:
        self.dfs = []
        ## Store list of dfs for different sheets
        for tab in self.gs_db.get_tabs():
            sheet_df = self.gs_db.get_data_as_df(tab)
            final_df = self.clean_single_year_df(sheet_df)
            if final_df is None:
                raise ValueError(f"Check headers from tab : {tab.title}")
            print(f"Append data for tab : {tab.title}")
            self.dfs.append(final_df)
            
        combined_df = pd.concat(self.dfs, ignore_index=True)
        ## check last no. and combined_df rows are the same
        final_row_num = combined_df.shape[0]
        assert self.check_last_index_number(final_row_num), f"Final rows {final_row_num} isn't same as the last sheet's max no."  ## How can I convert into test case?
        
        ## split year_annex name from Gsheet Title
        year_name, annex_name = self.get_spreadsheet_title().split('_')
        combined_df['annex_name'] = annex_name
        combined_df['year'] = int(year_name)
        return combined_df

    def get_spreadsheet_title(self) -> str:
        return self.gs_db.spreadsheet_title

class CleanAllYearsLoans:
    """
    Class to format result loans into correct data type
    Sample dates : 6/30/2009 ,  9/14/2010, 22-Feb-11, 07-Jan-99
    """
    def __init__(self) -> None:
        self.all_sheets_url = "https://docs.google.com/spreadsheets/d/1HSY8-q4LiqtbhIR4fU4Qhn_la3696l1ddqJENB_lQCM/edit#gid=0"
        self.all_sheets_list = GSheetConnector(self.all_sheets_url)
        self.sheets_lst = self.active_oda.get_all_url_list()
        
    def get_all_url_list(self) -> list:
        list_sheets = self.all_sheets_list.get_data_as_df("list_sheets")
        list_sheets, _ = CleaningHelper(list_sheets).get_clean_df()
        return list_sheets['URL'].to_list()

for sheet_url in sheets_lst:
    df_test = active_oda.get_single_year_data(sheets_lst[0])
    headers_lst = df_test.columns.to_list()
    print(df_test.shape)
    
    if len(headers_lst) > 12:
        print(df_test.columns)
    
    print("---x--- \n")


## Import df into sqlite db
# conn = sqlite3.connect('oda.db')
# combined_df.to_sql('active_loan', con=conn, if_exists='replace', index=False)

    
