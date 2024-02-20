import requests
from bs4 import BeautifulSoup

class AdbScraper:
    def __init__(self) -> None:
        self.url = "https://www.adb.org/projects/country/philippines?page=4"
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
    
    def find_item_meta(self):
        raw_items_list = self.soup.find_all("div", class_= "item-meta")
        print(len(raw_items_list))
        inside_raw_item = raw_items_list[0].find_all("div")
        
        # inside_raw_item.next_sibling
        for div_item in inside_raw_item:
            print(div_item)
            spans_under_div = div_item.childrens
            print(spans_under_div)

a = AdbScraper().find_item_meta()
