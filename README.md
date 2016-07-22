# Table of Contents

1. [Summary] (README.md#Sumary)
2. [Modules] (README.md#Modules)
3. [Method] (README.md#Method)


##Summary

[Back to Table of Contents] (README.md#table-of-contents)

WikiRacer is a python program which finds the shortest path between two pages in the Wikipedia. 

Wikiracing is a game that people play on Wikipedia. Given a starting article and an ending article, the objective of a wikirace is to get from the starting article to the ending article by only clicking on links occurring in the main bodies of wikipedia articles (not including the side navigation bar or the category footer).

<pre>
{
  "start": "<starting article>"
  "end": <ending article>"
}
</pre>

and which will return the results of the race in the form of a JSON object:

<pre>
{
  "start": "<starting article>"
  "end": <ending article>"
  "path": [
    "<starting article>"
	"<article at step 1>"
	"<article at step 2>"
	.
	.
	.
	"<article at step n-1>"
	"<ending article>"
  ]
}
</pre>

Each article will be identified with a fully expanded URL. So, for example, the Wikipedia article
about “Richard Feynman” will be represented by the URL https://en.wikipedia.org/wiki/Richard_Feynman

##Modules

The code was tested using Python 3.5.1. It uses the following modules:
1.	re (version 2.2.1)

2.	wikipedia (version 1.4.0)

3.	json (version 2. 0. 9)

4.	networkx (version 1.11)

5.	bs4 (version 4.4.1)

6.	urllib.request (version 3.5)


##Method
[Back to Table of Contents] (README.md#table-of-contents)

The WikiRacer.py uses a graph to identify connectivity relation between the links. The Wikipedia links are represented using nodes in the graph and are stored in a queue. The queue is initialized with the start link. The front item in the queue is used to call the Wikipedia API. The Wikipedia module returns a list of all links that are found in the main body of the article. First, the program inspects the list and checks whether the end (target) link is on the list. If the end link is found, it is added to the graph and a Dijkstra algorithm is used to find the shortest path between this node and the starting node. The program is terminated after writing the start, end, and shortest path links into JSON file. If the code cannot find the end link in the list, the new links are appended to the queue. Additionally, new edges are created in the graph between the new nodes and the front node in the queue. Then the front node is removed from the queue. This process continues until the program finds the end link or it reached to a maximum user-defined time.