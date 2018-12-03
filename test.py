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
import timeit

a_list = ('GBR','ARG','BRA')
# a_list = ('GBR','')
news_list = process(*a_list)
trig_dict = read_trigger_config('triggerlist.txt')

trig_story = filter_stories(news_list,trig_dict)

