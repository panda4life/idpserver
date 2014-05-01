# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 14:11:45 2014

@author: James Ahad
"""

import os
def create_path(path):
    import os.path as os_path
    paths_to_create = []
    while not os_path.lexists(path):
        paths_to_create.insert(0, path)
        head,tail = os_path.split(path)
        if len(tail.strip())==0: # Just incase path ends with a / or \
            path = head
            head,tail = os_path.split(path)
        path = head
    for path in paths_to_create:
        os.mkdir(path)

