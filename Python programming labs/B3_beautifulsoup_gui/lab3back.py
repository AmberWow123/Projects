'''
Description: This file contains a driver function named main() that creates a JSON file,
then opens that JSON file and puts in the data from the JSON file into the database file.
'''

import requests
import codecs
import sys
import sqlite3
from bs4 import BeautifulSoup
import re
import time
import json


def main():
    """ main() creates a json file, and then stores data from the JSON file into the database."""
    
    """
    page = requests.get('https://en.wikipedia.org/wiki/List_of_most_popular_given_names')
    soup = BeautifulSoup(page.content, 'lxml')
    countriesDict = {}
    for tag in soup.find_all('tr'):    # table row
        nameList = tag.find_all('td')    # little boxes in one row
        if nameList:
            variable = nameList[0].get_text().encode(sys.stdout.encoding, errors='ignore').decode(sys.stdout.encoding)
            if variable != "Region" or variable != '':
                country = variable
                countryName = re.sub("[\(|\[|\,].*", "", country).strip()
                countriesList = []
                for i in range(1, len(nameList)):
                    var = nameList[i].get_text().encode(sys.stdout.encoding, errors='ignore').decode(sys.stdout.encoding)
                    if var.strip("\n") != 'NA':
                        if ',' in var:
                            countriesList.extend(var.strip("\n").split(', '))
                        else:
                            countriesList.append(var.strip("\n"))
                if countryName in countriesDict:
                    countriesDict[countryName] = countriesDict[countryName] + (countriesList)
                else:
                    countriesDict[countryName] = countriesList

    with open("data.json", "w") as fh :
        json.dump(countriesDict, fh, indent = 5)
        
    """

    with open("data.json") as fh :
        d = json.load(fh)

    conn = sqlite3.connect("popularName.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS PopularNameDB")
    
    maxNum = max([len(value)   for value in d.values()])
    
    
    cur.execute("""CREATE TABLE PopularNameDB(country TEXT)""")
    for i in range(maxNum) :
        cur.execute("ALTER TABLE PopularNameDB ADD COLUMN {} TEXT".format("name" + str(i)))
    
    listN = ["name"+str(i)   for i in range(maxNum)]

    
    for i in d:
        cur.execute("INSERT INTO PopularNameDB (country) VALUES (?)", (i,))
        num = len(d[i])
        cur.execute("UPDATE PopularNameDB SET {} = {}  WHERE country = ?".format(tuple(listN[:num]), tuple(d[i])), (i,))
    
    conn.commit()
    conn.close()


main()

