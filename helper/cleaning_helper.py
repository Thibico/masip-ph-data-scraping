import pandas as pd
import numpy as np
from typing import Tuple, List

class CleaningHelper(object):
  def __init__(self, df: pd.DataFrame):
    self.current_df = df   ## living df that will update in every steps

  ## Replace blank values with np.nan
  def replace_all_blank_values(self):
    return self.current_df.replace(r'^\s*$', np.nan, regex=True, inplace=True)

  ## drop columns that missing all values
  def drop_all_values_blank_cols(self):
    self.current_df.dropna(how= 'all', inplace=True)    ## drop all blank rows
    return self.current_df.dropna(axis = 1, how='all', inplace=True)

  ## drop columns with blank names & longer names
  def drop_blank_longer_names_cols(self):
    cols = self.get_df_columns_list()
    drop_cols = [col for col in cols if len(col)<2 or len(col)> 40]
    return self.current_df.drop(columns=drop_cols, inplace=True)
  
  def get_clean_df(self) -> Tuple[pd.DataFrame, List[str]]:
      """
      Return : clean_df , headers_list
      """
      self.replace_all_blank_values()
      self.drop_all_values_blank_cols()
      return (self.current_df, self.get_df_columns_list())
  
  def get_df_columns_list(self):
    return self.current_df.columns.values.tolist()

  def get_dict_from_2cols(self, key_col:str, value_col:str) -> dict:
    self.get_clean_df()
    return dict(zip(self.current_df[key_col], self.current_df[value_col]))
    
  ## Extract selected data
  def extract_matched_data(self, standard_df, left_col, right_col):
    result_df = pd.merge(self.current_df, standard_df, left_on = left_col, right_on = right_col) ## INNER JOIN method - cols will be combined
    return result_df

  def extract_unmatched_data(self, standard_df, left_col, right_col):
    result_df = pd.merge(self.current_df, standard_df, left_on = left_col, right_on = right_col, how='left', indicator=True)
    result_df = result_df[result_df['_merge'] == 'left_only']
    result_df.drop(columns=['_merge'], inplace=True)
    return result_df

  def set_colValues_withTabName(self, tab_name:str, col_name:str):
    self.current_df[col_name] = tab_name