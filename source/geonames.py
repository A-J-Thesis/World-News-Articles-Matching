# Project:  World News Articles Matching
# File:     geonames.py
# Authors:  Jason Papapanagiotakis, Aris Kotsomitopoulos
# Github:   https://github.com/A-J-Thesis/World-News-Arcticles-Matching


# def geo_search(query):
#     results = dict()
#     # use the geonames webAPI to fill dictionary with data
#     results["country"] = "Greece"

#     return results


import urllib2
from bs4 import BeautifulSoup

Cache = dict()
GeonamesErrCodes = dict()
GeonamesErrCodes["10"]="Authorization Exception"
GeonamesErrCodes["11"]="record does not exist"
GeonamesErrCodes["12"]="other error"
GeonamesErrCodes["13"]="database timeout"
GeonamesErrCodes["14"]="invalid parameter"
GeonamesErrCodes["15"]="no result found"
GeonamesErrCodes["16"]="duplicate exception"
GeonamesErrCodes["17"]="postal code not found"
GeonamesErrCodes["18"]="daily limit of credits exceeded"
GeonamesErrCodes["19"]="hourly limit of credits exceeded "
GeonamesErrCodes["20"]="weekly limit of credits exceeded"
GeonamesErrCodes["21"]="invalid input"
GeonamesErrCodes["22"]="server overloaded exception"
GeonamesErrCodes["23"]="service not implemented"

def getCountry(query):
    
    if query in Cache:
        return Cache[query]
    else:
        url = "http://api.geonames.org/search?q=" + query.replace(" ","%20") + "&maxRows=1&username=project0&password=jasonaris"
        response = urllib2.urlopen(url)
        page_source = response.read()

        soup = BeautifulSoup(page_source)
        check = soup.find("status")
        if check is not None:
            val = check.get("value")
            if val != None:
                if val in GeonamesErrCodes:
                    RuntimeError("Geonames: " + GeonamesErrCodes[val] + " , query was: ." + query + ".")

        countryname = str(soup.find('countryname'))
        
        result = dict()
        if countryname is not None:
            result["country"] = countryname.replace("<countryname>","").replace("</countryname>","")

        name = str(soup.find('name'))
        if name is not None:
            result["place"] = name.replace("<name>","").replace("</name>","")
        
        Cache[query] = result
    
        return result

