# Project:  World News Articles Matching
# File:     NewsArticle.py
# Authors:  Jason Papapanagiotakis, Aris Kotsomitopoulos
# Github:   https://github.com/A-J-Thesis/World-News-Arcticles-Matching

from textblob import TextBlob
from textblob.np_extractors import FastNPExtractor
from hashtagify import Hashtagify
try:
    from nltk.tag.stanford import StanfordNERTagger
except:
    from nltk.tag.stanford import NERTagger
from geonames import *
from nltk.corpus import stopwords


class NewsArticle:
    def __init__(self, id, title, date, text, url, description):
        self.id = id
        self.title = title
        self.date = date
        self.metadata = dict()
        self.metadata["plaintext"] = text
        self.metadata["description"] = description
        self.metadata["title"] = title
        self.url = url
        self.heuristics()
    
    def heuristics(self):
        if self.url.find("abcnews.") != -1:
            if self.url.find("videos/") != -1 or self.url.find("video/") != -1:
                self.metadata["plaintext"] = self.metadata["title"]

    def extract_metadata(self):
        self.extract_noun_phrases()
        self.create_title_hashtags()
        self.named_entity_extraction()

    def extract_noun_phrases(self):
        extractor = FastNPExtractor()
        text = TextBlob(self.metadata["plaintext"], np_extractor=extractor)
        self.metadata["noun_phrases"] = []
        for noun_phrase in text.noun_phrases:
            self.metadata["noun_phrases"].append(noun_phrase)

    def create_title_hashtags(self):
        ht = Hashtagify(title=self.metadata["title"], content=self.metadata["plaintext"])

        # tag the relevant words on the title and save the result
        tagged_title = ht.hashtagify(0.40)

        # get only the tagged words and save them separately
        l_words = tagged_title.split(' ')
        l_tags = []
        for w in l_words:
            if "#" in w:
                l_tags.append(w)
        self.metadata["hashtags"] = l_tags

    def named_entity_extraction(self):
        try:
            ner = StanfordNERTagger('../lib/stanford-lib/english.all.3class.distsim.crf.ser.gz',
            '../lib/stanford-lib/stanford-ner.jar')
            extracted_ne2 = ner.tag(self.metadata["plaintext"].replace(".", " ").replace(",", " , ").replace("!", " ").replace("?", " ").replace("\n"," ").split())
            extracted_ne = extracted_ne2            
        except:
            ner = NERTagger('../lib/stanford-lib/english.all.3class.distsim.crf.ser.gz',
            '../lib/stanford-lib/stanford-ner.jar')            
            extracted_ne2 = ner.tag(self.metadata["plaintext"].replace(".", " ").replace(",", " , ").replace("!", " ").replace("?", " ").replace("\n"," ").split())
            extracted_ne = extracted_ne2[0]
        
        persons = self.process_named_entities(extracted_ne, "PERSON")
        organizations = self.process_named_entities(extracted_ne, "ORGANIZATION")
        locations = self.unify_locations(extracted_ne)
        
        self.metadata["persons"] = persons
        self.metadata["organizations"] = organizations
        self.metadata["locations"] = locations

        general_locations = self.enrich_location(locations)
        self.metadata["countries"] = general_locations[0]   # a list of countries
        self.metadata["places"] = general_locations[1]      # a list of places

    def process_named_entities(self, named_entities_l, type):
        aggregated_results = []
        prev_flag = 0
        for named_entity in named_entities_l:
            if named_entity[1] == type and prev_flag == 0:
                aggregated_results.append(named_entity[0])
                prev_flag = 1
            elif named_entity[1] == type and prev_flag == 1:
                aggregated_results[len(aggregated_results) -1] += " " + named_entity[0]
            else:
                prev_flag = 0

        return aggregated_results

    def unify_locations(self, named_entities):
        # rules:    LOCATION in LOCATION
        #           LOCATION of LOCATION
        #           LOCATION LOCATION
        #           LOCATION
        # return list with unified locations
        unified_locations = []

        # if there are less than 3 items in the list, no pattern can be matched
        if len(named_entities) < 3:
            return None

        index = 0

        while index < len(named_entities) - 2:
            if named_entities[index][1] == "LOCATION" and \
               named_entities[index + 1][0].lower() == "in" and \
               named_entities[index + 2][1] == "LOCATION":        # first rule matches
                unified_locations.append(named_entities[index][0] + named_entities[index + 2][0])
                index += 3

            elif named_entities[index][1] == "LOCATION" and \
                named_entities[index + 1][0].lower() == "of" and \
                named_entities[index + 2][1] == "LOCATION":        # second rule matches

                unified_locations.append(named_entities[index][0] + named_entities[index + 2][0])
                index += 3

            elif named_entities[index][1] == "LOCATION" and named_entities[index + 1][1] == "LOCATION":
                                                                    # thrid rule matches
                unified_locations.append(named_entities[index][0] + " " + named_entities[index + 1][0])
                index += 2

            elif named_entities[index][1] == "LOCATION":
                                                                    # fourth rule matches
                unified_locations.append(named_entities[index][0])
                index += 1
            else:
                index += 1

        return unified_locations

    def remove_unwanted_words(self, named_entities):
        for u_word in self.unwanted_words:
            named_entities = [(w, pos) for w, pos in named_entities if not w in stopwords.words('english')]
        return named_entities
       

    def enrich_location(self, unified_locations):
        # return tuple with two lists (countries, places)
        # where each list have the countries and the places found with geo_names API
        if unified_locations is None:
			return [[],[]]
			
        l_places = []
        l_countries = []
        for location in unified_locations:
            results = getCountry(location)   # get dictionary with geonames webAPI results
            if "country" in results:
                l_countries.append(results["country"])

            if "place" in results:
                l_places.append(results["place"])

        aggregated_results = l_countries, l_places

        return aggregated_results

