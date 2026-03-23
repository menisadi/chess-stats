# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# %config Completer.use_jedi = False
# %matplotlib inline

# %%
import os

# %%
from tqdm.notebook import tqdm

# %%
import requests

# %%
import re

# %%
from bs4 import BeautifulSoup

# %%
import urllib.request


# %%
def find_files(url):
    soup = BeautifulSoup(requests.get(url).text)

    hrefs = []

    for a in soup.find_all('a'):
        hrefs.append(a['href'])

    return hrefs

def extension(file_link):
    return file_link.split(sep='.')[-1]


# %%
def find_standard_xml_zip(link):
    result = False
    first_split = re.split('/|\.',link)
    second_split = first_split[-2].split(sep='_')
    if first_split[-1] == 'zip':
        if len(second_split) == 3:
            if second_split[0] == 'standard':
                if second_split[2] == 'xml':
                    result = second_split[1][-3:] == 'frl'
    return result


# %%
fide_url = "http://ratings.fide.com/download.phtml?period=2013-03-01" 
list_of_links = find_files(fide_url)

## show what you've found:
for link in list_of_links:
    if find_standard_xml_zip(link):
        print(link)

# %%
exp = 'http://ratings.fide.com/download/standard_mar13frl_xml.zip'

# %%
find_standard_xml_zip(exp)

# %%
years = range(2013,2023)
months = range(1,3)
empty_until_now = True
for year in years:
    for month in months:
        if month < 10:
            fide_url = f"http://ratings.fide.com/download.phtml?period={year}-0{month}-01" 
        else:
            fide_url = f"http://ratings.fide.com/download.phtml?period={year}-{month}-01"
#         print(f'Date: {year}-{month}')
        list_of_links = [link for link in find_files(fide_url) if find_standard_xml_zip(link)]
#         if list_of_links and empty_until_now:
#             empty_until_now = False
        print(f'Date: {year}-{month}')
        print(list_of_links[0])

# %%
all_xml_links = dict()
years = range(2013,2023)
months = range(1,13)
empty_until_now = True
for year in years:
    for month in months:
        date = f'{year}-{month}'
        if month < 10:
            fide_url = f"http://ratings.fide.com/download.phtml?period={year}-0{month}-01" 
        else:
            fide_url = f"http://ratings.fide.com/download.phtml?period={year}-{month}-01"
        list_of_links = [link for link in find_files(fide_url) if find_standard_xml_zip(link)]
        if not list_of_links:
            print(f'Date: {year}-{month}')
        else:
            all_xml_links[date] = list_of_links[0]
#         print(f'Date: {year}-{month}')
#         print(list_of_links[0])
print(len(all_xml_links))

# %%
# for date in tqdm(all_xml_links.keys()):
#     print(date + ".zip")

# %%
os.chdir('./xmls')
 
# verify the path using getcwd()
cwd = os.getcwd()

# %%
# print the current directory
cwd = os.getcwd()
print("Current working directory is:", cwd)

# %%
for date in tqdm(all_xml_links.keys()):
    urllib.request.urlretrieve(all_xml_links[date], date + ".zip")

# %%
