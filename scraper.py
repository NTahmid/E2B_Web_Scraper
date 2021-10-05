import requests
from bs4 import BeautifulSoup
import pandas as pd
import string

#url = "https://www.nepia.com/industry-news/coronavirus-outbreak-impact-on-shipping/"


def getMeanings(url):
    # url = "https://www.english-bangla.com/dictionary/a%20rise"
    r = requests.get(url)

    soup = BeautifulSoup(r.content,'html5lib')

    table = soup.find('div',attrs={"class":"word_info"})
    # print(table)
    meaning=None
    for row in table.findAll("span",attrs={"class":"format1","style":"font-family:TonnyBanglaMJ, SolaimanLipi,  Times, serif"}):
        # print(row.text)
        meaning=row.text.strip();
        return meaning
    # print(meanings)

def getLastPage(soup):
    table=soup.find('div',attrs={"class":"pagination","style":"clear:both"})

    elements = table.findAll('a');

    if len(elements) == 0:
        lastPage=1
    elif len(elements) == 1:
        lastPage=2
    else:
        lastPage=elements[1]['data-ci-pagination-page'];
    return int(lastPage)

def zehaha():
    letters = string.ascii_lowercase[15:26]
    print(letters)
#     print(letters)
#     baseUrl = "https://www.english-bangla.com/browse/index/" + "e"
#     r=requests.get(baseUrl)
#     soup=BeautifulSoup(r.content,'html5lib')
#     getLastPage(soup)

def main():

    # url = "https://www.geeksforgeeks.org/data-structures/"

    letters = string.ascii_lowercase[15:26]

    for letter in letters:
        # print(letter)
        baseUrl = "https://www.english-bangla.com/browse/index/"+letter

        initR= requests.get(baseUrl)
        initSoup = BeautifulSoup(initR.content,'html5lib')

        firstPage = 1
        lastPage = getLastPage(initSoup)

        # print(lastPage)

        for page in range(firstPage,lastPage+1):
            pageUrl=baseUrl+"/"+str(page)
            df=pd.DataFrame(columns=["Word","Meanings","Url"])
            r= requests.get(pageUrl)
            soup = BeautifulSoup(r.content,'html5lib')

            table = soup.find('ul',attrs={"style":"width:82%;list-style-type:none; padding:2px 20px; line-height:28px"})

            word=[]
            url=[]
            meaning=[]
            # dictionary = []

            count=0

            for row in table.findAll('li',attrs = {"style":"width:32%; float:left;"}):
                # print(row.a.text)
                word.append(row.a.text)
                url.append(row.a['href'])
                meaning.append(getMeanings(row.a['href']))

            df['Word']=word
            df["Meanings"]=meaning
            df["Url"]=url;
            fileName=letter+str(page)+".csv"
            df.to_csv(fileName, encoding='utf-8',index=False)
            # print(df)

main()