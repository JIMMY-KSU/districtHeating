# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np 


class Finder():
    def __init__(self):
        pass
    
    def findAllItems(self, item_list, search_list, arr=[]):
        noMoreElementsIn_search_list = 1
        for item0 in item_list:
            i = 0
            while i < len(search_list):
                if (item0[0] == search_list[i][0] or item0[0] == search_list[i][1]
                or item0[1] == search_list[i][0] or item0[1] == search_list[i][1]):
                    arr.append(search_list[i])
                    search_list = np.delete(search_list, i, axis=0)
                    i = i - 1
                    noMoreElementsIn_search_list = 0
                i = i + 1
        return np.asarray(arr) if(bool(noMoreElementsIn_search_list)) else\
                        self.findAllItems(arr, search_list, arr)
    
    
if __name__ == "__main__":
    print('Finder \t\t\t run directly')
    pipes = [[1,2],[2,3],[3,4],[4,1],[4,5],[4,6],[4,7],[8,11],\
             [9,11],[10,12],[12,11],[11,0]] #first value = SP, sec = RP
    consumer = [[1,11],[1,12],[5,8],[6,9],[7,10]]
    producer = [[1,0]]

    pipes_ab = pipes
    pipes_a = []
    producer_a = producer

    test_finder = Finder()
    print(test_finder.findAllItems([[1,None]], pipes_ab))
    print(pipes_ab)

else:
    print('Finder \t\t\t was imported into another module')



             
          
