# -*- coding: utf-8 -*-
"""Fundamentus fundamentalist analysis

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15n1xBlBJtRT39UwdVU2IaOlgeuykqumb

#1 Introdução
Fazer o scraping do Fundamentus para obter e analisar as informações fundamentalistas das empresas.

##1.1 Imports
"""

#!pip install cloudscraper
#!pip install pandas_profiling
#!pip install lxml
from json.tool import main
from multiprocessing.spawn import _main
from socket import if_indextoname
from threading import main_thread
import cloudscraper
import pandas as pd
import pandas_profiling

"""##1.2 Endereços
Endereço do fundamentus para pegar os principais indicadores de todas as empresas na bolsa.
"""
def obter_lista_acoes():
  range_plpvpa = (0,22.5)
  range_pl = (0,20)
  range_crescimento = (0,1000000)
  range_pebit = (0,1000000)
  sort_by = 'P/VP'
  url = 'https://www.fundamentus.com.br/resultado.php'
  #Scraper para a cloudflare
  scraper = cloudscraper.create_scraper()
  html = scraper.get(url).content

  """#2 Análise

  ##2.1 Obtenção dos dados
  """

  df = pd.read_html(html,decimal=",",thousands='.')

  #o pandas retorna uma lista de dataframes - cada tabela da página gera um dataframe diferente
  #temos então que ver todos os dataframes gerados
  # for d in df:
  #   print(d.head(10))
  #   print(d.dtypes)

  #como só foi criado um dataframe, ele será o padrão
  df = df[0]

  """##2.2 Tratamento dos dados"""

  #transforma as colunas que ainda são string em float, retirando os percentuais
  listaPc = list(df.dtypes[df.dtypes == 'object'].index)
  for item in listaPc:
    if item == "Papel": continue
    df[item] = df[item].str.replace("%","", regex=False).str.replace(".","", regex=False).str.replace(",",".", regex=False).astype('float64')

  #roda estatística completa sobre os dados obtidos
  #pandas_profiling.ProfileReport(df)

  #dropa o Liq.2meses = 0 - são as ações que não são mais negociadas
  dfValido = df[df["Liq.2meses"] != 0]
  """##2.3 Análise Fundamentalista"""
  #calcula o P/L*P/VPA
  #dfValido['PLPVPA']= pd.Series()

  dfValido = dfValido.assign(PLPVPA=dfValido['P/L']*dfValido['P/VP'])
  #filtra de acordo com os filtros fundamentalistas
  dfGraham = dfValido[dfValido['PLPVPA'] > range_plpvpa[0]]
  dfGraham = dfGraham[dfGraham['PLPVPA'] <= range_plpvpa[1]]
  dfGraham = dfGraham[dfGraham['P/L'] > range_pl[0] ]
  dfGraham = dfGraham[dfGraham['P/L'] <= range_pl[1]]
  dfGraham = dfGraham[dfGraham['Cresc. Rec.5a'] > range_crescimento[0]]
  dfGraham = dfGraham[dfGraham['Cresc. Rec.5a'] <= range_crescimento[1]]
  dfGraham = dfGraham[dfGraham['P/EBIT'] > range_pebit[0]]
  dfGraham = dfGraham[dfGraham['P/EBIT'] <= range_pebit[1]]
  dfGraham = dfGraham.set_index('Papel')

  """#3 - Resultado"""
  #pega os 30 menores valores de p/ebit e ordena pelo p/l
  resultado = dfGraham.sort_values(by=[sort_by]).head(10).sort_values(by=[sort_by])
  #destaca a coluna do P/L e mostra o resultado
  return resultado#.style.applymap(lambda x: 'background-color: yellow', subset=pd.IndexSlice[:,['P/L']])

#comparar o P/L da companhia estudada com a média de seu setor e, se possível, com a média do mercad

if __name__ == "__main__":
    print(obter_lista_acoes())