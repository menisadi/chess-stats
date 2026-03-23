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
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

# %%
years = {}
for y in range(13,23):
    years[y] = pd.read_csv("FIDEmarch"+str(y)+".csv")

# %%
years[20].head()

# %%
years[13]['Sex'].value_counts()

# %%
gender_list = [y['Sex'].value_counts() for y in years.values()]
gender = pd.concat(gender_list, axis=1)
gender.columns = list(range(2013,2023))

# %%
gender_list_normalized = [y['Sex'].value_counts(normalize=True) for y in years.values()] 
gender_normalized = pd.concat(gender_list_normalized, axis=1)
gender_normalized.columns = list(range(2013,2023))

# %%
gender_normalized[2013]

# %%
gender.transpose().head()

# %%
# sns.lineplot(data=gender_normalized.loc['M'])
# sns.barplot(data=gender_normalized)
gender_normalized.transpose().reset_index().plot(x = 'index',
    kind = 'bar',
    stacked = True,
    title = 'Percentage of Male and Female chess players',
    mark_right = True)

# %%

# %%
