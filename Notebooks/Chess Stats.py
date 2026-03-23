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
# # Putting It All Together

# %% [markdown]
# *This time using GeoPandas instead of Plotly*

# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import os
from datetime import datetime
# %matplotlib inline

# %%
# !pwd

# %%
# fide = pd.read_xml("./xmls/standard_dec22frl_xml.xml")
fide = pd.read_xml("../xmls/standard_aug22frl_xml.xml")

# %%
fide_codes = pd.read_csv('../Data/fide_codes.csv')

# %%
fide.head()

# %% [markdown]
# ## Feature engineering (titles and countries)

# %% [markdown]
# ### Adding names of countries

# %%
fide_codes.columns = ['country', 'country name']
codes_dict = fide_codes.set_index('country').to_dict()['country name']
fide['country name'] = fide['country'].apply(lambda c: codes_dict.get(c))

# %%
fide[fide['country name'].isna()]

# %%
fide.loc[fide['country'] == 'GEQ', 'country name'] = 'Equatorial Guinea'
fide.loc[fide['country'] == 'SKN', 'country name'] = 'Saint Kitts and Nevis'

# %% [markdown]
# ### Adding each country population stat

# %%
populations = pd.read_csv('../Data/pop.csv')

# %%
pop2022 = populations[['name','pop2022']].set_index('name')

# %%
pop2022 = pd.concat([pop2022, pd.DataFrame(index=['Swaziland', 'Kosovo'], data=[1160,1873], columns=['pop2022'])])
pop2022.rename(index={'United States Virgin Islands':'U.S. Virgin Islands'},inplace=True)
pop2022.rename(index={'Great Britain':'United Kingdom'},inplace=True)
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
def fix_some_countries(name):
    new_name = name
    if name in nieche_countries_dict.keys():
        new_name = nieche_countries_dict[name]
    return new_name


# %%
fide['country name'] = fide['country name'].apply(fix_some_countries)

# %%
fide.drop(['o_title', 'foa_title', 'games', 'k', 'flag'], axis=1, inplace=True)

# %% [markdown]
# ### Adding features

# %%
fide['is gm'] = fide['title'].apply(lambda t: t=='GM')

# %%
threshold = 2000
fide[f'above {threshold}'] = fide['rating'].apply(lambda t: t>=threshold)

# %%
fide['is junior'] = fide['birthday'].apply(lambda d: 20 >= (datetime.now().year - d))

# %%
fide['is prodigy'] = fide['is junior'] & fide[f'above {threshold}']

# %%
fide['is_titled'] = ~fide['title'].isna()

# %%
fide.loc[fide['is_titled'], 'country name'].value_counts().head(10)

# %%
sum(fide['is gm'])

# %%
sum(~fide['title'].isna())/len(fide)

# %% [markdown]
# ## The stats

# %% [markdown]
# ### Tabular view and bar plots

# %%

# %%
by_country = fide.groupby('country name')

# %%
players_per_country = by_country.count()['fideid']
gms_by_country = by_country['is gm'].sum()
prodigies_by_counry = by_country['is prodigy'].sum()

# %%
sexes = fide.groupby(['country name', 'sex']).size().unstack(fill_value=0)
females_by_country = sexes['F']
# females_by_country = sexes['F'] / sexes.sum(axis=1)

# %%
ppc = pd.DataFrame(players_per_country.sort_values(ascending=False).head(10))
ppc.index.name = 'Country'
ppc.columns = ['Players']
ppc

# %%
ppc.plot.bar()
plt.xticks(rotation=45, ha='right', wrap=True)
plt.tight_layout()

# %%
gmpc = pd.DataFrame(gms_by_country.sort_values(ascending=False).head(10))
gmpc.index.name = 'Country'
gmpc.columns = ['GMs']
gmpc

# %%
gmpc.plot.bar()
plt.xticks(rotation=45, ha='right', wrap=True)
plt.tight_layout()

# %%
prpc = pd.DataFrame(prodigies_by_counry.sort_values(ascending=False).head(10))
prpc.index.name = 'Country'
prpc.columns = ['Prodigies']
prpc

# %%
prpc.plot.bar()
plt.xticks(rotation=45, ha='right', wrap=True)
plt.tight_layout()

# %%
fpc = pd.DataFrame(females_by_country.sort_values(ascending=False).head(10))
fpc.index.name = 'Country'
fpc.columns = ['Players']
fpc

# %%
fpc.plot.bar()
plt.xticks(rotation=45, ha='right', wrap=True)
plt.tight_layout()

# %%
fide.columns

# %%
players_and_titles = by_country.agg({'fideid': 'count', 'is_titled': 'sum', 'is gm': 'sum'})

# %%
players_and_titles['gm_ratio'] = players_and_titles['is gm'] / players_and_titles['fideid']
players_and_titles['titled_ratio'] = players_and_titles['is_titled'] / players_and_titles['fideid']

# %%
players_and_titles.loc[['Russia', 'India', 'United States of America', 'Israel']]

# %%
players_and_titles[
    players_and_titles['fideid'] > 1000].sort_values(
    by='gm_ratio', ascending=False).head(20)[
    ['fideid', 'is gm', 'gm_ratio']]

# %%
players_and_titles[
    players_and_titles['fideid'] > 1000].sort_values(
    by='titled_ratio', ascending=False).head(20)[
    ['fideid', 'is_titled', 'titled_ratio']]

# %% [markdown]
# ### Graphical view - world maps

# %% [markdown]
# #### players per country

# %%
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[(world.pop_est>0) & (world.name!="Antarctica")]
merged = world.merge(players_per_country, left_on='name', right_on='country name', how='left')
merged['fideid'].fillna(0, inplace=True)

# %%
merged.plot(column='fideid', cmap='viridis', legend=True, figsize=(10,6),
           legend_kwds={'label': "Players",
                        'orientation': "horizontal"})

# %% [markdown]
# #### Gms per country

# %%
merged_gms = world.merge(gms_by_country, left_on='name', right_on='country name', how='left')
merged_gms['is gm'].fillna(0, inplace=True)

# %%
merged_gms.plot(column='is gm', cmap='viridis', legend=True, figsize=(10,6),
           legend_kwds={'label': "GMs",
                        'orientation': "horizontal"})

# %% [markdown]
# #### Prodigies by counry

# %%
merged_prs = world.merge(prodigies_by_counry, left_on='name', right_on='country name', how='left')
merged_prs['is prodigy'].fillna(0, inplace=True)

# %%
merged_prs.plot(column='is prodigy', cmap='viridis', legend=True, figsize=(10,6),
           legend_kwds={'label': "Prodigies",
                        'orientation': "horizontal"})

# %% [markdown]
# #### Female Players per country

# %%
merged_fms = world.merge(females_by_country, left_on='name', right_on='country name', how='left')
merged_fms['F'].fillna(0, inplace=True)

# %%
merged_fms.plot(column='F', cmap='viridis', legend=True, figsize=(10,6),
           legend_kwds={'label': "Prodigies",
                        'orientation': "horizontal"})

# %% [markdown]
# ## Let's Normalize

# %%
merged_ppc = merged.rename({'fideid': 'players'}, axis=1)

# %%
# merged_ppc.merge(merged_gms, on=

# %%
from functools import reduce

# %%
data_frames = [merged_ppc, merged_gms, merged_prs, merged_fms]
countries_data = reduce(lambda  left,right: pd.merge(left,right, 
                                                on=['pop_est', 'continent', 'name', 'iso_a3', 'gdp_md_est', 'geometry'],
                                                how='inner'), data_frames)

# %%
countries_data['players pc'] = 1000000 * countries_data['players'] / countries_data['pop_est']
countries_data['gms pc'] = 1000000 * countries_data['is gm'] /  countries_data['pop_est']
countries_data['prodigies pc'] = 1000000 * countries_data['is prodigy'] /  countries_data['pop_est']
countries_data['females pc'] = 1000000 * countries_data['F'] /  countries_data['pop_est']

# %%
countries_data.head()

# %% [markdown]
# ### Plot the data

# %%
countries_data.set_index('name')['players pc'].sort_values(ascending=False).head(10).plot.bar()
plt.xticks(rotation=45, ha='right', wrap=True)
plt.tight_layout()

# %%
countries_data.set_index('name')['gms pc'].sort_values(ascending=False).head(10).plot.bar()
plt.xticks(rotation=45, ha='right', wrap=True)
plt.tight_layout()

# %%
countries_data.set_index('name')['prodigies pc'].sort_values(ascending=False).head(10).plot.bar()
plt.xticks(rotation=45, ha='right', wrap=True)
plt.tight_layout()

# %%
countries_data.set_index('name')['females pc'].sort_values(ascending=False).head(10).plot.bar()
plt.xticks(rotation=45, ha='right', wrap=True)
plt.tight_layout()

# %% [markdown]
# ### Iceland has to go (it's messing with the scale)

# %%
countries_data = countries_data[countries_data['name']!='Iceland']

# %%
countries_data.set_index('name')['players pc'].sort_values(ascending=False).head(10).plot.bar()
plt.xticks(rotation=45, ha='right', wrap=True)
plt.tight_layout()

# %%
countries_data.set_index('name')['gms pc'].sort_values(ascending=False).head(10).plot.bar()
plt.xticks(rotation=45, ha='right', wrap=True)
plt.tight_layout()

# %%
countries_data.set_index('name')['prodigies pc'].sort_values(ascending=False).head(10).plot.bar()
plt.xticks(rotation=45, ha='right', wrap=True)
plt.tight_layout()

# %%
countries_data.set_index('name')['females pc'].sort_values(ascending=False).head(10).plot.bar()
plt.xticks(rotation=45, ha='right', wrap=True)
plt.tight_layout()

# %% [markdown]
# ### Maps

# %%
countries_data.plot(column='players pc', cmap='viridis', legend=True, figsize=(10,6),
           legend_kwds={'label': "Players Per Capita",
                        'orientation': "horizontal"})

# %%
countries_data.plot(column='gms pc', cmap='viridis', legend=True, figsize=(10,6),
           legend_kwds={'label': "GMs Per Capita",
                        'orientation': "horizontal"})

# %%
countries_data.plot(column='prodigies pc', cmap='viridis', legend=True, figsize=(10,6),
           legend_kwds={'label': "Prodigies Per Capita",
                        'orientation': "horizontal"})

# %%
countries_data.plot(column='females pc', cmap='viridis', legend=True, figsize=(10,6),
           legend_kwds={'label': "Female Players Per Capita",
                        'orientation': "horizontal"})

# %% [markdown]
# #### Zoom on Euroasia

# %%
euroasia = countries_data[(countries_data['continent']=='Asia') | (countries_data['continent']=='Europe')]

# %%
euroasia.plot()

# %%
russia_polygon = euroasia[euroasia['name']=='Russia']['geometry']
russia_polygon.plot()

# %%
from shapely.geometry import MultiPolygon

# %%
russia_without_the_east = MultiPolygon(russia_polygon.explode(index_parts=True)[:11].tolist())
russia_without_the_east

# %%
euroasia.loc[euroasia['name']=='Russia', 'geometry'] = russia_without_the_east
euroasia.plot()

# %%
euroasia[euroasia.geometry.bounds.minx==euroasia.geometry.bounds.minx.min()]

# %%
france_polygon = euroasia[euroasia['name']=='France']['geometry']
france_without_the_east = MultiPolygon(france_polygon.explode(index_parts=True)[1:].tolist())
france_without_the_east

# %%
euroasia.loc[euroasia['name']=='France', 'geometry'] = france_without_the_east
euroasia.plot()

# %%
euroasia.plot(column='players pc', cmap='viridis', legend=True, figsize=(10,6),
           legend_kwds={'shrink':0.75})
plt.title("Players Per 1M People in Euroasia")

# %%
euroasia.plot(column='gms pc', cmap='viridis', legend=True, figsize=(10,6),
           legend_kwds={'shrink':0.75})
plt.title("GMs Per 1M People in Euroasia")

# %%
euroasia.plot(column='prodigies pc', cmap='viridis', legend=True, figsize=(10,6),
           legend_kwds={'shrink':0.75})
plt.title("Prodigies Per 1M People in Euroasia")

# %%
euroasia.plot(column='females pc', cmap='viridis', legend=True, figsize=(10,6),
           legend_kwds={'shrink':0.75})
plt.title("Female Players Per 1M People in Euroasia")

# %% [markdown]
# **And Thas Is It For Now**

# %%
