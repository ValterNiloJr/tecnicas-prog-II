import os
# Define a relative path (current code)
RELATIVE_PATH = os.path.dirname(os.path.abspath(__file__))
DATASETS_PATH = os.path.abspath(os.path.join(RELATIVE_PATH, '../../Datasets'))

# Gerando algumas visualizações descritivas com matplotlib
# Vamos utilizar um dataset dos preços dos combustíveis no Brasil.

# Reproduza as visualizações abaixo. Para cada uma, pense em pontos que você poderia modificar na visualização, pensando em aprimorá-la.

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(DATASETS_PATH + '/gas_prices_brazil.tsv', sep = '\t')

#-----------------------------------------------------------------------------------------------------------------------------------#
# 1. Preços médios do etanol e da gasolina, por região do Brasil

#print(df.head())
#print(df.info())
df['date'] = pd.to_datetime(df['DATA FINAL'])
#print(df['date'].dt.isocalendar())

df2 = df[['PREÇO MÉDIO REVENDA', 'DATA FINAL', 'REGIÃO', 'PRODUTO']][df['PRODUTO'].isin(['ETANOL HIDRATADO', 'GASOLINA COMUM'])]

df_ethanol = df2[df2['PRODUTO'] == 'ETANOL HIDRATADO']
df_gasoline = df2[df2['PRODUTO'] == 'GASOLINA COMUM']

df_ethanol_grouped = df_ethanol.groupby(["DATA FINAL", "REGIÃO"])['PREÇO MÉDIO REVENDA'].mean().unstack()

df_ethanol_grouped.boxplot()

plt.savefig(RELATIVE_PATH + '/figure 1.0.png')

datas = df_ethanol_grouped.index.to_list() # eixo-x do gráfico


fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (18,8))

products = ['ETANOL HIDRATADO', 'GASOLINA COMUM']

subplot_index = 1

for product in products:
    plt.subplot(1, 2, subplot_index)
    
    df_filtered = df2[df2['PRODUTO'] == product]
    
    df_grouped = df_filtered.groupby(["DATA FINAL", "REGIÃO"])['PREÇO MÉDIO REVENDA'].mean().unstack()
    
    plt.plot(df_grouped)
    
    # Legenda
    plt.legend(df_grouped.columns.to_list())
    plt.ylabel("Preço médio de revenda (R$)")
    plt.xticks(datas[::80], rotation=45)
    plt.title(product)
    
    
    subplot_index += 1
    
plt.suptitle("Preço médio de revenda por região")

plt.savefig(RELATIVE_PATH + '/figure 1.1.png')

#-----------------------------------------------------------------------------------------------------------------------------------#
# 2. Preço médio em 2020 dos preços do Etanol e da Gasolina por região

grouped_df = df[(df['DATA FINAL'] < '2021-01-01') & (df['DATA FINAL'] > '2019-12-31') & \
                (df['PRODUTO'].isin(['ETANOL HIDRATADO', 'GASOLINA COMUM']))]\
                .groupby(["REGIÃO", "PRODUTO"])['PREÇO MÉDIO REVENDA'].mean().unstack()

import numpy as np
regioes = grouped_df.index.to_list()
etanol = grouped_df['ETANOL HIDRATADO']
gasolina = grouped_df['GASOLINA COMUM']

x = np.arange(len(regioes)) # localização dos labels para o eixo-x
width = 0.35

fig, ax = plt.subplots(1,1, figsize = (10,6))
rects1 = ax.bar(x - width/2, etanol, width, label = 'Etanol')
rects2 = ax.bar(x + width/2, gasolina, width, label = 'Gasolina')

# Adicionado informações aos eixos
ax.set_ylabel('Preço médio de revenda (R$/L)')
ax.set_title('Comparativo de preços - etanol e gasolina')
ax.set_xticks(x, regioes)
ax.legend()

# Adicionando os labels às barras
ax.bar_label(rects1, padding = 3, fmt = '%.2f')
ax.bar_label(rects2, padding = 3, fmt = '%.2f')

plt.savefig(RELATIVE_PATH + '/figure 2.png')


#-----------------------------------------------------------------------------------------------------------------------------------#
# 3. Total consolidado de postos para cada estado

grouped_df = df.groupby(["ESTADO"])['NÚMERO DE POSTOS PESQUISADOS'].sum().sort_values(ascending = True)

grouped_df = df.groupby(["ESTADO"])['NÚMERO DE POSTOS PESQUISADOS'].sum().sort_values(ascending = True)

estados = grouped_df.index
postos = grouped_df.values

fix, ax = plt.subplots(figsize = (15,8))
ax.barh(estados, postos)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.xaxis.set_visible(False)

for y, x in enumerate(postos):
    ax.text(x, y - 0.05, f"{x:.0f}", fontweight = 'bold')

plt.savefig(RELATIVE_PATH + '/figure 3.png')

#-----------------------------------------------------------------------------------------------------------------------------------#
# 4. Relação entre preço da gasolina e do etanol (nível Brasil)

from scipy.stats import linregress

etanol = df[df['PRODUTO'] == 'ETANOL HIDRATADO'][['DATA FINAL', 'ESTADO', 'PREÇO MÉDIO REVENDA']]
gasolina = df[df["PRODUTO"] == 'GASOLINA COMUM'][['DATA FINAL', 'ESTADO', 'PREÇO MÉDIO REVENDA']]

gasolina = gasolina.merge(etanol, how = 'inner', on = ['DATA FINAL', 'ESTADO'])

plt.figure(figsize = (9,7))

x = gasolina['PREÇO MÉDIO REVENDA_y']
y = gasolina['PREÇO MÉDIO REVENDA_x']

plt.scatter(x = x, y = y, s = 1)

# Linha de tendência
fit = linregress(x,y)

# valores quaisquer de x, dentro do intervalo do nosso plot
x_2 = np.linspace(0,7,100)
y_2 = fit[0]*x_2 + fit[1]
plt.plot(x_2, y_2, '--r')

plt.legend(['(Etanol, Gasolina)', 'Linha de tendência'])

plt.xlabel('Preço médio de revenda (etanol)')
plt.ylabel('Preço médio de revenda (gasolina)')

plt.savefig(RELATIVE_PATH + '/figure 4.png')

#plt.show()