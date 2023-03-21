import os
# Define a relative path (current code)
RELATIVE_PATH = os.path.dirname(os.path.abspath(__file__))
DATASETS_PATH = os.path.abspath(os.path.join(RELATIVE_PATH, '../../Datasets'))

# Utilizando a plotagem com pandas, reproduzam as visualizações abaixo, tentando deixá-las o mais próximas quanto possível da maneira 
# como estão postas. Para isso, atentem-se às personalizações dos gráficos, como títulos, legendas, eixos e outros tipos possíveis de 
# formatações e preferências de visualizações dos dados. Também é interessante que vocês discutam possíveis pontos de melhorias dessas 
# visualizações!

#-----------------------------------------------------------------------------------------------------------------------------------#
# 1. Reproduza o gráfico de barras abaixo, em que cada barra representa um dos 10 países com mais casos confirmados de 
#    COVID no dataset, e a "quebra" em cada cor indica a predominância de casos confirmados em cada mês.

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(DATASETS_PATH + '/Covid_19_Countrywise_timeseries.csv')

df['date'] = pd.to_datetime(df['ObservationDate']).astype('string').str.slice(0,7)

pivot = pd.pivot_table(df, values='New Recovered', index='country', columns='date', aggfunc='sum').fillna(0)
pivot = pivot.sort_values('2020-03', ascending=False)[:10]
pivot.plot(kind='barh', stacked=True)

#plt.show()
plt.savefig(RELATIVE_PATH + '/figure 1.png')

#-----------------------------------------------------------------------------------------------------------------------------------#
# 2. Reproduza o gráfico de linhas abaixo, que representa a série temporal da evolução de emissões de CO2 no Brasil.

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(DATASETS_PATH + '/co2_emissions_kt_by_country.csv')

df = df[df['country_name'] == 'Brazil']

df.plot(kind='line', x='year', y='value', legend=False, xlabel='Ano', title='Histórico de emissões de CO2 no Brasil')

#plt.show()
plt.savefig(RELATIVE_PATH + '/figure 2.png')

#-----------------------------------------------------------------------------------------------------------------------------------#
# 3. Uma visualização muito similar à anterior, mas com a adição da média global de emissão de CO2 (o Brasil deve ser incluído na 
#    linha da média global?).

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(DATASETS_PATH + '/co2_emissions_kt_by_country.csv')

df_brazil = df[df['country_name'] == 'Brazil']

fig = plt.figure(figsize=(12,6))

ax = df.groupby('year')['value'].mean().plot(kind='line', x='year', y='value')
df_brazil.plot(kind='line', x='year', y='value', ax=ax, xlabel='Ano', title='Histórico de emissões de CO2')

plt.legend(['Média global', 'Brasil'])
#plt.show()
fig.savefig(RELATIVE_PATH + '/figure 3.png')

#-----------------------------------------------------------------------------------------------------------------------------------#
# 4. Os 10 países que mais aumentaram, percentualmente, a emissão de CO2 entre os anos de 2018 e 2019, na forma de um gráfico de 
#    barras horizontal.

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(DATASETS_PATH + '/co2_emissions_kt_by_country.csv')

df_2018 = df[df['year'] == 2018]
df_2019 = df[df['year'] == 2019]

pct_list = []

for country in df_2018['country_name'].unique():
    value_2018 = df_2018.loc[df_2018['country_name'] == country, 'value'].iloc[0]
    value_2019 = df_2019.loc[df_2019['country_name'] == country, 'value'].iloc[0]
    
    pct = (value_2019 - value_2018) / value_2018 * 100

    pct_list.append({'country_name': country, 'pct_ascending': pct})

df_ascending = pd.DataFrame(pct_list)

df_ascending = df_ascending.sort_values('pct_ascending', ascending=True)[-10:]

X = list(df_ascending['pct_ascending'])
Y = list(df_ascending['country_name'])

fig = plt.figure(figsize=(12,6))

bars = plt.barh(y=Y, width=X, height=0.5, align='center')

ax = fig.get_axes()
ax[0].bar_label(bars, fmt='%.1f%%')

plt.title('Top 10 países com maiores aumentos percentuais de emissão entre 2018 e 2019')
plt.xticks([])
#plt.show()
fig.savefig(RELATIVE_PATH + '/figure 4.png')