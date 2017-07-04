#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 15:49:20 2017

@author: johannes
"""


def findAdditionalElements(elements_list, search_list, arr=[]):
    noMoreElementsIn_search_list = 1
    for item0 in elements_list:
        i = 0
        while i < len(search_list):
            if (item0[0] == search_list[i][0] or
                    item0[0] == search_list[i][1] or
                    item0[1] == search_list[i][0] or
                    item0[1] == search_list[i][1]):
                arr.append(search_list.pop(i))
                i = i - 1
                noMoreElementsIn_search_list = 0
            i = i + 1
    return arr if(bool(noMoreElementsIn_search_list)) else \
        findAdditionalElements(arr, search_list, arr)
