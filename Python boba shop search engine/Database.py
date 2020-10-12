# Yong Yu Xuan
# CIS 41B
# Final Project
# Description is attached in readme.txt

import requests
import json
import threading
import math
import sqlite3

def combineInfo(num):
    '''combineInfo: combines the data from all 4 JSON file into a single dictionary'''
    dictList = []
    mergeDict = {}
    for i in range(4):
        with open(str(i*50) +'_bobadata.json', 'r') as fh:
            d = json.load(fh)
        dictList.append(d)
        
    for dic in dictList:
        for k, v in dic.items():
            mergeDict.setdefault(k, []).append(v)
    return mergeDict

def createTable(cur,d):
    '''createTable: Creates a main table called Boba, 3 subtables that handle the city, ranking and price'''
    #CITY TABLE TO HAVE UNIQUE ID FOR EACH CITY
    cur.execute("DROP TABLE IF EXISTS Cities")
    cur.execute('''CREATE TABLE Cities(
                                id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                                city TEXT UNIQUE ON CONFLICT IGNORE)''')
    
    #RANKING TABLE TO HAVE UNIQUE ID FOR EACH RANKING
    cur.execute("DROP TABLE IF EXISTS Ranking")
    cur.execute('''CREATE TABLE Ranking(
                                id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                                ranking REAL UNIQUE ON CONFLICT IGNORE)''')
    
    cur.execute("DROP TABLE IF EXISTS Price")
    cur.execute('''CREATE TABLE Price(
                                id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                                price REAL UNIQUE ON CONFLICT IGNORE)''')
    
    #MAIN TABLE TO DIS{PLAY ALL THE INFO
    cur.execute("DROP TABLE IF EXISTS Boba") 
    cur.execute("""CREATE TABLE Boba(
                                cityID INTEGER,
                                bobaName TEXT,
                                rankingID INTEGER,
                                address TEXT,
                                distance REAL,
                                priceID INTEGER,
                                description TEXT)""")
    
    for cities in d:
        cur.execute('''INSERT INTO Cities (city) VALUES (?)''', (cities,))
        for bobaShops in d[cities]:
            for bobaName in bobaShops:
                for info in bobaShops[bobaName]:
                    cur.execute('''INSERT INTO Ranking (ranking) VALUES (?)''', (info[0],))
                    cur.execute('''SELECT id FROM Ranking WHERE ranking = ?''',(info[0],))
                    ranking_id = cur.fetchone()[0]
                                
                    cur.execute('''SELECT id FROM Cities WHERE city = ?''', (cities,))
                    city_id = cur.fetchone()[0] 
                
                    cur.execute('''INSERT INTO Price (price) VALUES (?)''', (info[1],))
                    cur.execute('''SELECT id FROM Price WHERE price = ?''', (info[1],))
                    price_id = cur.fetchone()[0]
                                
                    cur.execute('''INSERT INTO Boba 
                                (cityID, bobaName, rankingID, address, distance, priceID, description)
                                VALUES (?,?,?,?,?,?,?)''', (city_id, bobaName, ranking_id, ', '.join(info[2]), info[3], price_id, ', '.join(info[4])))

def main():
    conn = sqlite3.connect("boba.db")
    cur = conn.cursor()        
    d = combineInfo(4)
    createTable(cur, d)
    conn.commit()
main()