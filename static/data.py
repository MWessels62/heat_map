import urllib.request, urllib.parse, urllib.error
import requests
import pandas as pd 
import dask.dataframe as dd

from bs4 import BeautifulSoup
def getData(x):
    page = requests.get("https://www.worldometers.info/coronavirus")
    #html = urllib.request.urlopen('https://www.worldometers.info/coronavirus').read()

    soup = BeautifulSoup(page.content,'html.parser')

    table_data = soup.find('table', attrs = {'id':'main_table_countries_today'})

    rows = table_data.find_all("tr", attrs = {"style": ""})

    data = []
    datadict = {}

    for i,item in enumerate(rows):

        if i == 0:
            data.append(item.text.strip().split("\n")[:13])

        else:
            data.append(item.text.strip().split("\n")[:12])

    for i in range(2, len(data)-1):
        datadict[data[i][1]] = i-1

    #print(datadict)
    dt = pd.DataFrame(data)
    dt = pd.DataFrame(data[1:], columns=data[0][:12])
    df = dd.from_pandas(dt,npartitions = 1)

    test = (dt.loc[datadict[x]])
    output = df.to_csv("C:/Users/lucyr/Downloads/HeatMap/data-*.csv")