"""
graph_test.py  -- test for module graph.
By leonardo maffi
This testing code version: 1.8, Jun 30 2006.
See graph_docs.txt for documentation.

Testing conventions:
- Each function tests possibily one method of graph. Function names contain the method name(s)
  being tested.
- Each function name starts with "testXXX", XXX is a progressive number to assure the correct order.
- Working examples are as assert inside functions, not working examples (giving errors) are inside
  their docstrings as doctests.
- To disable a single test function, change its name, making it start with something different
  from "test".
"""

from graph import Graph
from time import clock
from random import random, randint, shuffle

exampleGraph = Graph({ 'A':{'C':5,'B':1,'D':8}, 'C':{'A':5,'B':3,'F':1}, 'D':{'A':8,'F':1},
                       'G':{'E':2,'F':1},'E':{'B':2,'G':2,'F':4}, 'B':{'A':1,'C':3,'E':2},
                       'F':{'C':1,'E':4,'D':1,'G':1} })
exampleGraphDraw = r"""
    (B)--2--(E)
    / \      |\
   1   3     | 2
  /     \    |  \
(A)--5--(C)  4  (G)
  \       \  |  /
   8       1 | 1
    \       \|/
    (D)--1--(F)
"""


def test001_basic1():
    g = Graph()
    g.addNode(1)
    g.addNode(2)
    g.addNode(3)
    g.addArc(1,2, 0)
    g.addArc(2,3, 0)
    g.addArc(3,1, 0)
    g.addArc(3,2, 0)
    assert g.o == {1: {2: 0}, 2: {3: 0}, 3: {1: 0, 2: 0}}
    assert g.i == {1: {3: 0}, 2: {1: 0, 3: 0}, 3: {2: 0}}
    assert g.arcCount == 4


def test002_short1():
    g = Graph()
    nodeCount = 100
    for n in xrange(nodeCount):
        g.addNode(n)
    assert g.short() == "  ".join(map(str, range(nodeCount)))


def test003_basic2():
    nodesn = 50

    # Create complete graph with shuffled commands
    g = Graph()
    assert g.arcCount == 0
    nodes = range(nodesn)
    arcs = [(n1,n2) for n1 in nodes for n2 in nodes]
    shuffle(arcs)
    if nodesn < 7: # Debugging print just for smaller graphs
        print arcs
        print
    for n1,n2 in arcs:
        g.addArc(n1, n2, 0)
    if nodesn < 7:
        print g.short()
        print

    # assert that it's complete
    def seq(i):
        return str(i) + ">" + ",".join(map(str, xrange(nodesn)))
    assert g.short(all=True) == "  ".join(seq(i) for i in xrange(nodesn))
    assert g.arcCount == nodesn**2 + nodesn

    # remove arcs util the graph is a circle
    arcs2 = [(n1,n2) for n1 in nodes for n2 in nodes if n1 != ((n2-1) % nodesn)]
    shuffle(arcs2)
    if nodesn < 7:
        print arcs2
        print
    for n1,n2 in arcs2:
        g.delArc(n1,n2)
    if nodesn < 7:
        print g.short()
        print

    # assert that it's a circle
    def seq(i):
        return str(i) + ">" + str((i+1) % nodesn)
    assert g.short(all=True) == "  ".join(seq(i) for i in xrange(nodesn))
    assert g.arcCount == nodesn


def test004_arcs_xarcs():
    g = Graph()
    nn = 4
    for n1 in xrange(nn):
        for n2 in xrange(nn):
            g.addArc(n1,n2, 0)
    arcs = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),
            (3,2),(3,3)]
    assert sorted(g.arcs()) == arcs
    assert sorted(g.xarcs()) == arcs


def test005_addClique1_clear():
    g = Graph()
    g.addClique([1])
    assert repr(g) == "Graph({1: {}})"
    g = Graph({1:{}})
    g.addClique([2])
    assert repr(g) == "Graph({1: {}, 2: {}})" or repr(g) == "Graph({2: {}, 1: {}})"

    g.clear()
    assert (g.i == g.o == g.nodeData == {}) and g.arcCount==0 # clear test
    g.addClique(range(10), nodeData="node", w=0)
    assert g.arcCount == 90
    assert g.short() == "0>1,2,3,4,5,6,7,8,9  1>0,2,3,4,5,6,7,8,9  2>0,1,3,4,5,6,7,8,9  3>0,1,2,4,5,6,7,8,9  4>0,1,2,3,5,6,7,8,9  5>0,1,2,3,4,6,7,8,9  6>0,1,2,3,4,5,7,8,9  7>0,1,2,3,4,5,6,8,9  8>0,1,2,3,4,5,6,7,9  9>0,1,2,3,4,5,6,7,8"
    assert str(g) == "0-1,2,3,4,5,6,7,8,9  1-2,3,4,5,6,7,8,9  2-3,4,5,6,7,8,9  3-4,5,6,7,8,9  4-5,6,7,8,9  5-6,7,8,9  6-7,8,9  7-8,9  8-9"

    g.clear()
    assert (g.i == g.o == g.nodeData == {}) and g.arcCount==0 # clear test

    g.addClique(range(10), nodeData="node", w=0, loops=True)
    assert g.arcCount == 110
    assert g.short() == "0>0,1,2,3,4,5,6,7,8,9  1>0,1,2,3,4,5,6,7,8,9  2>0,1,2,3,4,5,6,7,8,9  3>0,1,2,3,4,5,6,7,8,9  4>0,1,2,3,4,5,6,7,8,9  5>0,1,2,3,4,5,6,7,8,9  6>0,1,2,3,4,5,6,7,8,9  7>0,1,2,3,4,5,6,7,8,9  8>0,1,2,3,4,5,6,7,8,9  9>0,1,2,3,4,5,6,7,8,9"
    assert str(g) == "0-0,1,2,3,4,5,6,7,8,9  1-1,2,3,4,5,6,7,8,9  2-2,3,4,5,6,7,8,9  3-3,4,5,6,7,8,9  4-4,5,6,7,8,9  5-5,6,7,8,9  6-6,7,8,9  7-7,8,9  8-8,9  9-9"

    g.clear()
    assert (g.i == g.o == g.nodeData == {}) and g.arcCount==0 # clear test
    g.addNode(1)
    g.addNode(2)
    g.addNode(3)
    g.addArc(1,2)
    g.addArc(2,3)
    g.addArc(3,1)
    g.addArc(3,2)
    assert g.short() == "1>2  2>3  3>1,2"
    g.addClique((2,3,4,5), nodeData="node", w=0, loops=False)
    assert g.arcCount == 14
    assert g.short() == "1>2  2>3,4,5  3>1,2,4,5  4>2,3,5  5>2,3,4"
    assert str(g) == "1>2  2>3,4,5  3>1,2,4,5  4>2,3,5  5>2,3,4"
    h = Graph({1:{2:None},2:{3:0,4:0,5:0},3:{1:None,2:0,4:0,5:0},4:{2:0,3:0,5:0},5:{2:0,3:0,4:0}},{2:'node',3:'node',4:'node',5:'node'})
    assert g == h


def test006_copy():
    g1 = Graph({1:{2:0}, 2:{3:0}, 3:{1:0,2:0,3:0}})
    g1short = g1.short()
    g2 = g1.copy()
    assert g1.short() == g2.short()


def test007_save_load():
    import os
    g = Graph()
    g.addNode(" ")
    g.addClique(range(30), w=0, nodeData="node")
    g.addNode("\n\t\b1", nodeData=("\n\t\b",22))
    g.addNode("\n\t\b2", nodeData={"\n\t\b":22})
    fileName = "temporary_file.pik"
    g.save(fileName)
    h = Graph()
    h.load(fileName)
    assert h.i == g.i
    assert h.o == g.o
    assert h.arcCount == g.arcCount
    os.remove(fileName)


def test008_textSave_textLoad():
    import os
    g = Graph()
    g.addNode(" ")
    g.addClique(range(30), w=0, nodeData="node")
    g.addNode("\n\t\b1", nodeData=("\n\t\b",22))
    g.addNode("\n\t\b2", nodeData={"\n\t\b":22})
    fileName = "temporary_file.txt"
    g.textSave(fileName)
    h = Graph()
    h.textLoad(fileName)
    assert h.i == g.i
    assert h.o == g.o
    assert h.arcCount == g.arcCount
    os.remove(fileName)


def test009_eq_diff():
    g1 = Graph()
    g1.addClique("abcd", w=0)
    def seq(i):
        return str(i) + ">" + ",".join(s for s in "abcd" if s!=i)
    assert g1.short() == "  ".join(seq(i) for i in "abcd")

    g2 = Graph()
    g2.addClique(list("abcd"), w=0)
    assert g2.short() == "  ".join(seq(i) for i in "abcd")

    assert g1 == g2
    assert not(g1 != g2)
    g2.addNode("a", nodeData="1")
    assert g2.short() == "a>b,c,d  b>a,c,d  c>a,b,d  d>a,b,c"
    assert not(g1 == g2)
    assert g1 != g2


def test010_len_order():
    g = Graph()
    n = 50
    for i in xrange(n):
        g.addNode(randint(0,1000000), nodeData="node!")
    assert n == len(g)
    assert n == g.order()
    assert n == len(g.o)
    assert n == len(g.i)
    assert n == len(g.nodeData)


def test011_popNode_len():
    """
    >>> g = Graph()
    >>> g.addNode(1)
    >>> g.popNode()
    1
    >>> g.popNode()
    Traceback (most recent call last):
    ...
    IndexError: No items to select.
    """
    g = Graph()
    assert len(g) == 0
    s = "abcdef"
    g.addClique(s, w=0)
    assert str(g) == "a-b,c,d,e,f  b-c,d,e,f  c-d,e,f  d-e,f  e-f"
    poppedNodes = []
    for i,c in enumerate(s):
        poppedNodes.append( g.popNode() )
        assert i+1 == len(s)-len(g)
    assert g == Graph()
    assert len(s) == len(poppedNodes)
    assert set(poppedNodes) == set(s)


def test012_DFS1_BFS1_xDFS1_xDFS1_aview1_wview1():
    """
    >>> g = Graph()
    >>> g.DFS("a")
    Traceback (most recent call last):
    ...
        assert startNode in self_a
    AssertionError
    """
    g = Graph( {'a':{'c':0,'b':0}, 'c':{'e':0}, 'b':{'e':0,'d':0,'f':0}, 'e':{'f':0}, 'd':{'f':0},
                'g':{}, 'f':{'g':0}} )
    assert g.short() == "a>b,c  b>d,e,f  c>e  d>f  e>f  f>g  g"
    assert g.short(out=False) == "a  b<a  c<a  d<b  e<b,c  f<b,d,e  g<f"
    a = """\
Adjacency matrix (1=arc present, 2=self loop, "." or 0=absent):
     a b c d e f g
a: | . 1 1 . . . . |
b: | . . . 1 1 1 . |
c: | . . . . 1 . . |
d: | . . . . . 1 . |
e: | . . . . . 1 . |
f: | . . . . . . 1 |
g: | . . . . . . . |"""
    assert g.aview() == a

    w = """\
Adjacency Matrix of weights (values = arc weights, "." = absent arc):
     a b c d e f g
a: | . 0 0 . . . . |
b: | . . . 0 0 0 . |
c: | . . . . 0 . . |
d: | . . . . . 0 . |
e: | . . . . . 0 . |
f: | . . . . . . 0 |
g: | . . . . . . . |"""
    assert g.wview() == w
    assert g.DFS("a", sort=True) == ['a', 'b', 'd', 'f', 'g', 'e', 'c']
    assert g.DFS("b", sort=True) == ['b', 'd', 'f', 'g', 'e']
    assert g.BFS("a", sort=True) == ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    assert g.BFS("b", sort=True) == ['b', 'd', 'e', 'f', 'g']
    assert list(g.xDFS("a", sort=True)) == ['a', 'b', 'd', 'f', 'g', 'e', 'c']
    assert list(g.xDFS("b", sort=True)) == ['b', 'd', 'f', 'g', 'e']
    assert list(g.xBFS("a", sort=True)) == ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    assert list(g.xBFS("b", sort=True)) == ['b', 'd', 'e', 'f', 'g']


def test013_DFS2_BFS2_xDFS2_xDFS2_aview2_wview2():
    g = Graph()
    g.addClique("abcdefg", w=0)
    assert g.short() == "a>b,c,d,e,f,g  b>a,c,d,e,f,g  c>a,b,d,e,f,g  d>a,b,c,e,f,g  e>a,b,c,d,f,g  f>a,b,c,d,e,g  g>a,b,c,d,e,f"
    assert g.short(out=False) == "a<b,c,d,e,f,g  b<a,c,d,e,f,g  c<a,b,d,e,f,g  d<a,b,c,e,f,g  e<a,b,c,d,f,g  f<a,b,c,d,e,g  g<a,b,c,d,e,f"
    a = """\
Adjacency matrix (1=arc present, 2=self loop, "." or 0=absent):
     a b c d e f g
a: | . 1 1 1 1 1 1 |
b: | 1 . 1 1 1 1 1 |
c: | 1 1 . 1 1 1 1 |
d: | 1 1 1 . 1 1 1 |
e: | 1 1 1 1 . 1 1 |
f: | 1 1 1 1 1 . 1 |
g: | 1 1 1 1 1 1 . |"""
    assert g.aview() == a

    w = """\
Adjacency Matrix of weights (values = arc weights, "." = absent arc):
     a b c d e f g
a: | . 0 0 0 0 0 0 |
b: | 0 . 0 0 0 0 0 |
c: | 0 0 . 0 0 0 0 |
d: | 0 0 0 . 0 0 0 |
e: | 0 0 0 0 . 0 0 |
f: | 0 0 0 0 0 . 0 |
g: | 0 0 0 0 0 0 . |"""
    assert g.wview() == w
    assert g.DFS("a", sort=True) == ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    assert g.DFS("b", sort=True) == ['b', 'a', 'c', 'd', 'e', 'f', 'g']
    assert g.BFS("a", sort=True) == ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    assert g.BFS("b", sort=True) == ['b', 'a', 'c', 'd', 'e', 'f', 'g']
    assert list(g.xDFS("a", sort=True)) == ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    assert list(g.xDFS("b", sort=True)) == ['b', 'a', 'c', 'd', 'e', 'f', 'g']
    assert list(g.xBFS("a", sort=True)) == ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    assert list(g.xBFS("b", sort=True)) == ['b', 'a', 'c', 'd', 'e', 'f', 'g']


def test014_DFS3_BFS3_xDFS3_xDFS3_aview3_wview3_addPath1():
    g = Graph()
    g.addPath("abcdefg", w=0)
    assert g.short() == "a>b  b>c  c>d  d>e  e>f  f>g  g"
    assert g.short(out=False) == "a  b<a  c<b  d<c  e<d  f<e  g<f"
    a = """\
Adjacency matrix (1=arc present, 2=self loop, "." or 0=absent):
     a b c d e f g
a: | . 1 . . . . . |
b: | . . 1 . . . . |
c: | . . . 1 . . . |
d: | . . . . 1 . . |
e: | . . . . . 1 . |
f: | . . . . . . 1 |
g: | . . . . . . . |"""
    assert g.aview() == a

    w = """\
Adjacency Matrix of weights (values = arc weights, "." = absent arc):
     a b c d e f g
a: | . 0 . . . . . |
b: | . . 0 . . . . |
c: | . . . 0 . . . |
d: | . . . . 0 . . |
e: | . . . . . 0 . |
f: | . . . . . . 0 |
g: | . . . . . . . |"""
    assert g.wview() == w
    assert g.DFS("a", sort=True) == ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    assert g.DFS("b", sort=True) == ['b', 'c', 'd', 'e', 'f', 'g']
    assert g.BFS("a", sort=True) == ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    assert g.BFS("b", sort=True) == ['b', 'c', 'd', 'e', 'f', 'g']
    assert list(g.xDFS("a", sort=True)) == ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    assert list(g.xDFS("b", sort=True)) == ['b', 'c', 'd', 'e', 'f', 'g']
    assert list(g.xBFS("a", sort=True)) == ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    assert list(g.xBFS("b", sort=True)) == ['b', 'c', 'd', 'e', 'f', 'g']


def test015_DFS4_BFS4_xDFS4_xDFS4():
    g = exampleGraph.copy()
    assert g.short() == "A>B,C,D  B>A,C,E  C>A,B,F  D>A,F  E>B,F,G  F>C,D,E,G  G>E,F"
    assert g.short(False) == "A<B,C,D  B<A,C,E  C<A,B,F  D<A,F  E<B,F,G  F<C,D,E,G  G<E,F"

    a = """\
Adjacency matrix (1=arc present, 2=self loop, "." or 0=absent):
     A B C D E F G
A: | . 1 1 1 . . . |
B: | 1 . 1 . 1 . . |
C: | 1 1 . . . 1 . |
D: | 1 . . . . 1 . |
E: | . 1 . . . 1 1 |
F: | . . 1 1 1 . 1 |
G: | . . . . 1 1 . |"""
    assert g.aview() == a

    w = """\
Adjacency Matrix of weights (values = arc weights, "." = absent arc):
     A B C D E F G
A: | . 1 5 8 . . . |
B: | 1 . 3 . 2 . . |
C: | 5 3 . . . 1 . |
D: | 8 . . . . 1 . |
E: | . 2 . . . 4 2 |
F: | . . 1 1 4 . 1 |
G: | . . . . 2 1 . |"""
    assert g.wview() == w

    l = """\
Adjacency List (node: outbound neighbours:weights ):
A: B:1 C:5 D:8
B: A:1 C:3 E:2
C: A:5 B:3 F:1
D: A:8 F:1
E: B:2 F:4 G:2
F: C:1 D:1 E:4 G:1
G: E:2 F:1"""
    assert g.lview() == l

    assert g.DFS("A", True) == ['A', 'B', 'C', 'F', 'D', 'E', 'G']
    assert g.BFS("A", True) == ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    assert g.BFS("C", True) == ['C', 'A', 'B', 'F', 'D', 'E', 'G']
    assert list(g.DFS("A", True)) == ['A', 'B', 'C', 'F', 'D', 'E', 'G']
    assert list(g.BFS("A", True)) == ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    assert list(g.BFS("C", True)) == ['C', 'A', 'B', 'F', 'D', 'E', 'G']


'''
# This doctest doesn't work, I don't know why.
def test015b___getattr__():
    """
    >>> g = Graph()
    >>> g.connectedComp()
    Traceback (most recent call last):
    ...
    AttributeError: method 'connectedcomp' not found.
    Most similar named ones: connectedComponents, isConnected, createRandom, undirectedArcs, isUndirectedArc
    <BLANKLINE>
    connectedComponents(): return the list of the Connected Components of the graph.
    isConnected(): return true if the graph is connected.
    createRandom(nodes, arcProbability, nodeData=None, w=None, loops=False, bi=False):
    undirectedArcs(): return an unsorted list of all the undirected arcs of the graph.
    isUndirectedArc(n1, n2): return True if between two nodes there are two arcs with
    """
    pass
'''


def test016_fromMulti_fromArcs():
    g = Graph()
    g.addMulti( ((1,2,6),2,(3,1),(1,6),[],[7]) )
    assert g.short() == "1>2,6  2  3>1  6  7"
    h = Graph()
    h.addArcs( [(1,2,5),(1,6),(3,1,None),(2,3,"a"),7,[],(8,)] )
    assert str(h) == "1>2,6  2>3  3>1  6  7  8"


def test017_degreeDict1():
    n = 20
    g = Graph()
    g.addClique(range(n), w=0, loops=False)
    if n<10:
        print g.short()
        print g.short(False)
        print g
        print
    #t1 = clock()
    for x in range(100):
        d = g.degreeDict()
    #t2 = clock()
    #print round(t2-t1,3)
    if n<10:
        print d
    for e in d.itervalues():
        assert e == 2*(n-1)


def test018_add1_intersection1():
    g = Graph()
    g.addPath(range(10), w=1, nodeData="n")
    #print g.mview()
    #print g.wview()
    h = Graph()
    h.addPath(['f', 'e', 'd', 'c', 'b', 'a'], w=2, nodeData="n", closed=True)
    #print h.mview()
    #print h.wview()
    g.addUpdate(h)
    assert str(g) == "0>1  1>2  2>3  3>4  4>5  5>6  6>7  7>8  8>9  9  a>f  b>a  c>b  d>c  e>d  f>e"
    #print g.aview()
    #print g.wview()
    i = g.intersection(h)
    assert str(i) == "a>f  b>a  c>b  d>c  e>d  f>e"
    #print i.aview()
    #print i.wview()
    assert i == h
    i = h.intersection(g)
    assert str(i) == "a>f  b>a  c>b  d>c  e>d  f>e"
    #print i.aview()
    #print i.wview()
    assert i == h


def test019_add2_intersection2():
    nn = 50
    na = 200
    g1 = Graph()
    for i in xrange(na):
        g1.addArc(randint(0,nn-1), randint(0,nn-1), w=0)
    g2 = Graph()
    for i in xrange(na):
        g2.addArc(randint(0,nn-1), randint(0,nn-1), w=0)
    g3 = g1.intersection(g2)
    g4 = g2.intersection(g1)
    assert g3 == g4
    #print g3.short()
    g3 = g1.intersection(g2)
    g4 = g1.copy()
    g4.addUpdate(g2)
    assert g4.intersection(g3) == g3


def test020_startNodes1_degreeDict2_toposort1():
    g = Graph()
    g.addArcs([ (1,2),(2,3),(3,4) ])
    assert g.short(out=True) == "1>2  2>3  3>4  4"
    ts = g.toposort() == [1, 2, 3, 4]

    g = Graph()
    g.addArcs([ (1,2),(2,3),(3,2) ])
    assert g.short(out=True) == "1>2  2>3  3>2"
    assert g.toposort() == [1]


def test021_startNodes2_degreeDict3_toposort2():
    g = Graph()
    multi = "belt,jacket jacket pants,belt,shoes shirt,belt,tie shoes socks,shoes tie,jacket undershorts,pants,shoes watch"
    multi = [s.split(",") for s in multi.split(" ")]
    g.addMulti(multi)
    #g.saveDot() # Uncomment this to save the graph for graphViz.
    assert g.short() == "belt>jacket  jacket  pants>belt,shoes  shirt>belt,tie  shoes  socks>shoes  tie>jacket  undershorts>pants,shoes  watch"
    assert g.short(False) == "belt<pants,shirt  jacket<belt,tie  pants<undershorts  shirt  shoes<pants,socks,undershorts  socks  tie<shirt  undershorts  watch"
    assert g.startNodes() == set(['undershorts', 'watch', 'shirt', 'socks'])
    assert g.degreeDict() == {'shoes':3,'shirt':2,'watch':0,'socks':1,'jacket':2,'undershorts':2,'tie':2,'belt':3,'pants':3}
    ts = g.toposort()
    assert len(g) == len(ts) # Otherwise g contains one or more loops.
    # The following is just one of the correct topological sorts of the graph g:
    assert ts == ['shirt', 'watch', 'socks', 'undershorts', 'tie', 'pants', 'shoes', 'belt', 'jacket']


def test022_connectedComponents1():
    g_drawing = r"""
    a --> b --> c
    ^     |     ^
    |     |     |
    |     v     |
    d <-- e <-- f
    """
    # print g_drawing
    g = Graph()
    g.addMulti([ ("a","b"),("b","c","e"),"c",("d","a"),("e","d"),("f","e") ])
    assert str(g) == "a>b  b>c,e  c  d>a  e>d  f>e"
    assert g.connectedComponents() == [['a', 'b', 'd', 'c', 'e', 'f']]


def test023_isUndirected():
    g1 = Graph( {1:{3:1, 4:0}, 2:{1:0}, 3:{1:2}, 4:{}, 5:{5:3}} )
    assert g1.short(showw=True) == "1>3/1,4/0  2>1/0  3>1/2  4  5>5/3"
    assert not g1.isUndirected()
    g2 = Graph( {1:{2:0,3:1,4:0}, 2:{1:0}, 3:{1:2}, 4:{1:0}, 5:{5:3}} )
    assert g2.short(showw=True) == "1>2/0,3/1,4/0  2>1/0  3>1/2  4>1/0  5>5/3"
    assert not g2.isUndirected()
    g3 = Graph( {1:{2:0,3:1,4:0}, 2:{1:0}, 3:{1:1}, 4:{1:0}, 5:{5:3}} )
    assert g3.short(showw=True) == "1>2/0,3/1,4/0  2>1/0  3>1/1  4>1/0  5>5/3"
    assert g3.isUndirected()

    g = Graph()
    g.addArcs( ((randint(0,800),randint(0,800)) for i in xrange(600)) )
    assert not g.isUndirected()
    g.makeUndirected()
    assert g.isUndirected()


def test024_integerw():
    xn = xrange(30)
    g = Graph()
    assert g.integerw() # True for empty graph.
    assert g.realw() # True for empty graph.
    g.addClique(xn, w=1)
    assert g.integerw()
    assert g.realw()
    g.addClique(xn, w=1.1)
    assert not g.integerw()
    assert g.realw()
    g.addClique(xn, w="a")
    assert not g.integerw()
    assert not g.realw()


def test025_viewStats(): # This is a fragile test
    g = Graph()
    g.addClique(xrange(50), w=1.1)
    g.addPath("abcdefghilmnopqrsetuvxywz", w=1.2, closed=True)
    stats = """\
Graph stats:
Number of nodes: 74
Number of arcs: 2474
Average number of outbound (or inbound) neighbours: 33.4324324324
Number of node data: 0
Indirected graph: False
Number of loops: 0
All arcs have int or long weights: False
All arcs have int, long or float weights: True
Number of connected components: 2
Density: 0.445765765766"""
    assert stats == g.viewStats()


def test026_connectedComponents1():
    g = Graph()
    assert g.connectedComponents() == []
    a = [ (1,2),(2,3),(3,1),(1,3),(4,5),(8,7) ]
    g.addArcs(a)
    assert g.short() == "1>2,3  2>3  3>1  4>5  5  7  8>7"
    cc = g.connectedComponents()
    r = [[1, 2, 3], [4, 5], [7, 8]]
    assert len(cc) == len(r)
    lcc = map(len, cc)
    lr = map(len, r)
    assert len(lcc) == len(lr)
    assert set(lcc) == set(lr)
    assert set(map(frozenset, r)) == set(map(frozenset, cc))

    g.clear()
    nodes = range(30)
    g.addClique(nodes)
    cc = g.connectedComponents()
    assert len(cc) == 1
    assert set(cc[0]) == set(nodes)


def test027_shortestPath1():
    g = exampleGraph.copy()
    assert g.short() == "A>B,C,D  B>A,C,E  C>A,B,F  D>A,F  E>B,F,G  F>C,D,E,G  G>E,F"
    assert g.DFS("A", sort=True) == ['A', 'B', 'C', 'F', 'D', 'E', 'G']
    assert g.BFS("A", sort=True) == ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    assert g.BFS("C", sort=True) == ['C', 'A', 'B', 'F', 'D', 'E', 'G']
    assert g.shortestPath("A", "G") == ['A', 'B', 'E', 'G']
    assert g.shortestPath("D", "E") == ['D', 'F', 'G', 'E']


def test028_allPairsShortestPath1_shortestPath2():
    def normalDict(distm):
        result = {}
        for n1 in nodes:
            row = distm[1].index(n1)
            for n2 in nodes:
                column = distm[1].index(n2)
                result[ (distm[1][row], distm[1][column]) ] = distm[0][row][column]
        return result

    g = exampleGraph.copy()
    assert g.short() == "A>B,C,D  B>A,C,E  C>A,B,F  D>A,F  E>B,F,G  F>C,D,E,G  G>E,F"
    nodes = ['A','B','C','D','E','F','G']
    for n in nodes: g.addLoop(n, w=0) # Self-loops added for the test with weights=True.
    assert set(g.nodes()) == set(nodes)
    assert len(g.nodes()) == len(nodes)
    r1 = ([[0,4,1,3,6,5,5],[4,0,3,4,2,2,1],[1,3,0,2,5,4,4],[3,4,2,0,4,2,3],[6,2,5,4,0,2,1],[5,2,4,2,2,0,1],[5,1,4,3,1,1,0]],['A','C','B','E','D','G','F'])
    r1d = normalDict(r1)
    apsp1 = g.allPairsShortestPaths()
    apsp1d = normalDict(apsp1)
    assert apsp1d == r1d
    sp1 = {}
    for n1 in nodes:
        for n2 in nodes:
            sumpw = g.sumPathw(g.shortestPath(n1, n2, weights=True))
            if sumpw == None: # Because sumPathw[[node]] ==> None
                sp1[(n1,n2)] = 0
            else:
                sp1[(n1,n2)] = sumpw
    assert sp1 == r1d

    g = exampleGraph.copy()
    r2 = ([[0,1,1,2,1,3,2],[1,0,1,2,2,2,1],[1,1,0,1,2,2,2],[2,2,1,0,2,1,1],[1,2,2,2,0,2,1],[3,2,2,1,2,0,1],[2,1,2,1,1,1,0]],['A','C','B','E','D','G','F'])
    r2d = normalDict(r2)
    apsp2 = g.allPairsShortestPaths(weights=False)
    apsp2d = normalDict(apsp2)
    assert apsp2d == r2d
    sp2 = {}
    for n1 in nodes:
        for n2 in nodes:
            sp2[(n1,n2)] = len(g.shortestPath(n1, n2, weights=False))-1
    assert sp2 == r2d


def test029__recountArcs1_regenerate1():
    from random import randint
    nn = 40
    na = int(nn * 40)

    nn1 = nn - 1
    g1 = Graph()
    for i in xrange(na):
        g1.addArc(randint(0, nn1), randint(0, nn1), w=1)
    g2 = g1.copy()
    g1.arcCount = 0
    g1._recountArcs()
    assert g1.arcCount == g2.arcCount
    g1.i = {}
    g1.arcCount = 0
    g1._regenerate()
    assert g1 == g2


def test030__rawDelNode1__cleanDeadArcs1():
    n = 20
    n2 = n*2
    g1 = Graph()
    g1.addClique(xrange(n2))
    g2 = g1.copy()
    for i in xrange(n):
        g2._rawDelNode(i)
    g2._cleanDeadArcs()
    for i in xrange(n):
        g1.delNode(i)
    assert g1 == g2


def test031_createRandom1():
    r10 = range(10)
    g1 = Graph()

    g1.createRandom([], 0, w=1, loops=False)
    assert g1 == Graph()

    g1.clear()
    g1.createRandom([0], 0, w=1, loops=False)
    assert g1 == Graph({0:{}})

    g1.clear()
    g1.createRandom(r10, -1, w=1, loops=False, nodeData=2)
    g2 = Graph()
    g2.addNodes(r10, nodeData=2)
    assert g1 == g2

    g1.clear()
    g1.createRandom(r10, 0, w=1, loops=False)
    g2.clear()
    g2.addNodes(r10)
    assert g1 == g2

    g1.clear()
    g1.createRandom(r10, 2, w=1, loops=False)
    g2.clear()
    g2.addClique(r10, w=1, loops=False)
    assert g1 == g2

    g1.clear()
    g1.createRandom(r10, 2, w=1, loops=True)
    g2.clear()
    g2.addClique(r10, w=1, loops=True)
    assert g1 == g2

    g1.clear()
    n = 50
    g1.createRandom(range(50), 0.9, w=1, loops=True)
    assert g1.arcCount < n*(n+1) # Probabilistic assert
    assert g1.arcCount > (n**2)*0.6 # Probabilistic assert

    ac = g1.arcCount
    g1._recountArcs()
    assert ac == g1.arcCount


def test032_randomw_makeUndirected_isUndirected():
    g = Graph({0:{1:5,2:5,3:6,4:4,5:1},1:{0:3,2:4,3:5,4:3,5:3},2:{0:2,1:2,3:5,4:3,5:5},3:{0:6,1:1,2:1,4:3,5:3},4:{0:3,1:4,2:6,3:6,5:6},5:{0:2,1:3,2:4,3:4,4:3}})
    def reconcile(w1, w2):
        return (w1+w2)/2.0 # Average of two.
    g.makeUndirected(reconcile)
    assert g == Graph({0:{1:4.0,2:3.5,3:6,4:3.5,5:1.5},1:{0:4.0,2:3.0,3:3.0,4:3.5,5:3},2:{0:3.5,1:3.0,3:3.0,4:4.5,5:4.5},3:{0:6,1:3.0,2:3.0,4:4.5,5:3.5},4:{0:3.5,1:3.5,2:4.5,3:4.5,5:4.5},5:{0:1.5,1:3,2:4.5,3:3.5,4:4.5}})
    assert g.isUndirected()

    n = 30
    g = Graph()
    g.createRandom(range(n), (n**2)*0.6, w=1)
    g.randomw( lambda:randint(1,6) )
    def reconcile(w1, w2):
        return (w1+w2)/2.0 # Average of two.
    g.makeUndirected(reconcile)
    assert g.isUndirected()


def test033_addArcs():
    arcs = "ACABADCACBCFBABCBEEBEGEFDADFGEGFFCFEFDFG"
    g1 = Graph()
    g1.addArcs(arcs, w=None, bi=False, paired=False)
    g2 = exampleGraph.copy()
    g2.randomw(lambda:None)
    assert g2 == g1
    arcs2 = "A,B,C,D B,C,E C,F D,F E,F,G F,G".split(" ")
    g3 = Graph()
    g3.addMulti((a.split(",") for a in arcs2), w=None, bi=True)
    assert g3 == g1


def test034_reverseArc1():
    g1 = Graph()
    g1.addArcs([ (0,1),(1,2),(2,3) ])
    g1.addArcs([ (3,4),(4,0),(1,4) ], bi=True)
    g1.nodeData = {0:(2,5),1:(6,3),2:(6,-1),3:(-2,-1),4:(-2,3)}
    assert str(g1) == "0>1,4  1>2,4  2>3  3>4  4>0,1,3"
    g2 = g1.copy()
    for n1,n2 in g2.arcs():
        g2.reverseArc(n1, n2)
    assert str(g2) == "0>4  1>0,4  2>1  3>2,4  4>0,1,3"
    assert g1.nodeData == g2.nodeData
    g3 = g2.copy()
    for n1,n2 in g3.arcs():
        g3.reverseArc(n1, n2)
    assert g1 == g3

    g1.clear()
    n = 40
    g1.createRandom(xrange(n), n*3)
    for n in xrange(1000):
        g1.nodeData[n] = (randint(0,199), randint(0,199))
    g2 = g1.copy()
    for n1,n2 in g1.arcs():
        g1.reverseArc(n1, n2)
    for n1,n2 in g1.arcs():
        g1.reverseArc(n1, n2)
    assert g1 == g2


def test035_renameNode1():
    nn = 40
    g1 = Graph()
    g1.createRandom(range(nn), 0.3)
    g2 = g1.copy()
    for n in g1.nodes():
        g1.renameNode(n, str(n))
    for n in g1.nodes():
        g1.renameNode(n, int(n))
    assert g1 == g2

    g = Graph()
    g.addBiArc(0, 1)
    g.renameNode(0, "A")
    assert g.i == g.o == {'A': {1: None}, 1: {'A': None}}

    g.clear()
    g.addArcs([ (0,1),(1,2),(0,2) ])
    g.renameNode(0, str(0))
    assert str(g) == "1>2  2  0>1,2"
    assert g.o == {1: {2: None}, 2: {}, '0': {1: None, 2: None}}
    assert g.i == {1: {'0': None}, 2: {1: None, '0': None}, '0': {}}

    g.clear()
    g.addArcs([ (0,1),(1,2),(0,2) ])
    for i in [0,1,2]:
        g.renameNode(i, str(i))
    assert str(g) == "0>1,2  1>2  2"
    assert g.o == {'1': {'2': None}, '2': {}, '0': {'1': None, '2': None}}
    assert g.i == {'1': {'0': None}, '2': {'1': None, '0': None}, '0': {}}

    g.clear()
    g.addNode(1, (1,4) )
    g.addNode(2, (4,4) )
    g.addNode(3, (1,1) )
    g.addNode(4, (4,1) )
    g.addBiArc(1, 2, "a")
    g.addBiArc(1, 4, "b")
    g.addArc(4, 3, "c")
    g.addArc(4, 2, "d")
    g.renameNode(4, "4")
    assert g.o == {1: {2: 'a', '4': 'b'}, 2: {1: 'a'}, 3: {}, '4': {1: 'b', 2: 'd', 3: 'c'}}
    assert g.i == {1: {2: 'a', '4': 'b'}, 2: {1: 'a', '4': 'd'}, 3: {'4': 'c'}, '4': {1: 'b'}}
    assert g.arcCount == 6
    assert g.nodeData == {1: (1, 4), 2: (4, 4), 3: (1, 1), '4': (4, 1)}


def test036_sumPathw1():
    g = exampleGraph.copy()
    assert g.sumPathw("ABCFG") == 6
    assert g.sumPathw("BEFG") == 7
    assert g.sumPathw("ABC") == 4
    assert g.sumPathw("A") == None
    assert g.sumPathw([]) == None
    assert g.sumPathw("Z") == None


def test037_euclidify1_isEmbedded1():
    g = Graph()
    l = [(1,2),(2,3),(3,4),(4,5),(5,1),(2,5)] # Little house.
    g.addArcs(l, w=0)
    pl = ( (2,5),(6,3),(6,-1),(-2,-1),(-2,3) ) # Node 2D coordinates.
    for i,p in enumerate(pl):
        g.nodeData[i+1] = p
    assert g.isEmbedded()
    assert g == Graph({1:{2:0},2:{3:0,5:0},3:{4:0},4:{5:0},5:{1:0}},{1:(2,5),2:(6,3),3:(6,-1),4:(-2,-1),5:(-2,3)})
    g.euclidify2d()
    assert str(g) == "1>2  2>3,5  3>4  4>5  5>1"
    assert g.nodeData == {1: (2, 5), 2: (6, 3), 3: (6, -1), 4: (-2, -1), 5: (-2, 3)}
    assert [round(g.getArcw(*arc),4) for arc in l] == [4.4721000000000002, 4.0, 8.0, 4.0, 4.4721000000000002, 8.0]


def test038_complement1_addPath1():
    g = Graph( {1:{2:0},2:{3:0,5:0},3:{4:0},4:{5:0},5:{1:0}}, # Little house.
               {1:(2,5),2:(6,3),3:(6,-1),4:(-2,-1),5:(-2,3)} )
    g.complement(w=0)
    assert g == Graph({1:{1:0,3:0,4:0,5:0},2:{1:0,2:0,4:0},3:{1:0,2:0,3:0,5:0},4:{1:0,2:0,3:0,4:0},5:{2:0,3:0,4:0,5:0}},{1:(2,5),2:(6,3),3:(6,-1),4:(-2,-1),5:(-2,3)})

    g.clear()
    g.createRandom(range(50), 0.1, w=[0])
    h = g.copy()
    g.complement(w=[0])
    g.complement(w=[0])
    assert g == h

    g.clear()
    g.addPath(range(5))
    g.complement()
    assert str(g) == "0>0,2,3,4  1>0,1,3,4  2>0,1,2,4  3>0,1,2,3  4>0,1,2,3,4"

    g.clear()
    g.complement()
    assert g == Graph()


def test039_indipendentSet():
    g = Graph()
    g.addArcs([ (1,4),(4,1),(1,5),(5,2),(7,8),(8,7),(2,3),(3,2),6 ])
    assert not g.isIndependentSet([1,3,7,2])
    assert g.isIndependentSet([1,3,7])
    assert not g.isIndependentSet([2,5])
    assert g.isIndependentSet([2,7])
    assert g.isIndependentSet([2,7,0]) == None


def test040_isTournament():
    g = Graph()
    assert not g.isTournament()
    g.addClique(range(5))
    assert not g.isTournament()
    g.clear()
    g.addArcs( [(1,2), (2,3), (3,1)] )
    assert g.isTournament()
    g.addArc(4, 1)
    assert not g.isTournament()
    g.addArc(2, 4)
    assert not g.isTournament()
    g.addArc(4, 3)
    assert g.isTournament()
    g.addArc(4, 4)
    assert not g.isTournament()


def test041_isOrientation():
    g = Graph()
    assert g.isOrientation(g) == False

    g.clear()
    g.addNodes(range(10))
    assert g.isOrientation(g) == True

    g.clear()
    g.addClique(range(10))
    assert g.isOrientation(g) == False

    g.clear()
    g.addClique(range(10))
    h = g.copy()
    h.delArc(0,1)
    assert g.isOrientation(g) == False

    g.clear()
    g.addBiArc(1,2,4)
    g.addBiArc(1,3,2)
    h.clear()
    h.addArc(1,2,1)
    h.addArc(1,3,0)
    assert g.isOrientation(g) == False
    assert h.isOrientation(h) == False
    assert g.isOrientation(h) == False
    assert h.isOrientation(g) == True

    g.clear()
    g.addBiArc(1,2)
    g.addBiArc(1,1)
    h.clear()
    h.addArc(1,2)
    h.addArc(1,1)
    assert g.isOrientation(g) == False
    assert h.isOrientation(h) == False
    assert g.isOrientation(h) == False
    assert h.isOrientation(g) == False
    h.delArc(1,1)
    assert g.isOrientation(g) == False
    assert h.isOrientation(h) == False
    assert g.isOrientation(h) == False
    assert h.isOrientation(g) == False

    g.clear()
    g.addBiArc(1,2)
    g.addBiArc(1,1)
    g.addBiArc(2,2)
    h.clear()
    h.addBiArc(1,2)
    assert h.isOrientation(g) == False


def test042_undirectedArcs_directedArcs():
    g = Graph()
    g.clear()
    g.addBiArc(1,2)
    g.addLoop(1)
    g.addLoop(2)
    g.addArc(1,3)
    r1 = g.undirectedArcs()
    r2 = g.directedArcs()
    assert r1 == [(1, 1), (1, 2), (2, 2)]
    assert r2 == [(1, 3)]
    for n1,n2 in list(r1): r1.append((n2,n1)) # Addiction of the inverted arcs.
    r2 = g.directedArcs()
    assert r2 == [(1, 3)]
    r3 = set(r1).union(r2)
    assert set(g.arcs()) == r3

    g.clear()
    g.createRandom(xrange(50), 0.4)
    r1 = g.undirectedArcs()
    for n1,n2 in list(r1): r1.append((n2,n1)) # Addiction of the inverted arcs.
    r2 = g.directedArcs()
    r3 = set(r1).union(r2)
    assert set(g.arcs()) == r3


def test043_isomorph():
    g = Graph()
    g.addArcs([ (3,1), (3,2) ])
    h = Graph()
    h.addArcs([ ("c","a"), ("c","d") ])
    m = { "d":1, "a":2, "c":3}
    assert g.isIsomorphic(h, m)

    g = Graph()
    g.addArcs([ (3,1), (3,2), (3,4) ])
    h = Graph()
    h.addArcs([ ("c","a"), ("c","d") ])
    m = { "d":1, "a":2, "c":3}
    assert g.isIsomorphic(h, m)

    g = Graph()
    g.addArcs([ (3,1), (3,2), (3,4) ])
    h = Graph()
    h.addArcs([ ("c","a"), ("c","d") ])
    m = { "d":1, "a":2, "c":3}
    assert g.isIsomorphic(h, m)

    g = Graph()
    g.addArcs([ (3,1), (3,2), (3,7) ])
    h = Graph()
    h.addArcs([ ("c","a"), ("c","d"), ("a",4) ])
    m = { "d":1, "a":2, "c":3}
    assert g.isIsomorphic(h, m)

    g = Graph()
    g.addArcs([ (3,1), (3,2), (3,7) ])
    h = Graph()
    h.addArcs([ ("c","a"), ("c","d"), ("a",4) ])
    m = { "d":1, "c":2, "a":3}
    assert not g.isIsomorphic(h, m)

    g = Graph()
    g.addArcs([ (3,1), (3,2) ])
    h = Graph()
    h.addArcs([ ("c","a"), ("c","d") ])
    m = { "d":1, "a":2, "c":3}
    m = g.isomorphMap(h)
    assert g.isIsomorphic(h, m)

    n = range(11)
    g = Graph()
    g.createRandom(n, len(n)**2*0.6)
    h = g.copy()
    n2 = map(lambda x: chr(ord("a") + x), n)
    from random import shuffle
    shuffle(n2)
    for i, n in enumerate(g.xnodes()):
        h.renameNode(n, n2[i])
    m = g.isomorphMap(h)
    #print g, "\n", h, "\n", n2, "\n", m, "\n"
    assert g.isIsomorphic(h, m)


def test044_createIntervalgGraph1():
    g = Graph()
    g.createIntervalgGraph([])
    assert g == Graph()

    g.clear()
    g.createIntervalgGraph([ (1,4),(5,7),(8,11),(3,7),(5,7),(5,8) ])
    assert g.ushort(separator=" ") == "(1, 4)-(3, 7) (3, 7)-(5, 7),(5, 8) (5, 7)-(5, 8) (5, 8)-(8, 11)"

    # Blind test:
    n = 50
    k = 30
    #print "n,k:", n, k
    l = []
    for i in xrange(n):
        r1 = random()*100
        l.append( (r1, r1+random()*k) )
    g.clear()
    g.createIntervalgGraph(l)
    nn = len(g)
    an = g.arcCount + 0.0
    #print "Nodes, arcs, arc/node:", nn, an, round(an/nn, 3)
    #print "How much dense %:", round(100*an/(nn**2), 1)


def test045_short_ushort():
    def AddArcsStr(self, arcsStr, w=None): # Do not include this in Graph.
        for arc in arcsStr.split(","):
            bi = ">" not in arc
            arcl = arc.replace(">", "-").split("-")
            if len(arcl)==2:
                arcl.append(w)
            else:
                arcl[2] = int(arcl[2])
            if bi:
                self.addBiArc(arcl[0].strip(), arcl[1].strip(), arcl[2])
            else:
                self.addArc(arcl[0].strip(), arcl[1].strip(), arcl[2])

    g = Graph()
    g.addClique(range(4), loops=False)
    assert g.short() == "0>1,2,3  1>0,2,3  2>0,1,3  3>0,1,2"
    assert g.ushort() == "0-1,2,3  1-2,3  2-3"

    arcs = "joe-food,joe-dog,joe-tea,joe-cat,joe-table,table-plate-50,plate-food-30,food-mouse-100,food-dog-100,mouse-cat-150,table-cup-30,cup-tea-30,dog-cat-80,cup-spoon-50,plate-fork,dog-flea1,dog-flea2,flea1-flea2-20,plate-knive"
    g.clear()
    AddArcsStr(g, arcs, w=0)
    assert g.short(showw=True, hidew=False) == "cat>dog/80,joe,mouse/150  cup>spoon/50,table/30,tea/30  dog>cat/80,flea1,flea2,food/100,joe  flea1>dog,flea2/20  flea2>dog,flea1/20  food>dog/100,joe,mouse/100,plate/30  fork>plate  joe>cat,dog,food,table,tea  knive>plate  mouse>cat/150,food/100  plate>food/30,fork,knive,table/50  spoon>cup/50  table>cup/30,joe,plate/50  tea>cup/30,joe"
    assert g.ushort(showw=True, hidew=False) == "cat-dog/80,joe,mouse/150  cup-spoon/50,table/30,tea/30  dog-flea1,flea2,food/100,joe  flea1-flea2/20  food-joe,mouse/100,plate/30  fork-plate  joe-table,tea  knive-plate  plate-table/50"


def test046_renameNodes1():
    g = Graph()
    arcs = "a,b b,l,u c,r,t d,f,i,n e,d,h,n f,p,v g,c h,b,n,z i,b,n,t,u l,b,r,t m,f,p,u,z n,p,s o p,a,h,r,z q,p,v r,t s,r t,s u,e,z v z,g,p,s"
    arcs = [a.split(",") for a in arcs.split(" ")]
    g.addMulti(arcs, w=0)
    d = dict( (c,i) for i,c in enumerate("abcdefghil"))
    g.renameNodes(d)
    assert g.short(separator=" ") == "0>1 1>9,u 2>r,t 3>5,8,n 4>3,7,n 5>p,v 6>2 7>1,n,z 8>1,n,t,u 9>1,r,t m>5,p,u,z n>p,s o p>0,7,r,z q>p,v r>t s>r t>s u>4,z v z>6,p,s"

    g.clear()
    g.addNode(1,nodeData="Hello")
    g.addArc(1,2)
    g.addBiArc(2,3)
    g.addArc(3,1)
    assert g == Graph({1: {2: None}, 2: {3: None}, 3: {1: None, 2: None}}, {1: 'Hello'})
    d = {2:1, 1:3, 3:2}
    g.renameNodes(d)
    assert g == Graph({1: {2: None}, 2: {1: None, 3: None}, 3: {1: None}}, {3: 'Hello'})


def test047_undirectedArcs():
    g = Graph()
    g.addNode(1, nodeData=(256,128) )
    g.addNode(2+3J, nodeData=(6,11) )
    g.addNode((1,2), nodeData=(0,0) )
    g.addNode("a", nodeData=(1,1) )
    g.addBiArc(1, 2+3J, w=-2.1)
    g.addArc((1,2), 1, w=5)
    g.addArc(1, (1,2), w=1)
    g.addArc((1,2), 2+3J, w=11)
    g.addBiArc((1,2), "a", w=22)
    g.addBiArc(1,1, w=0)
    assert g.undirectedArcs() == [((1, 2), 'a'), (1, 1), (1, (2+3j))]
    assert g.directedArcs() == [((1, 2), 1), ((1, 2), (2+3j)), (1, (1, 2))]


def test048_savePajek1_saveDot1():
    # This test requires to save/load/remove two files fron disk.
    g = Graph()
    g.addNode(1, nodeData=(256,128) )
    g.addNode(2+3J, nodeData=(6,11) )
    g.addNode((1,2), nodeData=(0,0) )
    g.addNode("a", nodeData=(1,1) )
    g.addBiArc(1, 2+3J, w=-2.1)
    g.addArc((1,2), 1, w=5)
    g.addArc(1, (1,2), w=1)
    g.addArc((1,2), 2+3J, w=11)
    g.addBiArc((1,2), "a", w=22)
    g.addBiArc(1,1, w=0)
    filename = "temp.paj"
    g.savePajek(filename)
    from bz2 import decompress
    from base64 import standard_b64decode
    from os import remove
    d = r"QlpoOTFBWSZTWUt6mzsAAB7fgAAQUH9/QCIAEQAusBwAIABqGqeFMmIMgGhiDTKTagABoAIdlpWRKsYoEkrTN7L0Q11CpFrFVxGkwEducZmeAE4o8xZPFFpGEyBYp84M8UWIhJB5kJFEOXB8hACdS4VoB78BSvVIAWrZ7CEPxdyRThQkEt6mzsA="
    assert open(filename).read() == decompress(standard_b64decode(d))
    remove(filename)

    filename = "temp.dot"
    g.saveDot(filename)
    d = r"QlpoOTFBWSZTWWJy76UAAEZfgAAQUG54AwCAAAo+9d8KIACKCVMkxDRHijQPUBsoJRENAAAA0BHOTIro1EW2CuVXKqcWM1Ts1zn4dA60ZJ6bNkZeEfMQsBUUIbWjRWKwu2B4P6zAcJJWoODdYyQY1CAXtCAewvvvSZ3xroFAjKFgzoGQQeyjwsVCN0XZNX3n/F3JFOFCQYnLvpQ="
    assert open(filename).read() == decompress(standard_b64decode(d))
    remove(filename)


def test049_firstNode1_firstArc1_delArc_delNode():
    g = Graph()
    assert g.firstNode() == None
    assert g.firstArc() == None

    g.addNode(1)
    assert g.firstNode() == 1
    assert g.firstArc() == None

    g.addArc(1,2)
    assert g.firstArc() == (1, 2)

    g.clear()
    g.addClique(range(6))
    nodes = []
    while g:
        n = g.firstNode()
        nodes.append(n)
        g.delNode(n)
    assert set(range(6)) == set(nodes)

    g.clear()
    g.addClique(range(6))
    arcs = []
    while g.arcCount:
        a = g.firstArc()
        arcs.append(a)
        g.delArc(*a)
    h = Graph()
    h.addClique(range(6))
    assert set(arcs) == set(h.arcs())


def test050_addMulti():
    g = Graph()
    g.addNode(1, nodeData=1000)
    l = [(1,2,6),2,(3,1),(1,6),[],[7]]
    g.addMulti(l, w=0, nodeData=0)
    assert g == Graph({1:{2:0,6:0},2:{},3:{1:0},6:{},7:{}},{1:0,2:0,3:0,6:0,7:0})

    g.clear()
    g.addNode(1, nodeData=1000)
    g.addMulti(l, w=0, nodeData=0, bi=True)
    assert g == Graph({1:{2:0,3:0,6:0},2:{1:0},3:{1:0},6:{1:0},7:{}},{1:0,2:0,3:0,6:0,7:0})


def test051_Petersen_isBiregular_isRegular_isKregular():
    g = Graph()
    g.createPetersen()
    assert str(g) == "0-1,2,5  1-3,8  2-6,7  3-4,7  4-5,6  5-9  6-8  7-9  8-9"

    g1 = Graph({0:{0:0,1:0,4:0},1:{1:0,2:0},2:{0:0,1:0,2:0,4:0},3:{0:0,2:0,4:0,5:0},4:{0:0,2:0,3:0,4:0},5:{0:0,1:0,3:0,5:0}})
    g2 = Graph({0:{},1:{2:0,4:0},2:{0:0},3:{0:0,3:0},4:{0:0,5:0},5:{1:0,2:0}})
    g3 = Graph({0:{0:0,1:0,4:0},1:{1:0,2:0,5:0},2:{0:0,1:0,2:0,5:0},3:{0:0,1:0,2:0,3:0,4:0,5:0},4:{0:0,1:0,4:0,5:0},5:{0:0,2:0,3:0,4:0}})
    assert g1.isBiregular()
    assert not g1.isRegular()
    assert not g1.isKregular(8)

    assert not g2.isBiregular()
    assert g2.isRegular()
    assert not g2.isKregular(8)

    assert not g3.isBiregular()
    assert g3.isRegular()
    assert g3.isKregular(8)


def test052_fromMap():
    g = Graph()
    m = [[1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0],
         [1,1,1,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0],
         [1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,0,0,0],
         [0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0]]
    g.fromMap(m)
    ccl = map(len, g.connectedComponents())
    assert len(ccl)==4 and set([11, 9, 5, 4])==set(ccl)
    xside = xrange(100)
    m = [[random()<0.5 for c in xside] for r in xside]
    #t = clock()
    g.fromMap(m)
    #print round(clock()-t,3)


def test053_convexHull():
    from random import seed, gauss
    seed(15151515)
    g = Graph()
    g.addNodes(xrange(2000))
    g.randomCoords(lambda:gauss(1,1), lambda:gauss(1,1))
    ch = g.convexHull(add=True, bi=True)
    #g.plot2d(nodeLabels=False)
    r = [743, 1477, 1393, 1701, 1408, 1269, 611, 740, 445, 925, 921, 1547]
    assert len(ch)==len(r) and set(r)==set(ch)

    g.clear()
    g.addNodes([0,1,2])
    g.nodeData = {0:(0,0), 1:(1,0), 2:(0.5,0.866)}
    ch = g.convexHull(add=True, bi=True)
    r = [0, 2, 1]
    assert len(ch)==len(r) and set(r)==set(ch)

    g.clear()
    g.addNodes([0,1])
    g.nodeData = {0:(0,0), 1:(1,0)}
    ch = g.convexHull(add=True, bi=True)
    r = [0, 1]
    assert len(ch)==len(r) and set(r)==set(ch)

    g.clear()
    g.addNodes([0])
    g.nodeData = {0:(0,0)}
    ch = g.convexHull(add=True, bi=True)
    r = [0]
    assert len(ch)==len(r) and set(r)==set(ch)


def test053_delBiArc():
    g = Graph()
    g.addArc(1, 2)
    g.delBiArc(1, 2)
    assert g.o == {1: {}, 2: {}} == g.i

    g = Graph()
    g.addArc(1, 2)
    g.delBiArc(2, 1)
    assert g.o == {1: {}, 2: {}} == g.i

    g = Graph()
    g.addBiArc(1, 2)
    g.delBiArc(2, 1)
    assert g.o == {1: {}, 2: {}} == g.i

    g = Graph()
    g.addBiArc(1, 2)
    g.delBiArc(1, 2)
    assert g.o == {1: {}, 2: {}} == g.i

    g = Graph()
    g.addNodes([1,2])
    g.delBiArc(2, 1)
    assert g.o == {1: {}, 2: {}} == g.i

    g = Graph()
    g.addBiArc(1, 3)
    g.delBiArc(1, 2)
    assert (g.o, g.i) == ({1: {3: None}, 3: {1: None}}, {1: {3: None}, 3: {1: None}})

    g = Graph()
    g.o = {1: {2: None}, 2: {1: None}}
    g.i = {1: {2: None}, 2: {1: None}}
    g.delBiArc(1, 2)
    assert g.o == {1: {}, 2: {}} == g.i

    g = Graph()
    g.o = {1: {}, 2: {1: None}}
    g.i = {1: {2: None}, 2: {1: None}}
    g.delBiArc(1, 2)
    assert g.o == {1: {}, 2: {}} == g.i

    g = Graph()
    g.o = {1: {}, 2: {1: None}}
    g.i = {1: {}, 2: {}}
    g.delBiArc(1, 2)
    assert g.o == {1: {}, 2: {}} == g.i

    g = Graph()
    g.o = {1: {2: None}, 2: {1: None}}
    g.i = {}
    #print g.o, g.i
    g._regenerate()
    #print g.o, g.i
    g.delBiArc(1, 2)
    assert g.o == {1: {}, 2: {}} == g.i


if __name__ == '__main__':
    print "Graph tests:"
    import graph_test # Maybe the module name can be extracted from __file__
    from sys import stdout
    from doctest import run_docstring_examples
    time1 = clock()
    testFunctions = sorted(f for f in dir(graph_test) if f.startswith("test"))
    for i,fun in enumerate(testFunctions):
        funObject = eval(fun)

        # Test the function, with its asserts for working examples:
        funObject()

        # Test its docstring, just for the failing examples:
        run_docstring_examples(funObject, globals())

        # Print another "." without the space:
        stdout.write(".")

        # Just 5+5 tests for each row:
        if ((i+1) % 5) == 0 and i>0: stdout.write(" ")
        if ((i+1) % 10) == 0 and i>0: stdout.write("\n")
    print "\n" + str(len(testFunctions)), "Graph tests finished in", round(clock()-time1,1), "seconds."