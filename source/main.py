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

#Handle CTR+C
#def signal_handler(signal, frame):
#    print('You pressed Ctrl+C!')
#    sys.exit(0)
#signal.signal(signal.SIGINT, signal_handler)


#each Article has a unique local_id
id = Value('i',0)
lock = Lock()

#only for prints
##supplock = Lock()
##supportBar = SupportBar()

#some Countries
countries = ["Greece"]

def parallel_arct(arg):
    arcticle = arg
    local_id = 0
    with lock:
        local_id = id.value
        id.value += 1
    try:
        newarticle = NewsArticle(local_id, arcticle[0], arcticle[1], arcticle[2], arcticle[3], arcticle[4], countries)
        newarticle.extract_metadata()
    except Exception:
        print "Constructor"
    
    return newarticle
    
##    with supplock:
##        supportBar.increase()
##        size = len(str(supportBar.get()))
##        spaces = ' ' * (5 - size)
##        sys.stdout.write("{0}{1}\b\b\b\b\b".format(supportBar.get(), spaces))
##        sys.stdout.flush()
    
    
    
#set 40% similarity
aggr = NewsAggregator(0.40)

#Number of Pools
proc_pool = Pool()

#Read all files from folder
xmlfiles = [ f for f in listdir("filesXml") if isfile(join("filesXml",f)) ]
progressBar = ProgressBar(int(len(xmlfiles)))

#create file for results
results = open('results.txt', 'w+')
debug = open('debug.txt', 'w+')

   
for filename in xmlfiles:
    larct = parse("filesXml/" + filename)
    #for arcticle in larct:
        #newarticle = NewsArticle(id, arcticle[0], arcticle[1], arcticle[2], arcticle[3], arcticle[4], countries)
        #newarticle.extract_metadata()

    try:
        ##sys.stdout.write("(" + str(len(larct)) + "/" )
        ##sys.stdout.flush()
        newsarticles = proc_pool.map_async(parallel_arct, larct).get(9999999999)
        
        for newarticle in newsarticles:
            aggr.add_article(newarticle)

        ##supportBar.init()
        progressBar.update()
        debug.write(filename + " Done.\n")
        #debug.write("\n".join(aggr.topics) + "\n")
        for topic in aggr.topics:
            if len(aggr.topics[topic]) > 1:
                debug.write("---------------------------------------------------------\n")
                for id in aggr.topics[topic]:
                    debug.write(aggr.articles[id].url + "\n")
                debug.write("---------------------------------------------------------\n")
        debug.flush()
    except KeyboardInterrupt:
        proc_pool.terminate()
        print "Program Closed Successfully!"
        sys.exit(1)
    except Exception:
        print "Exception occurred!"

#    newsarticles = proc_pool.map(parallel_arct, larct)
#    
#    for newarticle in newsarticles:
#        aggr.add_article(newarticle)
#        
#    print filename + " done"
#    print aggr.topics
#    for topic in aggr.topics:
#        if len(aggr.topics[topic]) > 1:
#            print "---------------------------------------------------------"
#            print "MATCH FOUND"
#            for id in aggr.topics[topic]:
#                print aggr.articles[id].url
#            print "---------------------------------------------------------"

#print "All filenames Completed."

for topic in aggr.topics:
    if len(aggr.topics[topic]) > 1:
        results.write("---------------------------------------------------------\n")
        results.write("MATCH FOUND\n")
        for id in aggr.topics[topic]:
            results.write(aggr.articles[id].url + "\n")
        results.write("---------------------------------------------------------\n")
        results.flush()





    
    
    
