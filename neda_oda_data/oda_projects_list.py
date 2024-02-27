## Python Script to analyse downloaded pdf names and move all Annex files into one folder
from pathlib import Path
import re

current_wd = Path.cwd()

p = Path("./data/NEDA_ODA_Collections")

## Get all years folders
all_portfolio_folders = [x for x in p.iterdir() if x.is_dir()]

## List of dictionary to record file count
file_count_data = []
# annex_dict = {"folder_name": 'test', "annex_count" : 0, "non_annex_count": 0}
annex_dict = {}
annex_filenames = []
for folder in all_portfolio_folders:
    ## Loop through all sub-folder under each portfolio folder
    annex_dict["folder_name"] = str(folder)
    annex_count = 0
    non_annex_count = 0
    for sub_folder_file in folder.iterdir():
        ## Find and Count Annex files
        if re.search("[Aa]nnex-", str(sub_folder_file)):
            # print(sub_folder)
            annex_count += 1

            ## clean filename
            clean_filename = re.match(
                "^data\/NEDA_ODA_Collections\/.*\/(.*?)\.\w+", str(sub_folder_file)
            )[1]
            annex_filenames.append(clean_filename)
        else:
            # print(f"{sub_folder_file} inside {folder}")
            non_annex_count += 1
    annex_dict["annex_count"] = annex_count
    annex_dict["non_annex_count"] = non_annex_count
    file_count_data.append(annex_dict)
print(len(file_count_data))
print(file_count_data[0])

## get unique set of annex filenames
print(len(annex_filenames))
print(len(set(annex_filenames)))
## Create folder for Annex files

## Move Annex file to assigned folder
