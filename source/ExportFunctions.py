# Project:  World News Articles Matching
# File:     ExportFunctions.py
# Authors:  Jason Papapanagiotakis, Aris Kotsomitopoulos
# Github:   https://github.com/A-J-Thesis/World-News-Arcticles-Matching

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
