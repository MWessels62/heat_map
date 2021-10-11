import urllib.request, urllib.parse, urllib.error
import requests
import pandas as pd 
import dask.dataframe as dd

from bs4 import BeautifulSoup
#create data module, i might make this into a class though, and make use of inheritance to call functions within this
#this function takes in a country name and then will output the data associated with it
def getData(x):
    #create a get request for the page im scraping
    page = requests.get("https://www.worldometers.info/coronavirus")
    #use beautifulsoup to parse through the content
    soup = BeautifulSoup(page.content,'html.parser')
    #finding the code within the website for the table and the data therein 
    table_data = soup.find('table', attrs = {'id':'main_table_countries_today'})
    #this is a continuation to find the data within thpe rows
    rows = table_data.find_all("tr", attrs = {"style": ""})
    #create an empty list to store the data
    data = []
    datadict = {}
    #enumerate the rows 
    for i,item in enumerate(rows):
        if i == 0:
            data.append(item.text.strip().split("\n")[:13])

        else:
            data.append(item.text.strip().split("\n")[:12])
    #assign key value pairs to a dictionary in order to search the data for specifics about a country
    for i in range(2, len(data)-1):
        datadict[data[i][1]] = i-1

    #use pandas to create a dataframe
    dt = pd.DataFrame(data)
    dt = pd.DataFrame(data[1:], columns=data[0][:12])
    df = dd.from_pandas(dt,npartitions = 1)


    test = (dt.loc[datadict[x]])
    print(test)

 #output = df.to_csv("C:/Users/lucyr/Downloads/HeatMap/data-*.csv")