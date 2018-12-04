#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 11:44:04 2018

@author: BryanK
"""

#def test_fun(*args):
#    result = 0
#    for x in args:
#        result += x 
#    return result
#
#class Animal:
#    def __init__(self,num_legs):
#        self.num_legs = num_legs
#        self.name = 
#animal_list = [1,2,3]

# Initialize a country search by CountryCode

a_list = ('GBR','ARG','BRA')
# a_list = ('GBR','')
news_list = []

path = os.path.expanduser("/Users/BryanK//Documents/Github/UNGC/*.csv")
all_rec = iglob(path, recursive=True) 
#dataframes = (pd.read_csv(f) for f in all_rec)
#df = pd.concat(dataframes, ignore_index=True)

# Select corresponding country in the dataset.
# Read in taxonomy from 'triggerlist.txt'
for f in all_rec:
    news_list.extend(process(pd.read_csv(f),*a_list))
trig_dict = read_trigger_config('triggerlist.txt')

# Filter News with the trigger in the trig_dict
num_line = len(news_list)
#print(num_line)
trig_story = filter_stories(news_list,trig_dict,num_line)


"""
Print first 30 sample text with '-------' as separator.
"""
#for i in range(num_line):
#    if news_list[i].get_taxonomy() !=[]:
#        print(news_list[i].get_countryCode(), news_list[i].get_url())
#        print(news_list[i].get_taxonomy())
#        print('--'*10)
