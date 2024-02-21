import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from pathlib import PosixPath
import pandas as pd
import time

## Additional libs or exceptions
from gspread.exceptions import WorksheetNotFound, SpreadsheetNotFound, APIError
from typing import List, Optional

## To read secret file
import os
from dotenv import load_dotenv
## load env secrets
load_dotenv()

## Pandas - SettingWithCopyError warning hidden : default - 'warn'
pd.options.mode.chained_assignment = None

class GSheetConnector:
  def __init__(self, sheet_url) -> None:
        ## Get location as PosixPath object
        self.__location = PosixPath(os.getenv('gspread_location'))
        self._gc = gspread.oauth(credentials_filename= self.__location)
        self._sheet_url = sheet_url
        self._current_tab = None
        self.connect_gsheet()
        
  def connect_gsheet(self):
    try:
      self._get_sheet = self._gc.open_by_url(self._sheet_url)
      self.spreadsheet_title = self._get_sheet.title
    except WorksheetNotFound or SpreadsheetNotFound as e:
      raise AttributeError(f"Recheck sheet {self.spreadsheet_title} is existing.") from e
    except Exception as e:
      print(f"Check error : {e}")
      ## add delay and retry
      time.sleep(5)
      self.connect_gsheet()
      print(f"After delayed {self.spreadsheet_title}: Connected!")

  def get_tabs(self):
    """
    Get a list of all worksheets tab
    """
    get_all_tabs = self._get_sheet.worksheets()
    return get_all_tabs

  def get_data_as_df(self, ws : gspread.worksheet.Worksheet | str):
    """
    ws : Gspread Worksheet Object (or) tab name
    """
    if isinstance(ws, str):
      ws = self._get_sheet.worksheet(ws)
    self._current_tab = ws.title
    try:
      # print(f"Getting data from {self._current_tab} under {self.spreadsheet_title}")
      df = get_as_dataframe(ws, skipfooter = 900, skip_blank_lines = True)
      print(f"Shape for {self._current_tab} under {self.spreadsheet_title} : {df.shape}") ## Should I add logging?
      if df.shape[0] == 0:
        raise ValueError(f"Return shape under {self.spreadsheet_title} is being zero.")
      return df
    except APIError:
      print(f"API error happened for {self.spreadsheet_title}:{self._current_tab}. Need to wait 60 sec & refresh")
      time.sleep(60) ## wait 1 min to pass Google quota limit
      print(f"After API delayed {self.spreadsheet_title}:{self._current_tab} - Restart!")
      return self.get_data_as_df(ws)
    except Exception as e:
      print(f"Other errors : {e}")
  
  ## Export to Google Sheets
  def load_data(self, df, sheet_name: str):
    # self.connect_gsheet()
    try:
      test_sheet = self._get_sheet.add_worksheet(title=sheet_name,rows="10000",cols="10")
    except Exception:
      test_sheet = self._get_sheet.worksheet(sheet_name)
      test_sheet.clear()
    set_with_dataframe(test_sheet,df)
    print("Finish export to GSheet")

  ## Save as csv on Google Drive
  def save_csv_gdrive(self, export_df, filename: str):
    export_location = f"/content/drive/My Drive/colab_export/{filename}.csv"
    export_df.to_csv(export_location, index=False)
    print(f"CSV exported to - {export_location}")

  @property
  def tab_name(self):
    return self._tab_name