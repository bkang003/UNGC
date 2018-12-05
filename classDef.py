#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 11:23:17 2018

@author: BryanK
"""

#import feedparser
import string
import time
import pandas as pd
from glob import iglob
import os
#import threading
# from project_util import translate_html
#from mtTkinter import *
from datetime import datetime
import newspaper
from newspaper import Article
# os.chdir('/home/yy2891/indicator+GKG_2013_2018_RAW')
# b=[x for x in glob.glob('*.csv')]

#import pytz

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================        \


def process(df, *args): #input filename
    """
    Fetches news items from export.csv file
    Returns a list of News.
    """
#        try:
#            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
#            pubdate.replace(tzinfo=pytz.timezone("GMT"))
#          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
#          #  pubdate.replace(tzinfo=None)
#        except ValueError:
#            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

#    df = pd.read_csv('20131126.csv')
    
    ret = []
    for index,row in df.iterrows():
        if str(row['Actor1CountryCode']).upper() in args:
            gevent_id = row['GLOBALEVENTID']
            country_Code = row['Actor1CountryCode']
            tone = row['AvgTone']
            dateAdded = row['DATEADDED']
            url = row['SOURCEURL']
    
            news = News(gevent_id,country_Code,tone,dateAdded,url)
            ret.append(news)
    print('\nThere are %d items in News.'% len(ret))
    return ret

    
class News:
    def __init__(self,gevent_id,countryCode,tone,dateAdded,url):
        self.gevent_id = gevent_id
        self.countryCode = countryCode
        self.tone = tone
        self.dateAdded = dateAdded
        self.url = url
        self.text = None
        self.publish_date = None
        self.taxonomy = []

    def get_gevent_id(self):
        return self.gevent_id
    def get_countryCode(self):
        return self.countryCode
    def get_tone(self):
        return self.tone
    def get_dateAdded(self):
        return self.dateAdded
    def get_url(self):
        return self.url
    def get_text(self):
        return self.text
    def get_publish_date(self):
        return self.publish_date
    def get_taxonomy(self):
        return self.taxonomy
    
    def set_taxonomy(self,taxonomy):
        self.taxonomy.append(taxonomy)
    
    def clean_text(self):
        article = Article(self.url)
        try:
            article.download()
            article.parse()
            self.text,self.publish_date = article.text, article.publish_date
            print('Success.')
        except:
            self.text,self.publish_date = None, None
            print('No text found.')

class Trigger:
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError
        
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase
    def get_phrase(self):
        return self.phrase
    def evaluate(self, story):
        return self.is_phrase_in(story)
    
    def is_phrase_in(self, text):
        raw_text = text.lower()
        raw_phrase = self.phrase.lower()
        
        for char in raw_text:
            if char in string.punctuation:
                raw_text = raw_text.replace(char,' ')
        raw_list = raw_text.split()
        phrase_list = raw_phrase.split()
        
        if phrase_list[0] not in raw_list:
            return False
        else:
            temp_index = raw_list.index(phrase_list[0])
            return phrase_list == raw_list[temp_index:temp_index + len(phrase_list)]

class TextTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    def get_phrase(self):
        return self.phrase
    def evaluate(self, story):
        return self.is_phrase_in(story.get_text())

class AndTrigger(Trigger):
    def __init__(self, *args):
        self.args = args
        
    def get_args(self):
        phrase_list = [arg.get_phrase() for arg in self.args]
        return '+'.join(phrase_list)
    def evaluate(self, story):
        true_list = [T.evaluate(story) for T in self.args]
        result = (True, False)[False in true_list]
        return result
#        return self.T1.evaluate(story) and self.T2.evaluate(story) and self.T3.evaluate(story)

class OrTrigger(Trigger):
    def __init__(self,*args):
        self.args = args
    def get_args(self):
        phrase_list = [arg.get_phrase() for arg in self.args]
        return '+'.join(phrase_list)
    def evaluate(self, story):
        true_list = [T.evaluate(story) for T in self.args]
        result = (False,True)[True in true_list]
        return result
    
class NotTrigger(Trigger):
    def __init__(self, T):
        self.T = T
    def get_T(self):
        return self.T
    def evaluate(self, story):
        return not self.T.evaluate(story)

    
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    
    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
#    trigger_list = []
    trigger_dict = {}
    
    for line in lines:
        l_item = line.split('+')
#        if l_item[0] == 'ADD':
#            for item in l_item[1:]:
#                trigger_list.append(trigger_dict[item])
        if l_item[1] == 'TEXT':
            trigger_dict[l_item[0]] = TextTrigger(l_item[2])
        elif l_item[1] == 'AND':
            arg_tuple = tuple(TextTrigger(item) for item in l_item[2:])
            trigger_dict[l_item[0]] = AndTrigger(*arg_tuple)
        
#            if l_item[1] == 'TITLE':
#                trigger_dict[l_item[0]] = TitleTrigger(l_item[2])    
#            elif l_item[1] == 'DESCRIPTION':
#                trigger_dict[l_item[0]] = DescriptionTrigger(l_item[2])
#            elif l_item[1] == 'AFTER':
#                trigger_dict[l_item[0]] = AfterTrigger(l_item[2])
#            elif l_item[1] == 'BEFORE':
#                trigger_dict[l_item[0]] = BeforeTrigger(l_item[2])
#            elif l_item[1] == 'NOT':
#                T_not = trigger_dict[l_item[2]]
#                trigger_dict[l_item[0]] = NotTrigger(T_not)
#            elif l_item[1] == 'AND':
#                T_and1 = trigger_dict[l_item[2]]
#                T_and2 = trigger_dict[l_item[3]]
#                trigger_dict[l_item[0]] = AndTrigger(T_and1,T_and2)
#            elif l_item[1] == 'OR':
#                T_or1 = trigger_dict[l_item[2]]
#                T_or2 = trigger_dict[l_item[3]]
#                trigger_dict[l_item[0]] = OrTrigger(T_or1,T_or2)
    
    #print(lines) # for now, print it so you see what it contains!
    return trigger_dict    
    
def filter_stories(stories,trigger_dict,num_line):
    """
    Takes in a list of News instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
#    trig_story = []
    temp_stories = stories[:num_line]
    for index, story in enumerate(temp_stories):
        print('\n'+str(index),end=' ')
        print(story.get_gevent_id(),story.get_dateAdded())
        story.clean_text()
        if story.get_text() == None:
            pass
        else:
            for key,trig in trigger_dict.items():
                try:
                    story.set_taxonomy((key,trig.get_args())) if trig.evaluate(story) \
                    else print('False',end=' ')
                except AttributeError:
                    pass
#                print('Error occured',end=' ')
        #trig_story.append(story.get_text())
#    return trig_story


