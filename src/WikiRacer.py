import sys
import wikipedia
import json
from collections import deque
#from flask import Flask
import networkx as nx
#import matplotlib.pyplot as plt
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


def GetTitles(title,verbose=True):
    """
        Given a title of a Wikipedia page, this function returns 
        the titles of the Wikipedia links in the page.

        Note: The Wikipedia module uses the BeautifulSoup module and
        it does not always use the best HTML parser in python 3.
    """
    if verbose:
        try:
            print(title)
        except:
            print("Warning: 'gbk' can not encode unicode characters")
    try:
        page = wikipedia.page(title)
        return page.links
    except:
        return []

def GetTitleOfLink(url):
    """
        Given a Wikipedia URL, this function returns the title of
        the page.
    """
    wiki_html = urlopen(url).read()
    parsed_html = BeautifulSoup(wiki_html,'html.parser')
    title_html = parsed_html.find('h1',attrs={'id':'firstHeading'})
    title = re.search('>([\w\s\d]+)</',str(title_html))
    print(title.group(1))
    return title.group(1)

def GetUrls(titles):
    """
       This function returns the URLs of the titles in the input list.

       titles: A list of Wikipedia page titles. 
    """
    links = []
    for title in titles:
        page = wikipedia.page(title)
        links.append(page.url)
    return links

def GetInputs(file_path):
    """
        This functions get the path to the input folder and read the
        JSON file in the folder. It returns the start and end title
        that is used in the wiki race.

        file_path: The file path of the output file.
    """
    ajson = open(file_path,'r')
    input_json = json.load(ajson)
    start_url = input_json['start']
    end_url = input_json['end']
    start_title = GetTitleOfLink(start_url)
    end_title = GetTitleOfLink(end_url)
    ajson.close()
    return start_title,end_title

def TimeElapsed(starting_time):
    """
       This function returns the elapsed time of the search.

       starting_time: The clock time when the Wikiracer start searching
    """
    current_time = time.clock()
    return current_time - starting_time

def ConvertToJson(start_title,target_title,alist,file_path):
    """
       This function writes the outputs in the specified folder in
       JSON format.

       start_title: The title of the starting page
       target title: The title of the end page
       alist: A list of the titles of the shortest path
       file_path: A path to the output file
    """
    output_file = open(file_path,'w')
    start_url = GetUrls([start_title])
    end_url = GetUrls([target_title])
    path_urls = GetUrls(alist)
    url_dict = {"start": start_url,
                "end": end_url,
                "path": path_urls}
    json.dump(url_dict,output_file)
    output_file.close()

def FindShortestPath(start,target,max_time = 3600):
    """
       This function uses a graph to represent link-connectivity  
       between the start and end pages. The shortest path is
       found using the Dijkstra's algorithm.

       start: Title of the starting page (A graph node)
       target: Title of the end page (A graph node)
       max_time: The time limit in seconds that the Wikiracer is 
       allowed to search for the path. 
    """
    start_time = time.clock()
    print('WikiRacer is searching for the shortest path between %s \
and %s. Please be patient!' %(start,target))
    graph = nx.Graph()
    queue = deque()
    queue.append(start)
    found = False
    timeout = False
    while not found and not timeout:
        for item in list(queue):
            titles = GetTitles(item)
            '''check whether target is in the titles'''
            if target in titles:
                graph.add_edge(item,target)
                print('Processing time: %i sec' % TimeElapsed(start_time))
                return nx.dijkstra_path(graph,start,target),graph
                found = True
                break
            for title in titles:
                queue.append(title)
                graph.add_edge(item,title)
            queue.popleft()
        current_time = time.clock()
        processing_time =  TimeElapsed(start_time)
        if processing_time >= max_time:
            timeout = True
    

def main():
    """
        This function reads the folder pathes for input and output 
        files and pass it to FindShortestPath function to find the
        path between start and end pages. 
        
    """
    args = sys.argv[1:]

    if not args:
        print ("Error: Please add the '[input_file output_file]' to \
your execution command.")
        sys.exit(1)
    
    input_path = args[0]
    output_path = args[1]
    starting_title,ending_title = GetInputs(input_path)
    
    min_path,graph = FindShortestPath(starting_title,ending_title)
    ConvertToJson(starting_title,ending_title,min_path,output_path)
    
    try:
        print('Path found:')
        print(min_path)
    except:
        print('Path not found')  

if __name__ == '__main__':
    main()
