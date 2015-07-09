__author__ = 'jason'


def geo_search(query):
    results = dict()
    # use the geonames webAPI to fill dictionary with data
    results["country"] = "Greece"

    return results


import urllib2
from bs4 import BeautifulSoup

Cache = dict()
def getCountry(query):
    
    if query in Cache:
        return Cache[query]
    else:
        url = "http://api.geonames.org/search?q=" + query.replace(" ","%20") + "&maxRows=1&username=project0&password=jasonaris"
        response = urllib2.urlopen(url)
        page_source = response.read()

        soup = BeautifulSoup(page_source)
        countryname = str(soup.find('countryname'))
        
        result = dict()
        if countryname is None:
            result["country"] = ""
        else:
            result["country"] = countryname.replace("<countryname>","").replace("</countryname>","")

        name = str(soup.find('name'))
        if name is None:
            result["place"] = ""
        else:
            result["place"] = name.replace("<name>","").replace("</name>","")
        
        Cache[query] = result
    
        return result

