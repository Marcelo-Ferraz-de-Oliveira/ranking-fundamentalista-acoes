# -*- coding: utf-8 -*-



import cloudscraper
import pandas as pd


def get_stocks_list():
  """
  Get all Brazilian stock list, with their fundamentalist parameters, from www.fundamentos.com.br.
  Return a pandas dataframe with stocks filtered and sorted based on parameters
  """

  range_plpvpa = (0,22.5)
  range_pl = (0,20)
  range_crescimento = (0,1000000)
  range_pebit = (0,1000000)
  sort_by = 'P/VP'
  url = 'https://www.fundamentus.com.br/resultado.php'
  #Scraper para a cloudflare
  scraper = cloudscraper.create_scraper()
  html = scraper.get(url).content


  #A list of dataframes. Each dataframe correspond to a table-like structure found in the html page
  df_list = pd.read_html(html,decimal=",",thousands='.')

  #Get the only dataframe generated
  df = df_list[0]

  #Transform numeric strings data in float and remove "%" symbol
  listaPc = list(df.dtypes[df.dtypes == 'object'].index)
  for item in listaPc:
    if item == "Papel": continue
    df[item] = df[item].str.replace("%","", regex=False).str.replace(".","", regex=False).str.replace(",",".", regex=False).astype('float64')


  dfValido = df[df["Liq.2meses"] != 0]

  dfGraham = dfValido.assign(PLPVPA=dfValido['P/L']*dfValido['P/VP'])
  
  dfGraham = dfGraham[dfGraham['PLPVPA'] > range_plpvpa[0]]
  dfGraham = dfGraham[dfGraham['PLPVPA'] <= range_plpvpa[1]]
  dfGraham = dfGraham[dfGraham['P/L'] > range_pl[0] ]
  dfGraham = dfGraham[dfGraham['P/L'] <= range_pl[1]]
  dfGraham = dfGraham[dfGraham['Cresc. Rec.5a'] > range_crescimento[0]]
  dfGraham = dfGraham[dfGraham['Cresc. Rec.5a'] <= range_crescimento[1]]
  dfGraham = dfGraham[dfGraham['P/EBIT'] > range_pebit[0]]
  dfGraham = dfGraham[dfGraham['P/EBIT'] <= range_pebit[1]]
  dfGraham = dfGraham.set_index('Papel')

  resultado = dfGraham.sort_values(by=[sort_by]).head(10).sort_values(by=[sort_by])
  return resultado


if __name__ == "__main__":
    print(get_stocks_list())