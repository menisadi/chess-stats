# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

df = pd.read_xml('standard_apr22frl_xml.xml')

df.head()

df.info()

df.describe()

len(df[df['title']=='GM'])
# df['title'].unique()

df[df['title']=='GM'].describe()

gms = df[df['title']=='GM']

sns.histplot(gms['rating'], bins=30)

gms['age'] = gms['birthday'].apply(lambda b: 2022-b)

sns.histplot(gms['age'], bins=30)

df['age'] = df['birthday'].apply(lambda b: 2022-b)

sns.histplot(df['age'], bins=30)

sum(df['title'].notnull())

titled = df[df['title'].notnull()]

sns.histplot(titled['age'], bins=30)

titled.head()

sns.histplot(titled[titled['sex']=='F']['age'], bins=30)

genders_by_age = df.pivot_table(index='age', columns='sex',aggfunc='count',fill_value=0)['rating']

genders_by_age['ratio'] = genders_by_age.apply(lambda x: x.F/(x.F+x.M), axis=1)

genders_by_age

plt.figure(figsize=(10,6))
genders_by_age['ratio'].drop([5,6]).plot(marker='o',
         markerfacecolor='red', markersize=3)
plt.title('Ratio of female chess playes by age')
plt.xlabel('Age')
plt.ylabel('Ratio')

# +
# genders_by_age.groupby(pd.cut(genders_by_age.index, np.arange(5,105,5))).sum()
# # pd.cut(genders_by_age.index, np.arange(5,105,5))[1:-3]
# -

genders_by_dob = df.pivot_table(index='birthday', columns='sex',aggfunc='count',fill_value=0)['rating']
genders_by_dob['ratio'] = genders_by_dob.apply(lambda x: x.F/(x.F+x.M), axis=1)

genders_by_dob.tail()

plt.figure(figsize=(10,6))
genders_by_dob['ratio'].drop([2016,2017]).plot(marker='o',
         markerfacecolor='red', markersize=3)
plt.title('Ratio of female chess playes by Year of birth')
plt.xlabel('Year')
plt.ylabel('Ratio')

rolling = genders_by_dob.rolling(window=5, min_periods=5, ).sum()
rolling['ratio'] = rolling.apply(lambda x: x.F/(x.F+x.M), axis=1)

plt.figure(figsize=(10,6))
rolling['ratio'].plot(marker='o',
         markerfacecolor='red', markersize=3)
plt.title('Rolling 5-year average of the ratio of female chess playes by Year of birth')
plt.xlabel('Year')
plt.ylabel('Ratio')

rolling


