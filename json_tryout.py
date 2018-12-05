#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 22:06:05 2018

@author: BryanK
"""
import json

simple = dict(int_list=[1, 2, 3],text='string',number=3.44,boolean=True,none=None)
from datetime import datetime

class A(object):
    def __init__(self, simple):
        self.simple = simple        
    def __eq__(self, other):
        if not hasattr(other, 'simple'):
            return False
        return self.simple == other.simple
    def __ne__(self, other):
        if not hasattr(other, 'simple'):
            return True
        return self.simple != other.simple
 
complex = dict(a=A(simple), when=datetime(2016, 3, 7))

print(json.dumps(simple,indent=4))

def jdefault(o):
    return o.__dict__

class User(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password
alice = User('Alice A. Adams', 'secret')

a_str = json.dumps(alice, default=jdefault)
print(a_str)