import requests
from lxml import html
from pathlib import Path
import os

def getItemsList(url):
    staticItemsFile = url
    itemsList = Path(staticItemsFile)

    if not itemsList.is_file():
        #Saves the list as a file
        createItemsList(staticItemsFile)
        print('List created...')

    staticItems = open(staticItemsFile, 'r')
    return staticItems.read().split(',')


def handleCacheFiles(cleanTitle, urlResource):
    # Test if cache files exists
    cacheFile = Path("cache/"+cleanTitle+"/"+cleanTitle+".html")
    pathDir = "cache/"+cleanTitle

    # Create the directory
    createDir(pathDir)

    if not cacheFile.is_file():
        # Creates a cache file avoiding requests against the server
        # print("Creating cache file : " + cacheFile)
        page = requests.get(urlResource)
        createFile(cacheFile, page.content.decode('utf-8'))


def createDir(path):
    # Does the dir exists?
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory failed")
        else:
            print("Successfully created the directory")
    else:
        print("[Reading from cache]")


def createFile(fileName, content):
    print(fileName)
    file = open(fileName, 'w')
    file.write(content)
    file.flush()
    file.close()

def createItemsList(fileName):
    #Get initial page
    url = 'http://localhost/pulse_wp/cases-de-comunicacao-e-marketing/'
    query = '//div[@class="item-box"]/a/@href'
    cases = getHtmlContent(url, query)
    html = ', '.join(cases)
    createFile(fileName, html)


def getHtmlContent(url, query):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    raw = tree.xpath(query)
    # type(raw)
    return raw


def xpathToJson(urlAgainst, xpathQuery, jsonKey, separator=''):
    output = separator.join(getHtmlContent(urlAgainst, xpathQuery))
    return '\n\t "'+jsonKey+'" : "' + output + '"'


def clearTitle(title):
    # print(title)
    badChars = [' ', 'ç', 'ã', 'é', 'á', 'â', 'í']
    goodChars = ['-', 'c', 'a', 'e', 'a', 'a', 'i']

    for char in title:
        if char in badChars:
            myIndex = badChars.index(char)
            title = title.replace(char, goodChars[myIndex])

    return title.lower()
