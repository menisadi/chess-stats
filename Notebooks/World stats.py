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

# %% [markdown]
# # Chess Countries' Stats

# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime
# %matplotlib inline
# %config Completer.use_jedi = False

# %%
import plotly.graph_objs as go 
from plotly.offline import init_notebook_mode,iplot,plot
init_notebook_mode(connected=True)

# %%
fide = pd.read_xml("./xmls/standard_aug22frl_xml.xml")

# %%
fide.head()

# %% [markdown]
# ## General info

# %%
# fide.head()

# %%
# fide.describe().transpose()

# %%
# fide['sex'].value_counts()

# %%
# fide.info()

# %% [markdown]
# ## EDA

# %%
fide['title'].value_counts()

# %%

# %%
sns.histplot(data=fide[~fide['title'].isna()], x='rating', kde=True)

# %%
sns.histplot(data=fide[fide['title']=='IM'], x='rating', kde=True)

# %%
sns.histplot(data=fide[fide['title']=='GM'], x='rating', kde=True)

# %%
sns.boxplot(data=fide, y='rating', x='sex')

# %%
sns.histplot(data=fide['games'])

# %%
fide.sort_values('games', ascending=False)

# %%
played_percentege = 100*(fide['games'] > 0).sum()/len(fide['games'])
print(f'{played_percentege}%')

# %%
sns.jointplot(data=fide[fide['games']>0], x='rating', y='games')

# %%
sns.histplot(fide[fide['games']>0]['birthday'])

# %%
sns.histplot(fide['birthday'])

# %%
fide.corr()

# %%
sns.displot(fide[fide['birthday'] > 0]['birthday'])

# %% [markdown]
# ## Feature engineering (titles and countries)

# %% [markdown]
# ### Taking care of a few non-conventional country names

# %%
fide_codes = pd.read_csv('fide_codes.csv')

# %%
fide_codes.head()

# %%
fide_codes.columns = ['country', 'country name']

# %%
codes_dict = fide_codes.set_index('country').to_dict()['country name']

# %%
fide['country name'] = fide['country'].apply(lambda c: codes_dict[c])

# %%
populations = pd.read_csv('pop.csv')

# %%
populations.head()

# %%
pop2022 = populations[['name','pop2022']].set_index('name')
pop2022

# %%
pop2022 = pop2022.append(pd.DataFrame(index=['Swaziland', 'Kosovo'], data=[1160000,1873000], columns=['pop2022']))

# %%
pop2022.rename(index={'United States Virgin Islands':'U.S. Virgin Islands'},inplace=True)

# %%
pop2022.rename(index={'Great Britain':'United Kingdom'},inplace=True)

# %%
pop2022.rename(index={'North Macedonia':'Macedonia'},inplace=True)

# %%
nieche_countries_dict = {
    'Bosnia & Herzegovina' : 'Bosnia and Herzegovina',
    'England' : 'United Kingdom',
    'Wales' : 'United Kingdom',
    'Jersey' : 'United Kingdom',
    'Scotland' : 'United Kingdom',
    'Antigua & Barbuda' : 'Antigua and Barbuda',
     'Chinese Taipei' : 'China',
     'US Virgin Islands' : 'U.S. Virgin Islands',
     'Netherlands Antilles' : 'Netherlands',
     'St. Vincent and the Grenadines' : 'Saint Vincent and the Grenadines',
     'FYR Macedonia' : 'Macedonia',
     'Trinidad & Tobago' : 'Trinidad and Tobago',
     'Democratic Republic of Congo' : 'Zimbabwe',
     "Côte d'Ivoire" : 'Ivory Coast',
     'Guernsey' : 'United Kingdom',
}


# %%
# def temp_fix(c):
#     name = c
#     if name == '"U.S. Virgin Islands':
#         name = 'U.S. Virgin Islands'
#     return name
# fide['country name'] = fide['country name'].apply(temp_fix)

# %%
def fix_some_countries(name):
    new_name = name
    if name in nieche_countries_dict.keys():
        new_name = nieche_countries_dict[name]
    return new_name


# %%
fide['country name'] = fide['country name'].apply(fix_some_countries)

# %%
countries = fide.groupby('country name')

# %%
countries.count()['fideid'].sort_values().head()

# %%
countries.count()['fideid'].sort_values(ascending=False).head()

# %%
# players_per_country

# %%
# fide[fide['country']=='UKR'].count()['fideid']

# %%
# fide[fide['country']=='CHA']

# %%
# median_rating = countries.median()
# median_rating.head()

# %%
fide['is titled'] = fide['title'].apply(lambda t: t is not None)

# %%
fide['is gm'] = fide['title'].apply(lambda t: t=='GM')

# %%
threshold = 2000
fide['above threshold'] = fide['rating'].apply(lambda t: t>=threshold)

# %%
fide['is junior'] = fide['birthday'].apply(lambda d: 20 >= (datetime.now().year - d))

# %%
fide[['name', 'birthday', 'is junior']]

# %%
fide['prodigy'] = fide['is junior'] & fide['above threshold']

# %%
# sns.countplot(data=fide,x='is junior', hue='sex')
# # sns.countplot(data=fide,hue='is junior', x='sex')
# print(100*sum(fide['is junior'])/len(fide))
# print(100*sum(fide[fide['sex']=='M']['is junior'])/len(fide[fide['sex']=='M']))
# print(100*sum(fide[fide['sex']=='F']['is junior'])/len(fide[fide['sex']=='F']))

# %%
# sns.histplot(fide[fide['sex']=='F'], x='rating', hue='is junior')

# %%
by_country = fide.groupby('country name')

# %%
players_per_country = by_country.count()['fideid']

# %%
# codes_dict = codes_dict['country name']

# %%
# problematic = list(set(median_rating.index).difference(set(fide_codes['country name'])))
# problematic

# %%
# fide[fide['country'].isin(problematic)]

# %%
# fide.head()

# %%
# pop2022.loc['Kosovo']

# %%

# %%
# non_pop = list(set(median_rating.index).difference(set(pop2022.index)) - set(['Bosnia & Herzegovina', 'England','Wales','Jersey','Scotland']))
# non_pop

# %%

# %%
# sns.histplot(fide[fide['country name']=='Yemen']['rating'])
fide[fide['country name']=='Cambodia']

# %%
# set(feds.index).intersection(set(pop2022))

# %%
# feds.index

# %%
# codes = pd.read_csv('codes.csv')

# %%
# codes.head()

# %%
# codes.set_index('Code',inplace=True)

# %%
# codes.info()

# %%
# codes.head()

# %%
# codes.index

# %%
# feds.index

# %%
# len(set(feds.index).intersection(set(codes.index)))

# %%
# set(feds.index) - set(codes.index)

# %% [markdown]
# ## Maps

# %%
median_countries = by_country.median()

data = dict(
        type = 'choropleth',
        colorscale = 'thermal',
        locations = median_countries.index,
        locationmode = "country names",
        z = median_countries['rating'],
        text = median_countries['rating'],
        colorbar = {'title' : 'Rating By Countery'},
      )

# %%
layout = dict(title = 'Rating Median By Countery',
              geo = dict(projection = {'type':'mercator'})
             )

# %%
choromap = go.Figure(data = [data],layout = layout)
iplot(choromap,validate=False)

# %%
mean_countries = by_country.mean()

# %%
data = dict(
        type = 'choropleth',
        colorscale = 'thermal',
        locations = mean_countries.index,
        locationmode = "country names",
        z = mean_countries['rating'],
        text = mean_countries['rating'],
        colorbar = {'title' : 'Rating By Countery'},
      )

layout = dict(title = 'Rating Mean By Countery',
              geo = dict(projection = {'type':'mercator'})
             )

choromap = go.Figure(data = [data],layout = layout)
iplot(choromap,validate=False)

# %%
data = dict(
        type = 'choropleth',
        colorscale = 'thermal',
        locations = players_per_country.index,
        locationmode = "country names",
        z = players_per_country,
        text = players_per_country,
        colorbar = {'title' : 'Players By Countery'},
      )

layout = dict(title = 'Players By Countery',
              geo = dict(projection = {'type':'mercator'})
             )

choromap = go.Figure(data = [data],layout = layout)
iplot(choromap,validate=False)

# %%
gms_by_country = by_country.sum()['is gm']
titled_by_country = by_country.sum()['is titled']

# %%
data = dict(
        type = 'choropleth',
        colorscale = 'thermal',
        locations = gms_by_country.index,
        locationmode = "country names",
        z = gms_by_country,
        text = gms_by_country,
        colorbar = {'title' : 'GMs By Countery'},
      )

layout = dict(title = 'GMs By Countery',
              geo = dict(projection = {'type':'mercator'})
             )

choromap = go.Figure(data = [data],layout = layout)
iplot(choromap,validate=False)

# %%
data = dict(
        type = 'choropleth',
        colorscale = 'thermal',
        locations = titled_by_country.index,
        locationmode = "country names",
        z = titled_by_country,
        text = titled_by_country,
        colorbar = {'title' : 'Rating By Countery'},
      )

layout = dict(title = 'Titled Players By Countery',
              geo = dict(projection = {'type':'mercator'})
             )

choromap = go.Figure(data = [data],layout = layout)
iplot(choromap,validate=False)

# %%
prodigies_by_counry = by_country.sum()['prodigy']

# %%
data = dict(
        type = 'choropleth',
        colorscale = 'thermal',
        locations = prodigies_by_counry.index,
        locationmode = "country names",
        z = prodigies_by_counry,
        text = prodigies_by_counry,
        colorbar = {'title' : 'Prodigies By Countery'},
      )

layout = dict(title = 'Prodigies By Countery',
              geo = dict(projection = {'type':'mercator'})
             )

choromap = go.Figure(data = [data],layout = layout)
iplot(choromap,validate=False)

# %%

# %% [markdown]
# ## And now Lets Normalize!

# %%
list_of_series = [players_per_country.drop('FIDE'), 
                  pop2022.loc[players_per_country.drop('FIDE').index]['pop2022'], 
                 titled_by_country, 
                 gms_by_country,
                 prodigies_by_counry]
countries_data = pd.concat(list_of_series, axis=1)

# %%
countries_data.rename(columns={'fideid': 'players'}, inplace=True)
countries_data.head()

# %%
countries_data_normalized = pd.DataFrame()
countries_data_normalized['players'] = countries_data['players'] / countries_data['pop2022']
countries_data_normalized['is titled'] = countries_data['is titled'] / countries_data['pop2022']
countries_data_normalized['is gm'] = countries_data['is gm'] / countries_data['pop2022']
countries_data_normalized['prodigy'] = countries_data['prodigy'] / countries_data['pop2022']
countries_data_normalized['pop2022'] = countries_data['pop2022']

# %%
countries_data_normalized.head()

# %%
filter_smallest = countries_data_normalized[countries_data_normalized['pop2022'] > 500]

# %%
data = dict(
        type = 'choropleth',
        colorscale = 'thermal',
        locations = filter_smallest.index,
        locationmode = "country names",
        z = filter_smallest['players'],
        text = filter_smallest['players'],
        colorbar = {'title' : 'Players per 1000 people'},
      )

layout = dict(title = 'Players By Countery - Normalized',
              geo = dict(projection = {'type':'mercator'})
             )

choromap = go.Figure(data = [data],layout = layout)
iplot(choromap,validate=False)

# %%
data = dict(
        type = 'choropleth',
        colorscale = 'thermal',
        locations = filter_smallest.index,
        locationmode = "country names",
        z = filter_smallest['is gm']*100,
        text = filter_smallest['is gm']*100,
        colorbar = {'title' : 'Gms per 1e5 people'},
      )

layout = dict(title = 'GMs By Countery - Normalized',
              geo = dict(projection = {'type':'mercator'})
             )

choromap = go.Figure(data = [data],layout = layout)
iplot(choromap,validate=False)

# %%
data = dict(
        type = 'choropleth',
        colorscale = 'thermal',
        locations = filter_smallest.index,
        locationmode = "country names",
        z = filter_smallest['is titled']*100,
        text = filter_smallest['is titled']*100,
        colorbar = {'title' : 'Titled players per 1e5 people'},
      )

layout = dict(title = 'Titled players By Countery - Normalized',
              geo = dict(projection = {'type':'mercator'})
             )

choromap = go.Figure(data = [data],layout = layout)
iplot(choromap,validate=False)

# %% [markdown]
# ## Same thing but in tables

# %%
filter_smallest['is gm'].sort_values(ascending=False).head(10)*100

# %%
filter_smallest['is titled'].sort_values(ascending=False).head(20)*100

# %%
filter_smallest['players'].sort_values(ascending=False).head(21)*100

# %%
filter_smallest['prodigy'].sort_values(ascending=False).head(20)*100

# %%
# sns.countplot(data=filter_smallest.head(10), y='Prodigies')
# filter_smallest['Prodigies'].sort_values().plot(kind='bar')
(100*filter_smallest['Prodigies'].sort_values(ascending=False).head(20)).plot(kind='bar')

# %%
# filter_smallest.rename(columns={'is gm':'GMs', 'is titled':'Titled Players', 'prodigy' : 'Prodigies', 'pop2022' : 'Population'},inplace=True)
sns.heatmap(filter_smallest.corr(), annot=True, cmap='coolwarm')

# %% [markdown]
# ### Cheking on the big names

# %%
filter_smallest.rename(columns={'is gm':'gms', 'is titled':'titled'},inplace=True)

# %%
# filter_smallest['gms'] = filter_smallest['gms'].apply(lambda x:x*100)
# filter_smallest['titled'] = filter_smallest['titled'].apply(lambda x:x*100)
# filter_smallest['players'] = filter_smallest['players'].apply(lambda x:x*100)
filter_smallest.loc[['Croatia','Israel','Norway', 
                     'United States of America', 'Russia', 'China', 'India', 'Germany']]*100

# %%
countries_data_per1e5 = filter_smallest*100

# %%
c = countries_data_per1e5.reset_index()
c = c[(c['players'] > 50) | (c['is gm'] > 0.4)]
c = c.reset_index()

# %%
plt.figure(figsize=(12,8))

sns.scatterplot(data=countries_data_per1e5, x='players', y='is gm')
for i in range(c.shape[0]):
    plt.text(x=c.loc[i]['players']+0.03,y=c.loc[i]['is gm']+0.03,s=c.loc[i]['country name'])

plt.title('Playes vs GMs')
plt.xlabel('No. Players per 100k') #x label
plt.ylabel('No. GMs per 100k') #y label

# %%
c2 = countries_data_per1e5.reset_index()
c2 = c2[(c2['prodigy'] > 0.5) | (c2['is gm'] > 0.35)]
c2 = c2.reset_index()

# %%
plt.figure(figsize=(12,8))

sns.scatterplot(data=countries_data_per1e5, x='is gm', y='prodigy')
for i in range(c2.shape[0]):
    plt.text(y=c2.loc[i]['prodigy'],x=c2.loc[i]['is gm']+0.01,s=c2.loc[i]['country name'])

plt.title('Prodigy vs GMs')
plt.ylabel('No. Prodigies per 100k') #x label
plt.xlabel('No. GMs per 100k') #y label

# %%

# %%
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
init_notebook_mode(connected=True)
cf.go_offline()
import plotly.express as px

# %%
go.Figure(go.Scatter(
    x=countries_data_per1e5['players'], y=countries_data_per1e5['is gm'],
    text=countries_data_per1e5.index,
    mode='markers',
    name='%{x}:%{y}'
))                       

# %%
countries_data_per1e5.sort_values(by='players')

# %%
median_players = countries_data['players'].median()
top_players_countries = countries_data['players'].nlargest(20)
# countries_data[countries_data['players'] > median_players].corr()
top_20_countries_by_players = countries_data.loc[top_players_countries.index]
top_20_countries_by_players.corr()

# %%
sns.lmplot(data=top_20_countries_by_players, x='players', y='is gm')

# %%
