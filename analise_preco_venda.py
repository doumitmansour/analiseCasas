# -*- coding: utf-8 -*-

<b>Base de dados: Casas à Venda - Ponta Grossa PR</b>

Usa arquivo casas_amostra

Objetivo:
Fazer a análise estatísticas dos dados de casas à venda em Ponta Grossa PR
<ul>
<li>média minima e maxima, dos bairros</li>
<li>amostra aleatória com dados completos para os dados</li>
<li>mínimo máximo e média de vendas em cada bairro</li>
</ul>

#Base de dados
Para o trabalho usamos a base de dados sobre venda de casas em Ponta Grossa - PR<br>
https://www.kaggle.com/datasets/victorstein/casas-venda-ponta-grossa-pr
"""

import pandas as pd
import re
import matplotlib.pyplot as plt #para criar os graficos
from matplotlib.ticker import FuncFormatter
import numpy as np

# disable chained assignments
pd.options.mode.chained_assignment = None

def fomartar_moeda_grafico():
        return plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "R${:,.2f}".format(x)))

# Configurar a formatação de números de ponto flutuante
pd.options.display.float_format = 'R${:,.2f}'.format

df1 = pd.read_excel('Trabalho2.xlsx')
df = df1.copy()

df['valor_venda'] = df['valor_venda'].apply(lambda x: float(x))

# retirar outliers

# Calcular o IQR (intervalo interquartil) para 'area_total'
Q1 = df['area_total'].quantile(0.25)
Q3 = df['area_total'].quantile(0.75)
IQR = Q3 - Q1

# Definir um limite para identificar outliers
limite_superior = Q3 + 1.5 * IQR
limite_inferior = Q1 - 1.5 * IQR

# DataFrame "outliers" com os valores discrepantes
outliers = df[(df['area_total'] < limite_inferior) | (df['area_total'] > limite_superior)]

print("Valores Discrepantes (Outliers):")
print(outliers)

# Remover os outliers do DataFrame principal
df = df[~((df['area_total'] < limite_inferior) | (df['area_total'] > limite_superior))]

#tabelas

print("\nQuantidade de Apto por Bairro\n")
quantidade_vendas_por_bairro = df['bairro'].value_counts().reset_index()
quantidade_vendas_por_bairro.columns = ['Bairro', 'Quantidade de Vendas']
print(quantidade_vendas_por_bairro)

print("\nValor Minimo de Venda por Bairro\n")
venda_minima_por_bairro = df.groupby('bairro')['valor_venda'].min().reset_index()
venda_minima_por_bairro.columns = ['Bairro', 'Valor Mínima']
print(venda_minima_por_bairro)

print("\nValor Medio de Venda por Bairro\n")
media_valor_apartamento_por_bairro = df.groupby('bairro')['valor_venda'].mean().reset_index()
media_valor_apartamento_por_bairro.columns = ['Bairro', 'Média de Valor de Apartamento']
print(media_valor_apartamento_por_bairro)

print("\nValor Maximo de Venda por Bairro\n")
venda_maxima_por_bairro = df.groupby('bairro')['valor_venda'].max().reset_index()
venda_maxima_por_bairro.columns = ['Bairro', 'Valor Máximo']
print(venda_maxima_por_bairro)

print("\nValor Total de Venda por Bairro\n")
valor_total_vendido_por_bairro = df.groupby('bairro')['valor_venda'].sum().reset_index()
valor_total_vendido_por_bairro.columns = ['Bairro', 'Valor Total Ofertado']
print(valor_total_vendido_por_bairro)

#graficos

# histograma de faixas

faixas_de_preco = [0,500000, 1000000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000]

plt.hist(df['valor_venda'], bins=faixas_de_preco, edgecolor='k')

plt.xlabel('Faixa de Preço')
plt.ylabel('Quantidade de Imóveis')
plt.title('Distribuição de Imóveis por Faixa de Preço')

for i, bin_count in enumerate(np.histogram(df['valor_venda'], bins=faixas_de_preco)[0]):
    plt.text(faixas_de_preco[i], bin_count, str(bin_count), ha='left', va='bottom')

plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: "R${:,.2f}".format(x)))
plt.xticks(rotation=90)
plt.show()

# Gráfico de barras para a quantidade de vendas por bairro:

quantidade_vendas_por_bairro = quantidade_vendas_por_bairro.sort_values(by='Quantidade de Vendas', ascending=True)

plt.figure(figsize=(12, 6))
plt.bar(quantidade_vendas_por_bairro['Bairro'], quantidade_vendas_por_bairro['Quantidade de Vendas'])
plt.xlabel('Bairro')
plt.ylabel('Quantidade de Vendas')
plt.title('Quantidade de Apto a Venda por Bairro')
plt.xticks(rotation=90)
plt.show()

# Gráfico de barras para a média de valor de apartamento por bairro:

media_valor_apartamento_por_bairro = media_valor_apartamento_por_bairro.sort_values(by='Média de Valor de Apartamento', ascending=True)

plt.figure(figsize=(12, 6))
plt.bar(media_valor_apartamento_por_bairro['Bairro'], media_valor_apartamento_por_bairro['Média de Valor de Apartamento'])
plt.xlabel('Bairro')
plt.ylabel('Média de Valor de Apartamento')
plt.title('Média de Valor de Apartamento por Bairro')
plt.xticks(rotation=90)
fomartar_moeda_grafico()
plt.show()


# Gráfico de barras para o valor mínimo de venda por bairro:

venda_minima_por_bairro = venda_minima_por_bairro.sort_values(by='Valor Mínima', ascending=True)

plt.figure(figsize=(12, 6))
plt.bar(venda_minima_por_bairro['Bairro'], venda_minima_por_bairro['Valor Mínima'])
plt.xlabel('Bairro')
plt.ylabel('Valor Mínimo de Venda')
plt.title('Valor Mínimo de Venda por Bairro')
plt.xticks(rotation=90)
fomartar_moeda_grafico()
plt.show()

# Gráfico de barras para o valor máximo de venda por bairro:

venda_maxima_por_bairro = venda_maxima_por_bairro.sort_values(by='Valor Máximo', ascending=True)

plt.figure(figsize=(12, 6))
plt.bar(venda_maxima_por_bairro['Bairro'], venda_maxima_por_bairro['Valor Máximo'])
plt.xlabel('Bairro')
plt.ylabel('Valor Máximo de Venda')
plt.title('Valor Máximo de Venda por Bairro')
plt.xticks(rotation=90)
fomartar_moeda_grafico()
plt.show()

# Gráfico de barras para o valor total vendido por bairro:

valor_total_vendido_por_bairro = valor_total_vendido_por_bairro.sort_values(by='Valor Total Ofertado', ascending=True)

plt.figure(figsize=(12, 6))
plt.bar(valor_total_vendido_por_bairro['Bairro'], valor_total_vendido_por_bairro['Valor Total Ofertado'])
plt.xlabel('Bairro')
plt.ylabel('Valor Total Ofertado')
plt.title('Valor Total Ofertado por Bairro')
plt.xticks(rotation=90)
fomartar_moeda_grafico()
plt.show()

#compilado - analises especifica

# Defina os pesos para cada característica (quanto maior o peso, mais importante a característica)
peso_quartos = 10
peso_suites = 15
peso_banheiros = 10
peso_vagas_garagem = 7
peso_area_total = 1

# dataFrame vazio para armazenar as melhores opções por bairro
melhores_opcoes_por_bairro = pd.DataFrame(columns=df.columns)

# bairros únicos no DataFrame
frames=[]#****

bairros_unicos = df['bairro'].unique()
for bairro in bairros_unicos:
    # Filtrar o DataFrame para o bairro atual
    df_bairro = df[df['bairro'] == bairro]

    # Calcule a pontuação ponderada para cada apartamento no bairro atual
    df_bairro['pontuacao'] = (
        peso_quartos * df_bairro['quartos'] +
        peso_suites * df_bairro['suites'] +
        peso_banheiros * df_bairro['banheiros'] +
        peso_vagas_garagem * df_bairro['vagas_garagem'] +
        peso_area_total * df_bairro['area_total']
    )

    # Calcule o custo-benefício (razão entre a pontuação e o preço)
    df_bairro['custo_beneficio'] = df_bairro['pontuacao'] / df_bairro['valor_venda']

    # Encontre a melhor opção de custo-benefício no bairro atual
    melhor_custo_beneficio_bairro = df_bairro.loc[df_bairro['custo_beneficio'].idxmax()]

    frames.append(melhor_custo_beneficio_bairro)#****

# Adicione a melhor opção de custo-benefício do bairro ao DataFrame de melhores opções por bairro
melhores_opcoes_por_bairro=pd.DataFrame.from_records(frames)#****

# Exiba as melhores opções de custo-benefício por bairro
print("\nMelhores Opções de Custo-Benefício por Bairro:\n")
print(melhores_opcoes_por_bairro[['bairro', 'quartos', 'suites', 'banheiros', 'vagas_garagem', 'area_total', 'valor_venda', 'custo_beneficio']])
