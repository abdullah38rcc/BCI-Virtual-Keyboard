"""
graph_demo.py  -- demo for module graph.
By leonardo maffi
This demo code version: 1.5, Agu 18 2005.
See graph_docs.txt for documentation.
"""

from graph import Graph

print "Maze demo:"
from sys import stdout # for mprint.
def mprint(*args): # This is copied from util module.
    "mprint(*args): prints variabiles without spaces between them."
    stdout.write(  "".join(map(str, args))  )

maze = """\
#####################
#S  #             # #
### ##### ####### # #
# #     #   #   # # #
# ##### ### # ### # #
#     #     #   # # #
# # ########### # # #
# # #           # # #
# # # # ######### # #
# #   #            T#
#####################"""

start = "S"
target = "T"
wall = "#"
g = Graph()
m = map(list, maze.split("\n"))
g.fromMap(m, good=lambda x: x!=wall)
for y,row in enumerate(m):
    for x,e in enumerate(row):
        if e == start: startNode = (x,y)
        elif e == target: targetNode = (x,y)
solution = set(g.shortestPath(startNode, targetNode))

#g.aplot() # Decomment this line to see the adj. matrix as graphics (it requires MatPlotLib).
if solution:
    print "Solution:", solution, "\n\n", "* is the solution path:"
    for y, row in enumerate(m):
        for x,e in enumerate(row):
            if (x,y) in solution and e not in (start, target):
                mprint("*")
            else:
                mprint(e)
        print
for n in g.xnodes(): # for the graph plot:
    g.nodeData[n] = n[0],-n[1]
#print g.plot2d() # Decomment this to see a 2D plot of the maze graph.
print "\nThere are more efficient ways to solve such kind of problems, this is just a simple demo."


"""
Maze demo:
Solution: set([(7, 3), (17, 8), (12, 1), (9, 1), (17, 7), (2, 1), (15, 1), (17, 3), (17, 2),
(10, 3), (16, 1), (17, 6), (3, 3), (11, 5), (8, 5), (6, 3), (14, 1), (11, 1), (18, 9), (1, 1),
(17, 5), (3, 2), (11, 4), (9, 3), (17, 1), (7, 5), (10, 1), (17, 4), (5, 3), (13, 1), (10, 5),
(19, 9), (17, 9), (9, 2), (3, 1), (11, 3), (7, 4), (4, 3), (9, 5)])

* is the solution path:
#####################
#S**#    *********# #
###*#####*#######*# #
# #*****#***#   #*# #
# #####*###*# ###*# #
#     #*****#   #*# #
# # ########### #*# #
# # #           #*# #
# # # # #########*# #
# #   #          **T#
#####################

There are more efficient ways to solve such kind of problems, this is just a simple demo.
"""

print "_________________________________________________________________\n"
print "Erdos demo:"
n = 600 # nodes number
nsteps = 30
kmax = 2.5
def ppr(pair): return str(pair[0]) + ":" + str(pair[1])
nodes = range(n)
g = Graph()
print "Nodes numeber (fixed) =", n
print "Arcs number (it changes) = k*n"
print "The pairs means  len(connected component):number of them"
ccv = []
for kk in xrange(nsteps):
    k = ( (0.0+kmax)/nsteps ) * kk
    g.createRandom(nodes, (k*n) / (n*(n+1)))
    cc = map(len, g.connectedComponents())
    auxd = {}
    for e in cc:
        if e in auxd:
            auxd[e] += 1
        else:
            auxd[e] = 1
    ccv.append( auxd )
    print "k,arcs=", str(round(k,2)) + ",", str(g.arcCount) + ":", " ".join(map(ppr, sorted(ccv[-1].items())))
print """\
\nThere is a phase transition in the graph. You can see that:
- for k<<0.5 there are lots of tiny connected component;
- when k=~0.5 the number of groups with different length is maximum;
- for k>0.5, in the graph it grows a single huge connected component."""
print "_________________________________________________________________"
print
print "An experiment, let's add random arcs to a graph:"
from random import randint
g = Graph()
side = 15 # 15
arcsToAdd = int(1.5*side)
nodeCount = side**2
g.create2dGrid(xrange(nodeCount), side, w=1, coords=True)
# g.plot2d() # Decomment this to see a 2D plot of the grid graph.
print "Create a square grid of side*side nodes, with side=", side
print """\
A square grid is a graph like this (this has a side=4):
 0---1---2---3
 |   |   |   |
 4---5---6---7
 |   |   |   |
 8---9--10--11
 |   |   |   |
12--13--14--15"""
print "Node and arc count (arcs are bidirectional pairs):", len(g), g.arcCount
print "Diameter and radius of the grid:", str(g.diameterRadius())[1:-1]
print "(The diameter of a graph is the length of the longest shortest path between any two nodes. The computation of the diameter is based on the allPairsShortestPaths, this is a O(n^3) algorithm, so there is a Delphi5 routine to compute it quickly, useful on Windows. On non-win it reverts using slow Python code."
print "A 2D grid graph with side*side nodes has a diameter of 2*(m-1). Adding just few random nodes, the diameter decreses a lot."
print "Adding", arcsToAdd, "new random directed arcs."
startArcCount = g.arcCount
while g.arcCount - startArcCount < arcsToAdd:
    g.addArc(randint(0,nodeCount-1), randint(0,nodeCount-1), w=1)
print "New diameter and radius:", str(g.diameterRadius())[1:-1]


"""
Textual output:

Adding random arcs to a graph:
Create a square grid of side*side nodes, with side= 15
A square grid is a graph like this (this has a side=4):
 0---1---2---3
 |   |   |   |
 4---5---6---7
 |   |   |   |
 8---9--10--11
 |   |   |   |
12--13--14--15
Node and arc count (arcs are bidirectional pairs): 225 840
Diameter and radius of the grid: 28, 14
(The diameter of a graph is the length of the longest shortest path between any two nodes. The computation of the diameter is based on the allPairsShortestPaths, this is a O(n^3) algorithm, so there is a Delphi5 routine to compute it quickly, useful on Windows. On non-win it reverts using slow Python code.
A 2D grid graph with side*side nodes has a diameter of 2*(m-1). Adding just few random nodes, the diameter decreses a lot.
Adding 22 new random directed arcs.
New diameter and radius: 18, 10

Create a square grid of side*side nodes, with side= 20
Node and arc count (arcs are bidirectional pairs): 400 1520
Diameter and radius of the grid: 38, 20
Adding 30 new random directed arcs.
New diameter and radius: 19, 11

Create a square grid of side*side nodes, with side= 25
Node and arc count (arcs are bidirectional pairs): 625 2400
Diameter and radius of the grid: 48, 24
Adding 37 new random directed arcs.
New diameter and radius: 25, 13


Create a square grid of side*side nodes, with side= 35
Node and arc count (arcs are bidirectional pairs): 1225 4760
Diameter and radius of the grid: 68, 34
Adding 52 new random directed arcs.
New diameter and radius: 30, 16
"""

print """_________________________________________________________________

Word Chains, Code Kata 19:
http://blogs.pragprog.com/cgi-bin/pragdave.cgi/Practices/Kata
Problem: build a chain of words, starting with one particular word and ending with another. Successive entries in the chain must all be real words, and each can differ from the previous word by just one letter. Words of a chain must all have the same length. Example, fro cat to dog:
  cat cot cog dog
This program must accept start and end words and, using words from the dictionary, return the shortest word chain between them.\n"""

def generateWordsGraph(words):
    """generateWordsGraph(words): return
    This function is quick enough for a sequence of 50000 words."""
    d, daw = {}, {}
    g = Graph()
    #g_o = g.o; g_i = g.i # For the faster alternative.

    for w in words:
        g.addNode(w)
        #g_o[w] = {} # Faster alternative.
        alternativeWords = [ w[:i]+"*"+w[i+1:] for i in xrange(len(w)) ]
        daw[w] = alternativeWords
        for wa in alternativeWords:
            if wa in d:
                d[wa].add(w)
            else:
                d[wa] = set([w])

    for w in words: # Probably this can be made faster.
        l = set()
        for wa in daw[w]:
            l.update(d[wa])
        for n in l:
            g._fastAddBiArc(n, w, 1) # 1 is the arc weight. This creates absent nodes too.
            #g_o[n][w] = 1; g_o[w][n] = 1 # Faster alternative.
    return g

import gc
try: import psyco # Import Psyco if available.
except ImportError: pass
else: psyco.bind(generateWordsGraph) # Psyco is useful for a huge word list.
words = """Bill ball call came care cold come face fact fall fast find fine fire five food
foot full game gave give gold good have held help hold home kind last life like line list
live mind name part past same some talk tall tell than that them then they told walk well
what when wild will wind""".split()

gc.disable() # This speeds up a lot the graph creation
g = generateWordsGraph(words)
gc.enable()

# Decomment this to save the graph in binary, useful to generate the word graph one time only:
# g.save("wordsGraph.pik")

# Decomment this line if you have used the fast alternative and you want to elaborate the graph
#   a lot, because the fast version of generateWordsGraph initializes the outbound arcs only:
# g._regenerate()

print "Some chains:"
for wp in ("help", "foot"), ("full", "home"):
    r = g.shortestPath(*wp)
    print len(r), " ".join(r), "\n"
for n in "gold", "will":
    print 'Nodes most distant from "' + str(n) + '" are:', g.mostDistantNodes(n), "\n"
print "A pseudo-peripheral node of the graph:", g.pseudoperipheralNode()

# Decomment this line to save the graph for DotViz:
# for n in g: g.delArc(n,n); g.saveDot(colorConnectedComponents=True)

print """_________________________________________________________________

Topological sort example:
"""
g = Graph()
multi = "belt,jacket jacket pants,belt,shoes shirt,belt,tie shoes socks,shoes tie,jacket undershorts,pants,shoes watch"
multi = [s.split(",") for s in multi.split(" ")]
g.addMulti(multi)
#g.saveDot("toposort_graph.dot") # Uncomment this to save the graph for graphViz.
print "Graph:", g.short()
print
print "Its Topological Sort:", " ".join(g.toposort())
print


print """_________________________________________________________________

springCoords example:
"""
g = Graph()
g.create2dGrid(range(1,10), 3, w=0, coords=False)
g.addNcube(dim=3, nodes="abcdefgh")
g.addPath("ABCEFGH", closed=True)
print "30 iterations of the spring model..."
result = g.springCoords(iterations=100, restart=True)
if result: print result
g.plot2d()
print "20 more iterations of the spring model on the same node positions..."
result = g.springCoords(iterations=20, restart=False)
if result: print result
g.plot2d()
print

print "\nGraph demo finished."