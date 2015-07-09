import xml.sax
from xml.dom.minidom import parse
import xml.dom.minidom

def parse(filename):
    
    # Open XML document using minidom parser
    DOMTree = xml.dom.minidom.parse(filename)
    collection = DOMTree.documentElement

    myList = []

    # Get all the Articles of the Site
    articles = collection.getElementsByTagName("Article")

    # Print detail of each Article.
    for article in articles:
        
        tempList = []
        #ID
        #if article.hasAttribute("id"):
        #    tempList.append(article.getAttribute("id"))
        
        #TITLE
        title = article.getElementsByTagName('title')[0]
        if len(title.childNodes) == 0:
            tempList.append("")
        else:
            tempList.append(title.childNodes[0].data)
            
        #DATE
        date = article.getElementsByTagName('date')[0]
        if len(date.childNodes) == 0:
            tempList.append("")
        else:
            tempList.append(date.childNodes[0].data)
            
        #MAINBODY
        MainBody = article.getElementsByTagName('MainBody')[0]
        if len(MainBody.childNodes) == 0:
            tempList.append("")
        else:
            tempList.append(MainBody.childNodes[0].data)
            
        #LINK
        Link = article.getElementsByTagName('Link')[0]
        if len(Link.childNodes) == 0:
            tempList.append("")
        else:
            tempList.append(Link.childNodes[0].data)
        
        #DESCRIPTION
        Description = article.getElementsByTagName('Description')[0]
        if len(Description.childNodes) == 0:
            tempList.append("")
        else:
            tempList.append(Description.childNodes[0].data)
        
        myList.append(tempList)
    return myList
    
    
        
