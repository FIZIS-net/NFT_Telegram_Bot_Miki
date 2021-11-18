import requests
import config
import pandas as pd
from bs4 import BeautifulSoup
    
def dropParser(url, filePath):
    #Array of data about drops
    drops = {'Date':[],'ImgSrc':[], 'Title':[], 'Price':[], 'Items':[], 'DisFol':[], 'DisLink':[], 'TwitFol':[], 'TwitLink':[]}

    response = requests.get(url, headers = config.HEADERS, stream=True)
    soup = BeautifulSoup(response.text, 'lxml')
    tr = soup.find_all('tr')

    for i in range(1, len(tr)-1):
        td      = tr[i].find_all('td')
        drops['Date'].append(td[0].span.text)
        if td[1].a.img['src'] != '/static/images/default.png':
            drops['ImgSrc'].append(td[1].a.img['src'])
        else:
            drops['ImgSrc'].append(td[1].a.img.get('data-src'))
        drops['Title'].append(td[2].text)
        drops['Items'].append(td[3].text)
        drops['Price'].append(td[4].text)

        if td[6].find('span', {'class':"is-size-6"}) != None:
            drops['DisFol'].append(td[6].find('span', {'class':"is-size-6"}).text)
        else:
            drops['DisFol'].append(None)
        
        if td[6].find('a')!= None:
            drops['DisLink'].append(td[6].find('a')['href'])
        else:
            drops['DisLink'].append(None)

        if td[7].find('span', {'class':"is-size-6"}) != None:
            drops['TwitFol'].append(td[7].find('span', {'class':"is-size-6"}).text)
        else:
            drops['TwitFol'].append(None)
            
        if td[7].find('a') != None:
            drops['TwitLink'].append(td[7].find('a')['href'])
        else:
            drops['TwitLink'].append(None)
        
    dropData = pd.DataFrame(drops)
    dropData.to_csv(filePath ,sep='\t', encoding='utf-8')

dropParser(config.ETHDROPURL, 'data/ethDropData.csv')
dropParser(config.SOLDROPURL, 'data/solDropData.csv')