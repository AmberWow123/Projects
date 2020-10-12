# Shania Ie
# CIS 41B
# Final Project
# Description is attached in readme.txt

import requests
import json
import threading
import math

def fetchData(offset):
    '''fetchData: Fetching data of boba shops around De Anza College using Yelp API (json format). The extracted data will then be stored in a JSON file'''
    auth_token = 'jTsYlQOGT_UWN3JHQg7h_5pNxd_U1p9Nyz9Yc6MJms0vzSeiNFQbhWXwRAI7o2dOTSQwdf0W2-4HS7HMTR4zubFoI1hRcNjQjps9C2tVS_5t5ZND6AMCCJPx6haGXHYx'
    hed = {'Authorization': 'Bearer ' + auth_token}
    cityList = ['Cupertino', 'San Jose', 'Mountain View', 'Palo Alto', 'Santa Clara', 'Sunnyvale', 'Saratoga']
    
    bobaCity = {}
    for i in range(len(cityList)):
        # Since Yelp only returns maximum 50 shops per call, therefore offset is needed to fetch the next page
        page = requests.get('https://api.yelp.com/v3/businesses/search?location='+ cityList[i] +'&term=Bubble Tea&limit=50&alias =bubbletea&offset=' + str(offset), headers= hed)
        resultList = page.json()
        bobaShops = shopList(resultList, cityList[i])
        bobaCity[cityList[i]] = bobaShops

    with open(str(offset) +'_bobadata.json', 'w') as fh:
        json.dump(bobaCity, fh, indent = 3)        

def shopList(resultList, city):
    '''
    shopList: Stores the information of each boba shop in a list of tuples (shop name, rating, price, address, distance, and shop details)
              The list of tuple is then stored in a dictionary with the shop name as the key to prevent duplicates
    '''
    shops = list({d['name'] for d in resultList['businesses'] for elem in d['categories'] if d['location']['city'] == city if 'Tea' in elem['title']})

    shopinfo = []
    for d in resultList['businesses']:
        if d['location']['city'] == city:
            for s in shops:
                if d['name'] == s:
                    distance = calculateDistance(d['coordinates']['latitude'], d['coordinates']['longitude'])
                    details = getCategories(d['categories'])
                    try:
                        shopinfo.append((s,d['rating'], d['price'], d['location']['display_address'], distance, details))   
                    except KeyError:
                        shopinfo.append((s,d['rating'], 'NULL', d['location']['display_address'], distance, details))
    
    bobaShops = {}
    for s in shops:
        for i in range(len(shopinfo)):
            if s not in bobaShops:
                bobaShops.setdefault(s,[])
            if shopinfo[i][0] == s:
                bobaShops[s].append(shopinfo[i][1:])
    return bobaShops

def calculateDistance(latitude, longitude):
    '''calculateDistance: Calculating the distance between each boba shop and De Anza College using the provided longitude and latitude''' 
    # Uses the haversine formula to calculate the distance between two points
    # latitude of De Anza College = 37.3196134 N
    # longitude of De Anza College = 122.0449176 W
    
    radius = 6371  #in kilometers
    lat = math.radians(latitude - 37.3196134)
    lon = math.radians(longitude - (-122.0449176))
    a = pow(math.sin(lat/2),2) + math.cos(math.radians(37.3196134)) * math.cos(math.radians(latitude)) * pow(math.sin(lon/2),2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = round((radius * c)* 0.621371,1)   #in miles

    return distance   

def getCategories(categories):
    '''getCategories: get the data for the description of the shop, eg. Coffee & Tea, Bubble Tea'''
    details = [elem['title'] for elem in categories]
    return details

def main():
    '''main: Creates a list of 4 threads to fetch data simultaneously'''
    threads = []
    for i in range(4):
        t = threading.Thread(target=fetchData, args= (i * 50,))
        threads.append(t)
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
main()