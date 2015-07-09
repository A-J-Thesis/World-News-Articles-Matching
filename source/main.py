from NewsAggregator import NewsAggregator
from NewsArticle import NewsArticle
from XMLparser import *
from nltk.corpus import stopwords
from multiprocessing import Pool, Process, Value, Lock
import multiprocessing
import signal
import sys,os
from os import listdir
from os.path import isfile, join
from time import sleep
from ProgressBar import ProgressBar
from ProgressBar import SupportBar
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0
    
def ExportResults(aggr):
    results = []
    for topic in aggr.topics:
        if len(aggr.topics[topic]) > 1:
            temp_links = []
            temp_plaintexts = []
            for idx in aggr.topics[topic]:
                if aggr.articles[idx].metadata["plaintext"] not in temp_plaintexts:
                    temp_plaintexts.append(aggr.articles[idx].metadata["plaintext"])
                    temp_links.append(aggr.articles[idx].url)
            if len(temp_links) >= 2:
                results.append(temp_links)
    return results
    
#some Countries
countries = ["Greece"]
#read weights values from property file
# instantiate
config = ConfigParser()

# parse existing file
config.read('properties.ini')

# read values from a section
weights = []
weights.append(config.getint('weights_values', 'noun_phrases'))
weights.append(config.getint('weights_values', 'hashtags'))
weights.append(config.getint('weights_values', 'title'))
weights.append(config.getint('weights_values', 'persons'))
weights.append(config.getint('weights_values', 'organizations'))
weights.append(config.getint('weights_values', 'locations'))
weights.append(config.getint('weights_values', 'countries'))
weights.append(config.getint('weights_values', 'places'))
weights.append(config.getint('weights_values', 'plaintext'))
weights.append(config.getint('weights_values', 'description'))
similarity_threshold = config.getfloat('similarity_threshold', 'percentage')

#set 35% similarity
aggr = NewsAggregator(similarity_threshold,weights)

#Read all files from folder
xmlfiles = [ f for f in listdir("../filesXML") if isfile(join("../filesXML",f)) ]
progressBar = ProgressBar(int(len(xmlfiles)))
supportBar = SupportBar()

#create file for results
results = open('../output/results.txt', 'w+')
debug = open('../output/debug.txt', 'w+')

id = -1
for filename in xmlfiles:
    larct = parse("filesXml/" + filename)
    sys.stdout.write("(" + str(len(larct)) + "/" )
    sys.stdout.flush()
    for arcticle in larct:
        id += 1
        try:
            newarticle = NewsArticle(id, arcticle[0], arcticle[1], arcticle[2], arcticle[3], arcticle[4], countries)
            newarticle.extract_metadata()

            aggr.add_article(newarticle)
            
            #Update StatusBar
            supportBar.increase()
            size = len(str(supportBar.get()))
            spaces = ' ' * (4 - size)
            sys.stdout.write("{0}){1}\b\b\b\b\b".format(supportBar.get(), spaces))
            sys.stdout.flush()
            
        except KeyboardInterrupt:
            print "\nProgram Closed Successfully!"
            sys.exit(1)
        except Exception,e:
            print "\nException occurred!" + filename
            print str(e)
    supportBar.init()
    progressBar.update()
    
    #Write to Debug File
    finalResults = ExportResults(aggr)
    
    debug.write(filename + "\nDone.\n")
    debug.flush()
    for group in finalResults:
        debug.write("---------------------------------------------------------\n")
        for link in group:
            debug.write(link + "\n")
        debug.write("---------------------------------------------------------\n")
        debug.flush()

#print "All filenames Completed."

#for topic in aggr.topics:
#    if len(aggr.topics[topic]) > 1:
#        results.write("---------------------------------------------------------\n")
#        results.write("MATCH FOUND\n")
#        for id in aggr.topics[topic]:
#            results.write(aggr.articles[id].url + "\n")
#        results.write("---------------------------------------------------------\n")
#        results.flush()

finalResults = list(reversed(sorted(ExportResults(aggr), key=len)))
for group in finalResults:
    results.write("---------------------------------------------------------\n")
    results.write("MATCH FOUND\n")
    for link in group:
        results.write(link + "\n")
    results.write("---------------------------------------------------------\n")
    results.flush()
        





    
    
    
