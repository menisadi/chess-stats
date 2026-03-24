# Chess - Popularity  
The world of chess has experienced an increase in popularity in recent years.  
Since the broadcast of the "Queen's Gambit" series on Netflix, this ancient game has been gaining momentum online, a momentum that received an even greater boost during the COVID-19 pandemic when many remained locked in their homes and sought activities to engage with online.  
Chess provides a perfect solution as it can be played online with people from all over the world, offering an escape from the monotony of lock-down and providing a mental challenge to players.  
Additionally, the rise of online streaming platforms such as Twitch has made it possible for professional chess players to stream their games and provide commentary, further increasing the visibility of the game and inspiring a new generation of chess enthusiasts.  
As a result, the popularity of chess continues to grow, with tournaments attracting large audiences and players of all skill levels coming together to enjoy this timeless game.  
According to a [report](https://www.chess.com/article/view/chesscom-reaches-100-million-members) by the site chess.com, the world's largest site for online chess, the number of active users on the site reached 100 million users, an 238% increase from what it had two and a half years ago.  
Anyone interested in the field notices quite quickly the prominent presence of top players of Russian origin.  
In fact, for almost 60 years, starting from the 1940s, with the raise of  Mikhail Botvinnik, until the beginning of the 2000s at the end of Garry Kasparov's regime, the title of world champion was held only by players of Russian (or Soviet Union) origin, with the exception of a small break in the form of the phenomenal figure of the American Bobby Fisher.  
Since the beginning of the 2000s, the title has migrated to different countries such as Ukraine and Norway, but still at the top you can find many players from the red country.  
Names like Ian Nepominachi, Sergey Kryakin, Danil Dubov and Alexander Grishchuk populate the most prestigious tournaments and produce a Russian-made team that is very hard to match.  
All this without mentioning the fact that also in other countries, such as the United States, you can find many [Russian](https://www.youtube.com/watch?v=kGpA8jr_ZMg)-[speaking](https://www.youtube.com/watch?v=0wqAoopCe7Q) [players](https://www.youtube.com/watch?v=YqJ5u5cOprM).  
All these led to the perception that the world chess capital is Russia.  
Many speculations have been made over the years regarding the reason and Russian education is [often](https://www.chess.com/article/view/the-biggest-secret-of-the-soviet-chess-scool) [mentioned](https://en.wikipedia.org/wiki/Soviet_chess_school) as one of the main factors that make up the great popularity of the game of kings in Russia.  
  
Another country that has made headlines in recent years in the world of chess is India.  
A country that was not considered a prominent source of great chess players over the years, has been producing more and more excellent players in recent years.  
Starting with Anand, the world champion for the year 2007-2012, and up to the younger generation in the form of such as Gukesh, Sarin, Erigaisi and more.  
India is emerging as a rising power in the world of chess and [many](https://www.espn.com/chess/story/_/id/29501703/66-gms-counting-story-india-chess-surge) [articles](https://www.chessbase.in/news/The-rise-of-chess-in-India) have been written in an attempt to characterize the roots of this dramatic rise.  
  
But, I want to be a little annoying and challenge these two perceptions.  
To that end, let's take a look at some data.  
  
Before that, two small clarifications:  
1. The data I use is the full FIDE table of players. The data in this database includes national affiliation only and is not divided into regions within countries. I understand that there is logic in testing at a higher resolution and that certain cities or certain regions of the country can stand out in such an analysis and give a more accurate picture. I don't have this data, so I'll be content, for the sake of exercise and curiosity, with what is available.  
2. Different claims can be made regarding the non-official popularity of chess in different countries (sources) but I have no data or idea how to find such data. That's why I rely again on what is available, which is the list of all the players registered in FIDE. If anyone has other ideas I would love to hear them.  
3. I am using data from a few months ago for the simple reason that since the outbreak of the war in Ukraine, FIDE has imposed a boycott on Russia and for that reason many players are not registered as Russian but as stateless (and play under the FIDE flag).  
  
## the data  
In FIDE registered, as of August 2022, 393377 players.  
The full FIDE player list looks like thi  
![FIDE table](../Figures/fide_table.png)  
  
### Making the data usable  
  
One of the main obsitcles of using this table is that FIDE uses non-conventional country codes and also includes a huge list of federations (did you know that Jersey, an Island between England and France with 100K people on it, has its own federation? Shout out to Lula Robs).  
  
This is a problem because most of population data (which we will be using later) uses more standard list of countries. So we had to merge those provincies (sorry Jersey).  
  
```python  
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
  
def fix_some_countries(name):  
    new_name = name  
    if name in nieche_countries_dict.keys():  
        new_name = nieche_countries_dict[name]  
    return new_name  
  
fide['country name'] = fide['country name'].apply(fix_some_countries)  
```  
  
### Back to the Analysi  
  
The first thing we want to check is how many players there are in each country.  
  
```python  
fide['country name'].value_counts().head(10)  
```  
  
Which yield  
  
| Country        | Players |
| -------------- | ------- |
| Russia         | 38340   |
| India          | 36308   |
| Germany        | 28653   |
| Spain          | 28387   |
| France         | 26840   |
| Iran           | 12315   |
| Poland         | 12243   |
| Italy          | 11970   |
| Turkey         | 9553    |
| Czech Republic | 8658    |
  
Unsurprisingly, Russia is at the top and India in second place.  
For those who are wondering, in the last place is Chad where a single player, named Mahamat Hachim Bachar,  is listed.  
Another index that is interesting to check is how many Grand-Masters are registered in each country. A quick check yields the following table:  
  
| Country                  | GMs  |
| ------------------------ | ---- |
| Russia                   | 208  |
| United States of America | 106  |
| Germany                  | 97   |
| Ukraine                  | 90   |
| India                    | 76   |
| Spain                    | 57   |
| France                   | 54   |
| Serbia                   | 52   |
| Hungary                  | 51   |
| Poland                   | 50   |
  
A final prespective, slightly different but intriguing, is the young players. Let's try to give a glimpse of the next generation of chess by looking at players under a certain age who have already established themselves and crossed a certain ranking threshold. For this purpose, we set the maximum age to 20 and the minimum rating to 2000 and we will get  
  
| Country                  | Prodigies |
| ------------------------ | --------- |
| Russia                   | 272       |
| United States of America | 202       |
| India                    | 150       |
| Spain                    | 147       |
| Germany                  | 138       |
| France                   | 130       |
| Ukraine                  | 77        |
| Poland                   | 75        |
| Hungary                  | 71        |
| Czech Republic           | 70        |
  
No suprisies here - Russia at the top, US right after and the rising start India who just recently passed Spain.  
  
A little side note: I plan to write a separate post about women in  chess, so I'll keep the stats related to this topic for that future  post.  
  
Now, at last, we will present the tables nicely on a map:  
![Raw count maps](../Figures/raw_maps.png)  
As you can see very nicely, Russia is so dominant that it skews the scale. India is also present here, although still behind. It seems that the concepts we mentioned at the beginning are indeed anchored in the data.  
  
But this analysis overshadows a very important issue in data analysis and presentation: the great importance of data normalization.  
  
## on the importance of normalization  
  
Let's take for example the question "Which countries have the highest GDP?"[^1]  
  
| Ranking | Country            | GDP (millions USD) |
| ------- | ------------------ | ------------------ |
| 1       | United States      | 25,462,700         |
| 2       | China              | 17,963,171         |
| 3       | Japan              | 4,231,141          |
| 4       | Germany            | 4,072,192          |
| 5       | India              | 3,385,090          |
| 6       | United Kingdom     | 3,070,668          |
| 7       | France             | 2,782,905          |
| 8       | Russian Federation | 2,240,422          |
| 9       | Canada             | 2,139,840          |
| 10      | Italy              | 2,010,432          |
  
*Source: [World Development Indicators, World Bank, July 2023](https://databankfiles.worldbank.org/public/ddpext_download/GDP.pdf)*  
  
[^1]: The same pattern appears in many other statistics — total number of internet users, road traffic deaths, CO2 emissions — they all tend to look suspiciously like a list of the most populated countries.  
  
Probably no one will be surprised by the list. In fact, a quick glance will reveal that the list is suspiciously reminiscent of the list of "the most populated countries in the world".  
  
| Ranking | Country            | Population (thousands) |
| ------- | ------------------ | ---------------------- |
| 1       | India              | 1,417,173              |
| 2       | China              | 1,412,175              |
| 3       | United States      | 333,288                |
| 4       | Indonesia          | 275,501                |
| 5       | Pakistan           | 235,825                |
| 6       | Nigeria            | 218,541                |
| 7       | Brazil             | 215,313                |
| 8       | Bangladesh         | 171,186                |
| 9       | Russian Federation | 143,556                |
| 10      | Mexico             | 127,504                |
  
*Source: [World Development Indicators, World Bank, July 2023](https://databankfiles.worldbank.org/public/ddpext_download/POP.pdf)*  
  
This phenomenon has appeared in many places, although usually in a less exaggerated and noticeable way.![Heatmap](https://imgs.xkcd.com/comics/heatmap.png)  
  
[xkcd](https://xkcd.com/1138/).  
  
With this rather trivial insight, let's return to the question of "how many people play chess in each country" Would anyone be surprised that there are more chess players in Russia, a country of about two hundred million people, than in (relatively) small Norway? Well that may be obvious, I will be told now, but there are still more players in Russia than, say, China or the USA!  
And it is very true, the correlation here between the number of residents and the number of players in the country is not perfect and not close to it, but it cannot be ignored. As in the comparison between countries, one does not look at the GDP but at the GDP per capita because it is clear that there is almost no meaning in comparing the absolute numbers between countries that differ radically in population size.  
So, if you agree with me that the correct measure is not "the number of chess players" but "the number of chess players in relation to the population" the resulting picture is very different and much more interesting.  
Let's go back to data. Now we will divide all our data by the number of inhabitants of each country (and multiply by 10000 so that our own scale is more convenient) and we will get the following table:  
![Players per capita with Iceland](../Figures/players_per_capita_with_iceland.png)  
Well, I'm sorry Iceland, but you are completely distorting the scale, so we will exclude you from the discussion (and any other country smaller than Iceland).  
  
| Country        | Players per 1000 |
| -------------- | ---------------- |
| Croatia        | 88.857991        |
| Czech Republic | 79.576901        |
| Denmark        | 77.224312        |
| Slovakia       | 76.828786        |
| Slovenia       | 75.070956        |
| Montenegro     | 75.005972        |
| Hungary        | 69.569226        |
| Norway         | 68.766931        |
| Serbia         | 65.283596        |
| Spain          | 59.827725        |

As you can see the picture here is completely different. Suddenly the big countries disappeared and other countries emerged in their place, mainly Eastern European countries but not only. Shout out to Croatian Agadmator for being the most famous representative of Croatian chess (interested? [Here is an article about chess in Croatia](https://en.chessbase.com/post/che-in-croatia)). Apart from Croatia, the list also stars Spain, known for their strong team (some 2-3 names), Hungary, home of Judit Polgar and Richard Rapport, and of course - Norway, whose leading chess player needs no introduction [![Magnus](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/World_Chess_Championship_2021%2C_game_07%2C_Magnus_Carlsen_%28cropped%29.jpg/220px-World_Chess_Championship_2021%2C_game_07%2C_Magnus_Carlsen_%28cropped%29.jpg)](https://commons.wikimedia.org/wiki/File:World_Chess_Championship_2021,_game_07,_Magnus_Carlsen_(cropped).jpg).  
Let's zoom out. Here is an illustration of what is happening all over the world  
![Players per capita map](../Figures/players_per_capita_map.png)  
You are welcome to scroll up a second and compare to the corresponding map before normalization. As you can see Russia has deteriorated badly not to mention the USA which is placed below almost every European country and even some countries from South America and Asia. In India the story is similar, but we will return to it later. In China, if you were wondering, the most popular competative board game is Go, so the result there is not very surprising.  
Let's quickly make the same correction to our other metrics as well:  
| Country    | GMs per $10^5$ |
| ---------- | -------------- |
| Armenia    | 1.278615       |
| Montenegro | 1.273987       |
| Georgia    | 0.755908       |
| Croatia    | 0.739046       |
| Serbia     | 0.600947       |
| Hungary    | 0.541314       |
| Latvia     | 0.540881       |
| Slovenia   | 0.529346       |
| Israel     | 0.526735       |
| Bulgaria   | 0.511352       |
  
| Country    | Titled Players per $10^5$ |
| ---------- | ------------------------- |
| Montenegro | 10.191894                 |
| Serbia     | 7.003338                  |
| Slovenia   | 6.640892                  |
| Croatia    | 6.552877                  |
| Hungary    | 5.142481                  |
| Armenia    | 4.609743                  |
| Estonia    | 4.084998                  |
| Latvia     | 3.732076                  |
| Suriname   | 3.518584                  |
| Georgia    | 3.451979                  |
  
| Country        | Prodigies per $10^5$ |
| -------------- | -------------------- |
| Slovenia       | 1.203060             |
| Montenegro     | 1.114738             |
| Armenia        | 0.975785             |
| Estonia        | 0.907777             |
| Hungary        | 0.884840             |
| Slovakia       | 0.879090             |
| Czech Republic | 0.838240             |
| Mongolia       | 0.740066             |
| Norway         | 0.707628             |
| Israel         | 0.661221             |

Some key points:  
For a reason that is not clear to me, the number of GMs in Montenegro and Serbia is unusual. Although there is not a single GM in these two countries who is ranked above 2700, the top player is Alexandr Predke and he is currently ranked 49th in the world. Nevertheless, Serbia is a country of less than 7 million people and has over 50 GMs! ([Here](https://www.quora.com/Why-how-does-Serbia-produce-so-many-chess-grandmasters) is a discussion in the case of possible causes of the phenomenon)  
If in the general ranking of players Russia has fallen a little lower, in the ranking of GMs its situation is even worse.  
To summarize the discussion, I decided to combine two parameters into one plot to also examine the popularity (in the form of the overall number of players) at the same time as the degree of "success" (to be measured for that matter by the number of GMs):  
![GMs vs Players scatter](../Figures/gms_vs_players_scatter.png)  
  
### Final note - India  
  
Chess in India is growing drastically, it's no secret ([1](https://www.espn.com/chess/story/_/id/29501703/66-gms-counting-story-india-chess-surge), [2](https://www.chessbase.in/news/The-rise-of-chess-in-India)). In the light of our presentation we must mention that the Indian case demonstras a dark side of the normalization - it disables more subtle insights about really large groups. India is huge, the number of Indian citizens is equal to that of the USA, Russia, Brazil, Japan and Great Britain combined! The problem is that this is a country on a different scale of size. Some would argue that a more correct comparison would be to divide India (and perhaps China as well) into provinces in this analysis. Unfortunately, I do not have such information, so will have to content only with the great chess that the young (and also the old) from India are giving us.  
