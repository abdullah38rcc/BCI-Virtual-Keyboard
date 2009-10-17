"""
graph.py
A graph is set of items (nodes or vertices) connected by arcs (also called edges).
This module contains a Graph class to implement a network data structure.
By leonardo maffi, V. 2.32, Jun 30 2006.
Dijkstra algorithm implementation is by David Eppstein.

This library has the same license as Python itself: http://www.python.org/2.4/license.html


REQUIREMENTS: Python 2.4
OPTIONAL: Tkinter, Psyco, numarray or Numeric, GrafPlotLib, Graphviz, Pajek.

DATA STRUCTURES:
This structure allows loops, and no more than one directed arc from a node to another one
  (another arc in the opposite direction is allowed too).
- This directed graph class contains a dictionary "o". Inside "o" each key is a node;
    the corresponding value is another dictionary, it contains keys (final ends of arcs),
    and their values are the arcs weights.
    Undirected arcs are made with two opposite directed arcs.
- There is second dictionary, called "i", that is the trasposed of "o", and with equal structure.
- The third dictionary is "nodeData", it contains optional data associated with nodes.
    By default if a node isn't present inside nodeData, then it's associated data is None.
    Associating None as the data of a node, removes it from nodeData.
- "arcCount" is the total number of directed arcs of the graph. Loops are counted two times.


EXAMPLE GRAPH:
self.o = {0:{1:2}, 1:{2:2}, 2:{0:2,1:2}}
self.i = {0:{2:2}, 1:{0:2,2:2}, 2:{1:2}}
self.nodeData = {0:"N1", 1:"N2", 2:"N3"}
self.arcCount = 4
self.nextNode = 0

This graph as adjacency matrix (1 = arc present):
     0 1 2
0: | 0 1 0 |
1: | 0 0 1 |
2: | 1 1 0 |

Its matrix of arc weights:
     0 1 2
0: |   2   |
1: |     2 |
2: | 2 2   |


NOTES:
- Method names beginning with "_" are usually private. Sometimes they are public, but low level and
  without safety cheeks, for people that know well the details of data structures used by the graph.
- Masking/unmasking of nodes and arcs isn't supported, to keep algorithms simple enough.
- "Bidirectional arcs" (here usually called "BiArcs") are defined as a couple of
  opposite arcs between two nodes with the same arc weights.
- Self-loops are allowed, they count as *two* for the global arc count of the graph. So a complete
  graph has n*(n+1) arcs (and not just n*n).
- Node IDs must be hashable, but they can be unsortable. So [1] isn't allowed as node ID, but 1+8J
  is allowed. Unsortable nodes change the behaviour of some printing methods (that call _mysorted).
- Arc weights and nodeData can be any object, like a tuple of the coordinates of a node, its
  color, a number, it's masking status, etc.


SEE "graph_docs.txt" for more information on methods and the graph.
"""

"""

KNOWN BUGS:


TO DO:
- add a call to Graphviz?
- Depth-first traversal with cycle detection
- Depth-first traversal results in a spanning tree (Spanning tree: path through all vertices in a tree)
- Jarnik-Prim
- kruskal
- Bellman-Ford algorithm
- Max-flow: Ford-Fulkerson algorithm
- random graph generators
- shortestPath again
- Add tests
"""


from itertools import islice, chain, tee, izip
from collections import deque # For BFS.
import os, stat # For binaryLoad and allPairsShortestPaths
import cPickle # For binarySave and binaryLoad.
from bz2 import BZ2File # for binarySave and binaryLoad.
from random import random # for createRandom, randomw and springCoords
from cartesianPlot import cartesianPlot # For 2dshow
from math import pi, sin, cos, sqrt # For circularCoords and springCoords
from sys import maxint, platform # For allPairsShortestPaths
import sys # For allPairsShortestPaths (path)
from operator import itemgetter # for createIntervalgGraph
from difflib import get_close_matches # for __getattr__
from partition import partition # for allPairsShortestPaths
from subprocess import Popen, PIPE # for allPairsShortestPaths
import dijkstra


def _mysorted(seq):
    "_mysorted(seq): useful for unsortable node IDs."
    result = list(seq) # This is necessary if seq is an iterator.
    try:
        result.sort()
    except TypeError:
        pass
    return result


def _stableUnique(seq): # This function is present in util too.
    """_stableUnique(seq): return a list with the unique elements in seq, keeping their original
    order. Elements must be hashable."""
    if isinstance(seq, set):
        return list(seq)
    else:
        seqSet= set()
        result = []
        for e in seq:
            if e not in seqSet:
                result.append(e)
                seqSet.add(e)
        return result


def xpairwise(iterable): # From util
    "xpairwise(range(n)) ==> (0,1), (1,2), (2,3), ..., (n-2, n-1)"
    a, b = tee(iterable)
    try:
        b.next()
    except StopIteration:
        pass
    return izip(a, b)


class _GetterSetter(object):
    "_GetterSetter: object to get or set an arc of the graph."
    # for __getitem__ of class Graph
    def __init__(self, g, n1):
        self._g = g
        self._n1 = n1
    def __setitem__(self, n2, arcw):
        self._g.addArc(self._n1, n2, arcw)
    def __getitem__(self, n2):
        return self._g.getArcw(self._n1, n2)
    def __str__(self):
        return "<Getter/setter of the arc starting from node: " + repr(self._n1) + ">"


class Graph(object):
    """Directed weighted graph data structure class. A graph is set of nodes connected by arcs.
    Node IDs must be hashable, weights can be non-hashable. More info in the module docstring."""

    __slot__ = ["o", "i", "nodeData", "arcCount", "nextNode"]


    def __init__(self, nodesGraph=None, nodeData=None):
        "__init__(self, nodesGraph=None, nodeData=None): create a graph structure."
        if nodesGraph!=None and not isinstance(nodesGraph, (dict, Graph)):
            raise TypeError, "in Graph __init__: input nodesGraph isn't None, Graph or a dict."
        if nodeData!=None and not isinstance(nodeData, dict):
            raise TypeError, "in Graph __init__: input nodeData isn't None or a dict."
        if isinstance(nodesGraph, Graph): # copy.
            self.o = {}
            self.i = {}
            self_o = self.o
            self_i = self.i
            for n,a in nodesGraph.o.iteritems(): # Its necessary to copy a the second level too.
                self_o[n] = dict(a)
            for n,a in nodesGraph.i.iteritems(): # Its necessary to copy a the second level too.
                self_i[n] = dict(a)
            self.nodeData = dict(nodesGraph.nodeData)
            self.arcCount = nodesGraph.arcCount
            self.nextNode = nodesGraph.nextNode
        else:
            self.o = {} # Outbound arcs. Node name => outbound name arcs => arc weights.
            self.i = {} # Inbound arcs. Node name => inbound arc names => arc weights (oa transposed).
            self.nodeData = {} # Node data. Node name => optional data associated with the node
                               #   (not present means None).
            self.arcCount = 0  # Total number of directed arcs. Each self-loop is counted two times.
            self.nextNode = 0 # Next number that can be used by createID.
            if nodesGraph: # This can be made faster, but here controls are important.
                for n1, arcs in nodesGraph.iteritems():
                    self.addNode(n1)
                    for n2, w in arcs.iteritems():
                        self.addArc(n1, n2, w)
                if nodeData:
                    for node,data in nodeData.iteritems():
                        if node in self.o:
                            self.nodeData[node] = data


    # NODE OPERATIONS: ===========================================
    def addNode(self, n, nodeData=None):
        """addNode(n, nodeData=None) (or just add): add a node n, if not already present.
        Updates its nodeData if necessary. nodeData exists only if it's != None.
        n must be hashable, otherwise a TypeError is raised."""
        if n not in self.o:
            self.o[n] = {}
            self.i[n] = {}
        if nodeData is None:
            if n in self.nodeData:
                del self.nodeData[n] # Not present nodeData is equivalent to None.
        else:
            self.nodeData[n] = nodeData

    add = addNode


    def addNodes(self, nodes, nodeData=None):
        """addNodes(nodes, nodeData=None): add a sequence of nodes.
        Updates their nodeData if necessary. nodeData exists only if it's != None.
        nseq must contain hashables, otherwise a TypeError is raised."""
        self_o = self.o
        self_i = self.i
        self_nodeData = self.nodeData
        for n in nodes:
            if n not in self_o:
                self_o[n] = {}
                self_i[n] = {}
        if nodeData != None:
            for n in nodes:
                self_nodeData[n] = nodeData # (not present means None).
        else:
            for n in nodes:
                if n in self_nodeData:
                    del self_nodeData[n]


    def hasNode(self, n):
        "hasNode(n): return True if node n exists in the graph. You can also use 'n in g'."
        return n in self.o


    def getNodeData(self, n):
        "getNodeData(n): if the node n exists, return its nodeData, otherwise return None."
        if n in self.o and n in self.nodeData:
            return self.nodeData[n]


    def changeNodeData(self, n, newnd):
        """changeNodeData(n, newnd): updates/adds nodeData to a node n, if n is present.
        if nodeData=None its nodeData is deleted."""
        if newnd is None:
            self.nodeData.pop(n, 0)
        elif n in self.o:
            self.nodeData[n] = newnd


    def renameNode(self, oldnode, newnode):
        """renameNode(oldnode, newnode): copy old node with a new name (not already present),
        then delete the old node (this is a slow operation)."""
        # This is a O(k) operation, where k is the number of inbound arcs of oldnode.
        self_o = self.o
        self_i = self.i
        if oldnode in self_o and oldnode in self_i and newnode not in self_o:
            self_o[newnode] = dict(self_o[oldnode])
            self_i[newnode] = dict(self_i[oldnode])
            for n,w in self_i[oldnode].iteritems():
                self_o[n][newnode] = w
                del self_o[n][oldnode]
            for n,w in self_o[oldnode].iteritems():
                self_i[n][newnode] = w
                del self_i[n][oldnode]
            if oldnode in self.nodeData:
                self.nodeData[newnode] = self.nodeData[oldnode]
                del self.nodeData[oldnode]
            del self_o[oldnode]
            del self_i[oldnode]


    def renameNodes(self, trans):
        """renameNodes(trans): renames nodeIDs using a trans translation dictionary.
        trans.keys() are the old nodeIDs, and trans.values() are new NodeIDs.
        renameNodes is faster than many calls to renameNode."""
        tresh = 0.25
        if not trans: return # Finish already.
        if set(trans) - set(self.o):
            raise TypeError, "trans contains nodes that aren't in the self graph."
        if (len(trans)+0.0) / len(self.o) <= tresh:
            for oldnode,newnode in trans.iteritems():
                self.renameNode(oldnode, newnode)
        else: # else it's faster to regenerate all the graph:
            auxg = self.__class__()
            auxg_o = auxg.o
            auxg_i = auxg.i
            for n1,a in self.o.iteritems():
                n1Translated = trans.get(n1, n1)
                auxg_o[n1Translated] = {}
                for n2,w in a.iteritems():
                    auxg_o[n1Translated][trans.get(n2, n2)] = w
            for n1,a in self.i.iteritems():
                n1Translated = trans.get(n1, n1)
                auxg.i[n1Translated] = {}
                for n2,w in a.iteritems():
                    auxg_i[n1Translated][trans.get(n2, n2)] = w
            for n in self.nodeData:
                auxg.nodeData[trans.get(n, n)] = self.nodeData[n]
            self.o = auxg.o
            self.i = auxg.i
            self.nodeData = auxg.nodeData


    def firstNode(self):
        """firstNode(): return an arbitrary node, without removing it, or None if the graph is empty.
        It uses the next() method of the nodes dictionary, so it usually returns the same node."""
        if not self.o: return None
        return self.o.iterkeys().next()


    def delNode(self, n):
        "delNode(n): remove the node n, if present."
        self_o = self.o
        self_i = self.i
        if n in self_o and n in self_i:
            arcCount = self.arcCount
            if n in self_o[n]:
                del self_o[n][n]
                arcCount -= 2
            if n in self_i[n]:
                del self_i[n][n]
            for n1 in self_i[n].iterkeys():
                if n1 in self_o and n in self_o[n1]:
                    del self_o[n1][n]
                    arcCount -= 1
            for n1 in self_o[n].iterkeys():
                if n1 in self_i and n in self_i[n1]:
                    del self_i[n1][n]
            self.arcCount = arcCount - len(self_o[n])
            del self_o[n]
            del self_i[n]
            if n in self.nodeData:
                del self.nodeData[n]


    def popNode(self):
        """popNode(): remove and return an arbitrary node of the graph. Raises IndexError if the
        graph is empty."""
        if not self.o:
            raise IndexError("No items to select.")
        node = self.o.iterkeys().next()
        self.delNode(node) # remove it.
        return node


    def delManyNodes(self, nodes):
        """delManyNodes(nodes): quickly deletes many nodes, given as a sequence.
        Useful to remove ~30% or more of the nodes of the graph for a complete graph, or
        ~55% or more of the nodes for a path graph. For fewer nodes delNode method is faster."""
        for n in nodes:
            self.o.pop(n, 0)
            self.i.pop(n, 0)
        self._cleanDeadArcs()


    def inNodes(self, n):
        """inNodes(n): return the list of nodes with arcs to the node n.
        If n isn't present, return []."""
        if n in self.i:
            return self.i[n].keys()
        else:
            return []

    def outNodes(self, n):
        """outNodes(n): return the list of nodes connected with arcs coming from the node n.
        If n isn't present, return []."""
        if n in self.o:
            return self.o[n].keys()
        else:
            return []

    def xinNodes(self, n):
        """xinNodes(n): return the iterable of nodes with arcs to the node n.
        If n isn't present, return []."""
        if n in self.i:
            return self.i[n].iterkeys()
        else:
            return []

    def xoutNodes(self, n):
        """xoutNodes(n): return the iterable of nodes connected with arcs coming from the node n.
        If n isn't present, return []."""
        if n in self.o:
            return self.o[n].iterkeys()
        else:
            return []

    def inOutNodes(self, n):
        """inOutNodes(n): return a list containing the nodes connected with arcs coming from the
        node n, followed by the nodes with arcs to the node n. If n isn't present, return []."""
        if n in self.i and n in self.o:
            return self.i[n].keys() + self.o[n].keys()
        else:
            return []

    def xinOutNodes(self, n):
        """xinOutNodes(n): return an iterable of the nodes connected with arcs coming from the
        node n, chained with the iterable of nodes with arcs to the node n.
        If n isn't present, return []."""
        if n in self.i and n in self.o:
            return chain(self.i[n].iterkeys(), self.o[n].iterkeys())
        else:
            return []


    def nodes(self):
        "nodes(): return an unsorted list of the IDs of all the nodes of the graph."
        return self.o.keys()

    def xnodes(self):
        """xnodes(): return an unsorted iterable of the IDs of all the nodes of the graph.
        The same as iterating on the graph itself."""
        return self.o.iterkeys()


    def degree(self, node):
        """degree(node): return the degree (the number of inbound + outbound arcs) of a node.
        Self-loops are counted twice. Return 0 if the node isn't in the graph."""
        if node in self.o and node in self.i:
            return len(self.o[node]) + len(self.i[node])
        else:
            return 0

    def inDegree(self, node):
        """inDegree(node): return the number of arcs coming into a node.
        Self-loops are counted one time. Return 0 if the node isn't in the graph."""
        if node in self.i:
            return len(self.i[node])
        else:
            return 0

    def outDegree(self, node):
        """outDegree(node): return the number of arcs coming from a node.
        Self-loops are counted one time. Return 0 if the node isn't in the graph."""
        if node in self.o:
            return len(self.o[node])
        else:
            return 0


    def xselectNodeData(self, predicate=bool):
        """xselectNodeData(nodeData): return an iterable of all the nodes with
         predicate(nodeData)==True. Example:
           xselectNodeData(lambda nd: isinstance(nd, (tuple,list)) and len(nd)=2 )
         Another example to select nodes without nodeData:
           xselectNodeData( lambda nd: nd==None ) """
        return ( n for n in self.o.iterkeys() if predicate(self.nodeData.get(n, None)) )


    def createID(self, n):
        "createID(n): return a list of n integers (or longs) that aren't already nodes of the graph."
        n = int(round(n))
        result = []
        nextNode = self.nextNode
        for i in xrange(n):
            while nextNode in self.o:
                nextNode += 1
            result.append(nextNode)
            nextNode += 1
        self.nextNode = nextNode
        return result


    def _rawDelNode(self, n):
        """_rawDelNode(n): low level method: quickly delete a node from the graph without removing
        dead-ending arcs. After one or more rawDelNode, a cleanDeadArcs is necessary."""
        self.o.pop(n, 0)
        self.i.pop(n, 0)


    # ARC OPERATIONS: ===========================================

    def addArc(self, n1, n2, w=None):
        """addArc(n1, n2, w=None): add/update a directed arc between node n1 and n2.
        The weight w can be any object, and it is always present (None by default)."""
        # This method can made faster, but then it can become quite difficult to understand.
        # Still, it's a very used basic method for a graph, therefore speed is quite important.
        self_o = self.o
        self_i = self.i
        if n1 not in self_o:
            self_o[n1] = {}
            self_i[n1] = {}
        if n2 not in self_o:
            self_o[n2] = {}
            self_i[n2] = {}
        if n2 not in self_o[n1]:
            if n1 == n2:
                self.arcCount += 2
            else:
                self.arcCount += 1
        self_o[n1][n2] = w
        self_i[n2][n1] = w


    def __getitem__(self, n1):
        """__getitem__: to set and get an arc of the graph with the syntax graph[n1][n2].
        This is rather slow, use addArc or getArcw for a faster access."""
        return _GetterSetter(self, n1)


    def addBiArc(self, n1, n2, w=None):
        """addBiArc(n1, n2, w=None): add/update two arcs in opposite directions (an undirected arc)
        between node n1 and n2. Their weight w can be any object, and they are always present
        (None by default)."""
        if n1 == n2:
            if n1 in self.o:
                if n1 not in self.o[n1]:
                    self.arcCount += 2
                self.o[n1][n1] = w
                self.i[n1][n1] = w
            else:
                self.o[n1] = { n1:w }
                self.i[n1] = { n1:w }
                self.arcCount += 2
        else:
            self_o = self.o
            self_i = self.i
            if n1 not in self_o:
                self_o[n1] = {}
                self_i[n1] = {}
            if n2 not in self_o:
                self_o[n2] = {}
                self_i[n2] = {}
            if n2 not in self_o[n1]:
                self.arcCount += 1
            if n1 not in self_o[n2]:
                self.arcCount += 1
            self_o[n1][n2] = w
            self_i[n2][n1] = w
            self_o[n2][n1] = w
            self_i[n1][n2] = w


    def hasArc(self, n1, n2):
        "hasArc(n1, n2): return True is the directed arc between n1 and n2 exists in the graph."
        self_o = self.o
        self_i = self.i
        return ( n1 in self_o and n2 in self_o and n1 in self_i and n2 in self_i and
                 n2 in self_o[n1] and n1 in self_i[n2] )


    def getArcw(self, n1, n2):
        """getArcw(n1, n2): if the directed arc between n1 and n2 exists return its weight,
        otherwise raise KeyError."""
        if n1 not in self.o: raise KeyError, repr(n1)
        if n2 not in self.o[n1]: raise KeyError, repr(n1) + " -> " + repr(n2)
        return self.o[n1][n2]


    def setArcw(self, n1, n2, neww):
        """setArcw(n1, n2, neww): if the directed arc between n1 and n2 is present,
        then updates its weight w."""
        if n1 in self.o and n2 in self.o[n1]:
            self.o[n1][n2] = neww
        if n2 in self.i and n1 in self.i[n2]:
            self.i[n2][n1] = neww


    def delArc(self, n1, n2):
        """delArc(n1, n2): remove, if present, the directed arc between node n1 and node n2."""
        if n1 in self.o and n2 in self.o[n1]:
            del self.o[n1][n2]
            if n1 == n2:
                self.arcCount -= 2
            else:
                self.arcCount -= 1
        if n2 in self.i and n1 in self.i[n2]:
            del self.i[n2][n1]


    def delBiArc(self, n1, n2):
        """delBiArc(n1, n2): remove, if present, the bidirectional arc between n1 and n2,
        or just one of the directional ones."""
        if n1 == n2:
            if n1 in self.o and n1 in self.o[n1]:
                del self.o[n1][n1]
                self.arcCount -= 1
            if n1 in self.i and n1 in self.i[n1]:
                del self.i[n1][n1]
                self.arcCount -= 1
        else:
            if n1 in self.o and n2 in self.o[n1]:
                del self.o[n1][n2]
                self.arcCount -= 1
            if n2 in self.i and n1 in self.i[n2]:
                del self.i[n2][n1]
            if n2 in self.o and n1 in self.o[n2]:
                del self.o[n2][n1]
                self.arcCount -= 1
            if n1 in self.i and n2 in self.i[n1]:
                del self.i[n1][n2]


    def inArcs(self, n):
        "inArcs(n): return the list of arcs (*,n)."
        if n in self.i:
            return [ (n1, n) for n1 in self.i[n].iterkeys() ]
        else:
            return []

    def outArcs(self, n):
        "outArcs(n): return the list of arcs (n,*)."
        if n in self.o:
            return [ (n, n1) for n1 in self.o[n].iterkeys() ]
        else:
            return []

    def xinArcs(self, n):
        "xinArcs(n): return the iterable of arcs (*,n)."
        if n in self.i:
            return ((n1, n) for n1 in self.i[n].iterkeys())
        else:
            return []

    def xoutArcs(self, n):
        "xoutArcs(n): return the iterable of arcs (n,*)."
        if n in self.o:
            return ((n, n1) for n1 in self.o[n].iterkeys())
        else:
            return []


    def arcs(self):
        """arcs(): return an unsorted list of all the arcs of the graph, without weights.
        Its elements are (n1,n2)."""
        self_o = self.o
        return [(n1,n2) for n1,a in self_o.iteritems() for n2 in a.iterkeys()]

    def xarcs(self):
        """xarcs(): return an iterator on all the unsorted arcs of the graph, without weights.
        Its elements are (n1,n2)."""
        self_o = self.o
        return ( (n1,n2) for n1,a in self_o.iteritems() for n2 in a.iterkeys() )

    def arcsw(self):
        """arcsw(): return an unsorted list of all the arcs of the graph, with weights.
        Its elements are (n1,n2,w)."""
        self_o = self.o
        return [ (n1,n2,w) for n1,a in self_o.iteritems() for n2,w in a.iteritems() ]

    def xarcsw(self):
        """xarcsw(): return an iterator on all the unsorted arcs of the graph, with weights.
        Its elements are (n1,n2,w)."""
        self_o = self.o
        return ( (n1,n2,w) for n1,a in self_o.iteritems() for n2,w in a.iteritems() )


    def delAllLoops(self):
        "delAllLoops(): delete all loops from the graph."
        self_i = self.i
        for n,a in self.o.iteritems():
            if n in a:
                del a[n]
                del self_i[n][n] # graph must be coherent.
                self.arcCount -= 2


    def hasLoops(self):
        "hasLoops(): return True if the Graph has one or more loops."
        for n,a in self.o.iteritems():
            if n in a:
                return True
        return False


    def directedArcs(self):
        """directedArcs(): return an unsorted list of all the directed arcs of the graph.
        In the result there aren't self-loops."""
        so = self.o
        return [ (n1,n2) for n1,a in so.iteritems() for n2,w in a.iteritems() if n1 not in so[n2] \
                                                                              or w != so[n2][n1]]

    def undirectedArcs(self):
        """undirectedArcs(): return an unsorted list of all the undirected arcs of the graph.
        In the result there is only one arc (randomly chosen) for each undirected arc,
        and self-loops too. An arc is undirected if there is only an arc between two nodes, or if
        there are two but the tweir weights are different."""
        so = self.o
        result = []
        added = set()
        for n1,a in so.iteritems():
            for n2,w in a.iteritems():
                if n1 in so[n2] and w==so[n2][n1] and (n2,n1) not in added:
                    arc = (n1,n2)
                    result.append( arc )
                    added.add( arc )
        return result


    def delAllArcs(self):
        "delAllArcs(): removes all the arcs from the graph."
        self_o = self.o
        self_i = self.i
        for n in self_o: self_o[n].clear()
        for n in self_i: self_i[n].clear()
        self.arcCount = 0


    def sumw(self):
        """sumw(): return the sum of the weights of all arcs.
        NOTE: weights must be int, long or float, otherwise an error is raised.
        You can use integerw or realw to test it before."""
        result = 0
        self_o = self.o
        for n in self.o.iterkeys():
            result += sum(self_o[n].itervalues()) # Suggestion: do not use sum start here.
        return result


    def sumPathw(self, path):
        """sumPathw(path): given a sequence of nodes, return the summed weight of the path.
        All arc weights must have __add__ defined (like int, long, float, basestring, complex),
        otherwise an error is raised. If path is empty, or len(path)==1, return None. Example:
          g = Graph()
          g.addArcs( [("a","b",1), ("b","c",0.5)] )
          print g.sumPathw( "abc" ) ==> 1.5
          print g.sumPathw( "ab" ) ==> 1
          print g.sumPathw( "a" ) ==> None  """
        if not isinstance(path, (list, tuple, basestring)):
            raise TypeError, "in sumPathw: path isn't a list, tuple or basestring."
        result = None # An empty sequence, or a single node are ignored.
        self_o = self.o
        first = True
        for n1,n2 in zip(path[:-1], path[1:]):
            if n1 in self_o and n2 in self_o[n1]:
                if first:
                    result = self_o[n1][n2]
                    first = False
                else:
                    result += self_o[n1][n2]
            else:
                raise "in sumPathw: one or more path nodes don't exist, or they aren't connected."
        return result


    def inThroughCapacity(self, node):
        """inThroughCapacity(node): return the max in flow that may be received through the node.
        Return 0 by default."""
        if node in self.i:
            return sum( self.i[node].itervalues() )

    def outThroughCapacity(self, node):
        """outThroughCapacity(node): return the max out flow that may be given through the node.
        Return 0 by default."""
        if node in self.o:
            return sum( self.o[node].itervalues() )

    def throughCapacity(self, node):
        """throughCapacity(node): return the max flow that may be sent through the node.
        It's the min of inThroughCapacity and outThroughCapacity."""
        return min( self.inThroughCapacity(node), self.outThroughCapacity(node) )

    def maxThroughCapacity(self):
        "maxThroughCapacity(): return the max flow that may be sent through any node of the graph."
        if self.o:
            return max( map(self.throughCapacity, self.o) )
        else:
            return 0


    def isUndirectedArc(self, n1, n2):
        """isUndirectedArc(n1, n2): return True if between two nodes there are two arcs with
        the same weight. Return False otherwise."""
        # Full coherence tests!
        # This method has a long name to make its meaning fully explicit (isBiArc isn't clear).
        self_o = self.o
        self_i = self.i
        return ( n1 in self_o and n2 in self_o and n2 in self_o[n1] and n1 in self_o[n2] and
                 n1 in self_i and n2 in self_i and n2 in self_i[n1] and n1 in self_i[n2] and
                 self_o[n1][n2]==self_o[n2][n1] and self_i[n1][n2]==self_i[n2][n1] )


    def reverseArc(self, n1, n2):
        """reverseArc(n1, n2): invert the direction of a single arc, or
        both bidirectional arcs, between node n1 and n2."""
        """
        # Original hi-level algorithm:
        if self.hasArc(n1, n2):
            w1 = self.getArcw(n1, n2)
            if self.hasArc(n2, n1):
                w2 = self.getArcw(n2, n1)
                self.setArcw(n1, n2, w2)
                self.setArcw(n2, n1, w1)
            else: # There is only n1 -> n2
                self.delArc(n1, n2)
                self.addArc(n2, n1, w1)
        else:
            if self.hasArc(n2, n1): # only n2 -> n1
                w2 = self.getArcw(n2, n1)
                self.delArc(n2, n1)
                self.addArc(n1, n2, w2)
        """
        if n1 != n2:
            self_o = self.o
            self_i = self.i
            if n1 in self_o and n2 in self_o and n1 in self_i and n2 in self_i:
                if n2 in self_o[n1] and n1 in self_i[n2]:
                    w1 = self_o[n1][n2]
                    if self.hasArc(n2, n1):
                        w2 = self_o[n2][n1]
                        self_o[n1][n2] = w2
                        self_i[n2][n1] = w2
                        self_o[n2][n1] = w1
                        self_i[n1][n2] = w1
                    else: # There is only n1 -> n2
                        self.delArc(n1, n2)
                        self_o[n2][n1] = w1
                        self_i[n1][n2] = w1
                        self.arcCount += 1
                else:
                    if n1 in self_o[n2] and n2 in self_i[n1]: # only n2 -> n1
                        w2 = self_o[n2][n1]
                        self.delArc(n2, n1)
                        self_o[n1][n2] = w2
                        self_i[n2][n1] = w2
                        self.arcCount += 1


    def makeUndirectArc(self, n1, n2, reconcile=None):
        """makeUndirectArc(n1, n2, reconcile=None): make the already existing arc undirected,
        duplicating it if it's directed. Do nothing if they don't share an arc.
        If there are already two arcs between the two nodes, and their weights are
        different, it calls the given reconcile function (like the makeUndirected), that takes two
        weights as input, and chooses which one to keep (or raises an exception when needed).
        If reconcile isn't given, then it uses the standard one that always raises an exception.
        Few possible alternative reconcile functions:
        from random import random
        def reconcile(w1, w2): # Random choose.
            if random() <= 0.5: return w1
            else: return w2
        Another possible:
        def reconcile(w1, w2): # Always choose the first.
            return w1
        Another possible:
        def reconcile(w1, w2): # Average of two.
            return (w1+w2)/2
        Another possible:
        def reconcile(w1, w2): # Weight = None
            return None """
        if n1 == n2 and n1 in self.o and n1 in self.o[n1]:
            return # If there's a loop do nothing.
        self_o = self.o
        self_i = self.i
        if n1 in self_o and n2 in self_o and n1 in self_i and n2 in self_i: # n1 and n2 exist
            if reconcile is None:
                def reconcile(w1, w2):
                    s = "Between the two nodes there are already two arcs with different weights: w1,w2= ("
                    raise s + str(w1) + ", " + str(w2) + ")."

                if n2 in self_o[n1] and n1 in self_i[n2]: # If n1->n2 exists:
                    w12 = self_o[n1][n2]
                    if n1 in self_o[n2] and n2 in self_i[n1]: # If n2<->n1 exists:
                        w21 = self_o[n2][n1]
                        if w12 != w21:
                            w = reconcile(w12, w21)
                            self_o[n1][n2] = w
                            self_i[n2][n1] = w
                            self_o[n2][n1] = w
                            self_i[n1][n2] = w
                    else: # n1->n2 exists and n2->n1 not exists
                        self_o[n2][n1] = w12
                        self_i[n1][n2] = w12
                        self.arcCount += 1
                elif n1 in self_o[n2] and n2 in self_i[n1]: # n1->n2 not exists. If n2->n1 exists:
                    w21 = self_o[n2][n1]
                    self_o[n1][n2] = w21
                    self_i[n2][n1] = w21
                    self.arcCount += 1


    def addLoop(self, n, w=None):
        """addLoop(self, n, w=None): add/update a self-loop at node n.
        The weight w can be any object, and it is always present (None by default)."""
        if n in self.o:
            if n not in self.o[n]:
                self.arcCount += 2
            self.o[n][n] = w
            self.i[n][n] = w
        else:
            self.o[n] = { n:w }
            self.i[n] = { n:w }
            self.arcCount += 2


    def firstArc(self):
        """firstArc(): return an arbitrary arc, without removing it, or None if there aren't arcs.
        It uses the next() method of the nodes dictionary, so it usually returns the same node."""
        if not self.arcCount: return None
        for n1,a in self.o.iteritems():
            if a: return n1, a.iterkeys().next()


    def xselectw(self, predicate=bool):
        """xselectw(predicate=bool): return an iterable of all the arcs with predicate(w)==True.
        Ex: xselectw(lambda w: w>=12)  """
        self_o = self.o
        return ( (n1,n2) for n1,a in self_o.iteritems() for n2,w in a.iteritems() if predicate(w) )


    def convexHull(self, add=False, bi=False, w=None):
        """convexHull(add=False, bi=False, w=None): return a list of the 2D convex hull of the nodes
        of the graph.
        If add=True add directed arcs of the convex hull to the graph, with given w arc weight.
        nodeData of nodes must contain their (x,y) coordinates.
        If add=True and bi=True, arcs are created undirected."""
        def convexHull2D(points):
            """convexHull2D(points): convex hull (Graham scan by x-coordinate) of a list of 2D points in
            O(n log n) time. A point is a pair (x,y). Return the list of the points on the convex hull."""
            # David Eppstein, UC Irvine, 7 Mar 2002, modified.
            # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117225
            def orientation(p,q,r):
                "Return positive number if p-q-r are clockwise, neg if ccw, zero if colinear."
                p0, p1 = p
                q0, q1 = q
                r0, r1 = r
                return (q1-p1)*(r0-p0) - (q0-p0)*(r1-p1)

            U = []
            L = []
            for p,i in sorted((p,i) for i,p in enumerate(points)):
                while len(U) > 1 and orientation(U[-2][0],U[-1][0],p) <= 0: U.pop()
                while len(L) > 1 and orientation(L[-2][0],L[-1][0],p) >= 0: L.pop()
                U.append((p,i))
                L.append((p,i))
            L.reverse()
            return U[:-1] + L

        if not self:
            return []
        err = self.isEmbedded()
        if err is not True:
            return err
        nlabels = self.nodeData.keys()
        coords = self.nodeData.values() # The order is the same of nlabels.
        hullNodes = [nlabels[n] for c,n in convexHull2D(coords)]
        if add:
            self.addArcs(xpairwise(hullNodes), bi=bi, w=w)
        if len(hullNodes)>1:
            return hullNodes[:-1]
        else:
            return hullNodes


    def _fastAddArc(self, n1, n2, w=None):
        """_fastAddArc(n1, n2, w=None): low level method: nodes must be already present, and arc
        must not be present."""
        # This method is probably useless, and can be removed.
        self.o[n1][n2] = w
        self.i[n2][n1] = w
        if n1 == n2:
            self.arcCount += 2
        else:
            self.arcCount += 1


    def _fastAddBiArc(self, n1, n2, w=None):
        """_fastAddBiArc(n1, n2, w=None): low level method: nodes must be already present, and
        arcs must not be present."""
        # This method is probably useless, and can be removed.
        if n1 == n2:
            self.arcCount += 2
            self.o[n1][n1] = w
            self.i[n1][n1] = w
        else:
            self.arcCount += 1
            self_o = self.o
            self_i = self.i
            self_o[n1][n2] = w
            self_i[n2][n1] = w
            self_o[n2][n1] = w
            self_i[n1][n2] = w


    def _recountArcs(self):
        """_recountArcs(): low level method: recount all the arcs of the graph, updating arcCount.
        Useful after some low level changes to the graph. Each self-loops counts as two arcs."""
        self_o = self.o
        self.arcCount = sum( len(a)+(n in a) for n,a in self_o.iteritems() )


    def _fastDelArc(self, n1, n2):
        """_fastDelArc(n1, n2): low level method: remove the directed arc between n1 and n2.
        The directed arc must be present."""
        del self.o[n1][n2]
        del self.i[n2][n1]
        if n1 == n2:
            self.arcCount -= 2
        else:
            self.arcCount -= 1


    def _cleanDeadArcs(self):
        """_cleanDeadArcs(): low level method: clean dead-ending arcs, useful after many "raw"
        node deletions, and then it calls regenerate."""
        self_o = self.o
        for a in self_o.itervalues():
            for n in a.keys(): # Do not put an interkeys here!
                if n not in self_o:
                    del a[n]
        self._regenerate()


    # GRAPH OPERATORS: ===========================================

    def makeUndirected(self, reconcile=None):
        """makeUndirected(reconcile=None): make the graph undirected, duplicating isolated arcs.
        When there are already two arcs between two nodes, and their weights are different,
        it calls the given reconcile function, that takes two weights as input, and chooses
        which one to keep (or raises an exception when needed). If reconcile isn't given, then
        it uses the standard one that always raises an exception.
        Few possible alternative reconcile functions:
        from random import random
        def reconcile(w1, w2): # Random choose.
            if random() <= 0.5: return w1
            else: return w2
        Another possible:
        def reconcile(w1, w2): # Always choose the first.
            return w1
        Another possible:
        def reconcile(w1, w2): # Average of two.
            return (w1+w2)/2
        Another possible:
        def reconcile(w1, w2): # Weight = None
            return None """
        # Structure must be fully coherent.
        if reconcile is None:
            def reconcile(w1, w2):
                s = "Between two nodes there are already two arcs with different weights: w1,w2= ("
                raise s + str(w1) + ", " + str(w2) + ")."

        self_i = self.i
        self_o = self.o
        for n1,a in self_o.iteritems():
            for n2,w12 in a.iteritems():
                if n1 != n2:
                    if n1 in self_o[n2]:
                        w21 = self_o[n2][n1]
                        if w12 != w21:
                            w = reconcile(w12, w21)
                            self_o[n1][n2] = w
                            self_i[n2][n1] = w
                            self_o[n2][n1] = w
                            self_i[n1][n2] = w
                    else:
                        self_o[n2][n1] = w12
                        self_i[n1][n2] = w12
                        self.arcCount += 1


    def copy(self):
        "copy(): return a shallow copy of the graph."
        return self.__class__(self)

    __copy__ = copy # For the copy module


    def transpose(self):
        """transpose(): return the transposed of the graph, that is the directed graph with all the
        arcs reversed (this operation is nearly instantaneous for this implementation)."""
        # Structure must be coherent!
        self.o, self.i = self.i, self.o


    def clear(self):
        "clear(): remove all elements from the graph."
        self.i.clear()
        self.o.clear()
        self.arcCount = 0
        self.nodeData.clear()
        self.nextNode = 0


    def complement(self, w=None):
        """complement(w=None): create the complement of the graph. nodeData of nodes are kept.
        Old arc weights are discarded, the new arcs have the optionally given weight w or None.
        Definition: the complement of a graph G is the graph G' with the same nodes, whose arcs
        are precisely those that are not in the arc set of G. Note that self loops are considered
        too."""
        # Another fast algoritm can be added for an very dense graph input.
        tresh = 0.3
        self_o = self.o
        self_i = self.i
        if not self_o: return # Empty graph.
        nodes = self_o.keys()
        lenNodes = len(nodes)
        if self.arcCount > lenNodes * (lenNodes+1) * tresh: # Dense enough graph
            arcCount = 0
            for n1 in nodes:
                for n2 in nodes:
                    if n2 in self_o[n1]:
                        del self_o[n1][n2]
                        del self_i[n2][n1]
                    else:
                        self_o[n1][n2] = w
                        self_i[n2][n1] = w
                        if n1 == n2:
                            arcCount += 2
                        else:
                            arcCount += 1
            self.arcCount = arcCount
        else: # It's a very sparse graph, then a different algoritm is faster:
            oldarcs = self.arcs()
            # Quickly create a clique
            auxd = dict.fromkeys(nodes, w)
            for n in nodes:
                self.i[n] = dict(auxd)
                self.o[n] = dict(auxd)
            arcCount = lenNodes * (lenNodes+1)
            for n1,n2 in oldarcs: # Remove old arcs from the clique:
                if n1 == n2:
                    arcCount -= 2
                else:
                    arcCount -= 1
                del self_o[n1][n2]
                del self_i[n2][n1]
            self.arcCount = arcCount


    def subgraphExtract(self, nodes):
        """subgraphExtract(nodes): return a subgraph of the graph, containing only nodes from
        nodes sequence (and contained in the graph), with only the arcs between such elements."""
        self_o = self.o
        self_i = self.i
        self_nodeData = self.nodeData
        arcCount = 0
        if isinstance(nodes, set):
            nodesset = nodes.intersection(self_o)
        else:
            nodesset = set(nodes).intersection(self_o)
        subgraph = self.__class__() # Necessary for a good subclassing.
        subgraph_o = subgraph.o
        subgraph_i = subgraph.i
        subgraph_nodeData = subgraph.nodeData
        for n1 in nodesset:
            subgraph_o[n1] = {}
            for n2,w in self_o[n1].iteritems():
                if n2 in nodesset:
                    subgraph_o[n1][n2] = w
            subgraph_i[n1] = {}
            for n2,w in self_i[n1].iteritems():
                if n2 in nodesset:
                    subgraph_i[n1][n2] = w
            if n1 in subgraph_o[n1]:
                arcCount += len(subgraph_o[n1]) + 1
            else:
                arcCount += len(subgraph_o[n1])
            if n1 in self_nodeData:
                subgraph_nodeData[n1] = self_nodeData[n1]
        subgraph.arcCount = arcCount
        subgraph.nextNode = self.nextNode
        return subgraph


    def __contains__(self, node):
        "__contains__: called in response to the expression 'node in self'"
        return node in self.o


    def degreeDict(self):
        """degreeDict(): return a dictionary of all (node, node_degree) of the graph.
        Self-loops are counted twice."""
        # Graph structure must be coherent.
        self_i = self.i
        result = {}
        for n,a in self.o.iteritems():
            result[n] = len(a) + len(self_i[n])
        return result


    def inboundDict(self):
        """inboundDict(): return a dictionary. Its keys are all the nodes of the graph.
        Its values are sets of their inbound arcs."""
        return dict(  (n,set(a)) for n,a in self.i.iteritems()  )


    def addArcs(self, seq, w=None, bi=False, paired=True):
        """addArcs(seq, w=None, bi=False, paired=True): add a sub-graph from a given sequence
        of arcs expressed as pairs of nodes, plus optional weight (default weight w=None).
        If bi=True, bidirectional arcs are added (with the same weight).
        If paired=False then seq is meant as a flattened sequence, to be paired.
        Example:
          g.addArcs(  [(1,2,5),(1,6),(3,1,None),(2,3,"a"),7,[],(8,)]  ) ==>
          g.o == {1: {2:5, 6:None}, 2: {3:'a'}, 3: {1:None}, 6:{}, 7:{}, 8:{}}
        That is:
        g.nodes() ==> [1,2,3,6,7,8]
        g.arcs() ==> [(1,2,5),(1,6,None),(3,1,None),(2,3,"a")]
        Another example:
        g.clear()
        g.addArcs([1,2,3,4,5,6], paired=False)
        print g ==>
        1>2  2  3>4  4  5>6  6 """
        self_o = self.o
        list_tuple = (list, tuple)
        # To not exaust an iterable just in the node creation:
        if not isinstance(seq, (list, tuple, set, dict)):
            seq = list(seq)
        if not paired:
            seq = zip(seq[::2], seq[1::2])
        # Create all possible nodes:
        for elem in seq:
            if isinstance(elem, list_tuple):
                le = len(elem)
                if le>0:
                    e0 = elem[0]
                    if e0 not in self_o:
                        self_o[e0] = {}
                if le>1:
                    e1 = elem[1]
                    if e1 not in self_o:
                        self_o[e1] = {}
            else:
                if elem not in self.o:
                    self_o[elem] = {}
        # Create arcs:
        if bi:
            for elem in seq:
                if isinstance(elem, list_tuple) and len(elem)>1:
                    n1,n2 = elem[0], elem[1]
                    if len(elem)>2: w = elem[2]
                    self_o[n1][n2] = w
                    self_o[n2][n1] = w
        else:
            for elem in seq:
                if isinstance(elem, list_tuple) and len(elem)>1:
                    if len(elem)>2:
                        self_o[elem[0]][elem[1]] = elem[2]
                    else:
                        self_o[elem[0]][elem[1]] = w
        self._regenerate()
        #return self


    def addMulti(self, seq, w=None, nodeData=None, bi=False):
        """addMulti(seq, w=None, nodeData=None, bi=False): add a sub-graph from a given sequence of
        groups node-arcs (nodes must be hashable). All weights are set to w (or None by default).
        Groups can be just pairs. Example: g.addMulti( [(1,2,6),2,(3,1),(1,6),[],[7]], w=0 )
        ==> g.o == {1: {2:None, 6:0}, 2: {}, 3: {1:0}, 6:{}, 7:{}}
        That is:
        g.nodes() ==> [1,2,3,6,7]
        g.arcsw() ==> [(1,2,0),(1,6,0),(3,1,0)] """
        self_o = self.o
        self_i = self.i
        # To not exaust an iterable just in the node creation:
        if not isinstance(seq, (list, tuple, set, dict)): seq = list(seq)
        list_tuple = (list, tuple)
        nodes = set()
        # Create all nodes:
        for elem in seq:
            if isinstance(elem, list_tuple):
                nodes.update(elem)
                for n in elem:
                    if n not in self_o:
                        self_o[n] = {}
                        self_i[n] = {}
            else:
                nodes.add(elem)
                if elem not in self_o:
                    self_o[elem] = {}
                    self_i[elem] = {}
        # Clear/update nodeDatas:
        if nodeData is None:
            for n in nodes:
                if n in self.nodeData:
                    del self.nodeData[n]
        else:
            for n in nodes:
                self.nodeData[n] = nodeData
        # Create arcs:
        if bi:
            for elem in seq:
                if isinstance(elem, list_tuple) and len(elem)>1:
                    elem_0 = elem[0]
                    for n in elem[1:]:
                        if n not in self_o[elem_0]:
                            if elem_0 == n:
                                self.arcCount += 2
                            else:
                                self.arcCount += 1
                        self_o[elem_0][n] = w
                        self_i[n][elem_0] = w
                        if elem_0 not in self_o[n]:
                            self.arcCount += 1
                        self_o[n][elem_0] = w
                        self_i[elem_0][n] = w
        else:
            for elem in seq:
                if isinstance(elem, list_tuple) and len(elem)>1:
                    elem_0 = elem[0]
                    for n in elem[1:]:
                        if n not in self_o[elem_0]:
                            if elem_0 == n:
                                self.arcCount += 2
                            else:
                                self.arcCount += 1
                        self_o[elem_0][n] = w
                        self_i[n][elem_0] = w
        #return self


    def addSource(self, node, nodeData=None, w=None):
        "addSource(node, nodeData=None, w=None): source is a node with arcs to all other nodes."
        self.addNode(node, nodeData)
        for n in self.o.iterkeys():
            if n != node:
                self.addArc(node, n, w) # this can be made faster.


    def addSink(self, node, nodeData=None, w=None):
        "addSink(node, nodeData=None, w=None): sink receives arcs from all other nodes."
        self.addNode(node, nodeData)
        for n in self.o.iterkeys():
            if n != node:
                self.addArc(n, node, w) # this can be made faster.


    def addClique(self, nodes, nodeData=None, w=None, loops=False):
        """addClique(nodes, nodeData=None, w=None, loops=False):
        add a clique (a complete subgraph) of given nodes.
        If loops==True then nodes are connected with themselves too."""
        if not isinstance(loops, bool):
            raise TypeError, "in addClique: loops isn't a bool but a " + str(type(loops))
        if isinstance(nodes, set):
            nodeset = nodes
            nodes = list(nodes)
        else:
            nodeset = set(nodes)
            nodes = list(nodeset) # To remove duplicated nodes (and to cheek their hashability).
        nodesn = len(nodes)
        if nodesn:
            self_o = self.o
            self_i = self.i
            if not self_o: # empty graph
                self.i = {}
                self.arcCount = nodesn * (nodesn+1)
                auxd = dict.fromkeys(nodes, w)
                self.i = dict( (n, dict(auxd)) for n in nodes )
                self.o = dict( (n, dict(auxd)) for n in nodes )
                self_o = self.o
                self_i = self.i
                if not loops: # removes self arcs if requested
                    self.arcCount -= (2*nodesn)
                    for n in nodes:
                        del self_o[n][n]
                        del self_i[n][n]
            else:
                for n in nodeset.difference(self_o): # create absent nodes
                    self_o[n] = {}
                    self_i[n] = {}
                for i,n1 in enumerate(nodes): # add arcs. This too can be speed up with a copy.
                    for j in xrange(i+1, nodesn):
                        n2 = nodes[j]
                        if n2 not in self_o[n1]:
                            self.arcCount += 1
                        if n1 not in self_o[n2]:
                            self.arcCount += 1
                        self_o[n1][n2] = w
                        self_o[n2][n1] = w
                        self_i[n1][n2] = w
                        self_i[n2][n1] = w
                if loops: # creates self arcs if requested
                    for n in nodes:
                        if n not in self_o[n]:
                            self.arcCount += 2
                        self_o[n][n] = w
                        self_i[n][n] = w
            if nodeData is None: # not present means None.
                for n in nodes:
                    if n in self.nodeData:
                        del self.nodeData[n]
            else:
                for n in nodes:
                    self.nodeData[n] = nodeData


    def addPath(self, nodes, nodeData=None, w=None, closed=False):
        """addPath(nodes, nodeData=None, w=None, closed=False):
        add a linear structure of chained nodes; open, or closed in a circle. Example:
          addPath(g.createID(50), closed=True)  """
        closed = bool(closed)
        self_o = self.o
        self_i = self.i
        nodes = _stableUnique(nodes) # To remove duplicated nodes keeping original order.
        nodesn = len(nodes)
        if nodesn > 0:
            if self_o == {}: # empty graph
                self.i = {}
                self_i = self.i
                for n in nodes: # create absent nodes
                    self_o[n] = {}
                    self_i[n] = {}
                self.arcCount = nodesn-1
                for i,n1 in enumerate(islice(nodes, nodesn-1)): # create chain of arcs
                    n2 = nodes[i+1]
                    self_o[n1][n2] = w
                    self_i[n2][n1] = w
            else:
                for n in nodes: # create absent nodes
                    if n not in self_o:
                        self_o[n] = {}
                        self_i[n] = {}
                for i,n1 in enumerate(islice(nodes, nodesn-1)): # create chain of arcs
                    n2 = nodes[i+1]
                    if n2 not in self_o[n1]:
                        self.arcCount += 1
                    self_o[n1][n2] = w
                    self_i[n2][n1] = w
            if closed:
                nodes0 = nodes[0]
                nodesm1 = nodes[-1]
                if nodes0 not in self_o[nodesm1]:
                    if nodes0 == nodesm1:
                        self.arcCount += 2
                    else:
                        self.arcCount += 1
                self_o[nodesm1][nodes0] = w
                self_i[nodes0][nodesm1] = w
            if nodeData is None: # not present means None.
                for n in nodes:
                    if n in self.nodeData:
                        del self.nodeData[n]
            else:
                for n in nodes:
                    self.nodeData[n] = nodeData


    def create2dGrid(self, nodes, columns, w=None, coords=False):
        """create2dGrid(nodes, columns, w=None, coords=False): create a 2D grid undirected graph,
        from the given sequence of nodes. Columns is the number of desired columns.
        len(nodes) must be divisible by columns. All arcs are created with the given weight w, or
        the default None. If coords is True, nodeData of nodes contains (x,y) coordinates of the
        node (integer coordinates). Example:
          g.create2dGrid(range(6), 3, w=0, coords=True) ==>
          g.nodeData = {0:(0,0), 1:(1,0), 2:(2,0), 3:(0,1), 4:(1,1), 5:(2,1)}
          g.short() = 0>1,3  1>0,2,4  2>1,5  3>0,4  4>1,3,5  5>2,4 """
        nodes = _stableUnique(nodes) # To remove duplicated nodes.
        if not isinstance(columns, (int, long, float)):
            raise TypeError, "in create2dGrid: columns isn't a int, long or float."
        if not isinstance(coords, bool):
            raise TypeError, "in create2dGrid: coords isn't a bool."
        columns = int(round(columns))
        nnodes = len(nodes)
        self.clear() # if nnodes==0 the graph must be cleaned.
        if columns <= 0 or nnodes <= 0:
            return # End.
        if nnodes % columns:
            raise TypeError,"Error in Graph.add2dGrid, len(nodes)%columns != 0"
        else:
            rowsm1 = nnodes / columns - 1
            columnsm1 = columns - 1
            self_o = self.o
            self_i = self.i
            # Create nodes:
            if coords:
                self_nodeData = self.nodeData
                for i,n in enumerate(nodes):
                    self_o[n] = {}
                    self_i[n] = {}
                    y,x = divmod(i, columns)
                    self_nodeData[n] = (x,y)
            else:
                for n in nodes:
                    self_o[n] = {}
                    self_i[n] = {}
            # Create arcs:
            for i,n in enumerate(nodes):
                y,x = divmod(i, columns)
                if x<columnsm1: self.addBiArc(n, nodes[i+1], w)
                if y<rowsm1: self.addBiArc(n, nodes[i+columns], w)
        #return self


    def addNcube(self, dim=3, nodes=None, w=None, nodeData=None):
        """addNcube(dim=3, nodes=None, w=None, nodeData=None): add to the self graph a graph
        with the structure of an dim-dimensional cube. All arcs are created bidirectional and have
        the given weight w, or None. Nodes are created with the given optional nodeData.
        nodes = optional list of 2**dim nodeIDs, they must not be present in the graph.
        If nodes==None then integer nodeIDs are created with createID."""
        """ Original algorithm that generates adjacent node IDs:
        self.clear()
        dim = int(round(dim))
        if dim>=0: self.addNode(0)
        for d in xrange(dim):
            aux = 2 ** d
            for n1 in xrange(aux):
                n1aux = n1 + aux
                for n2,w in self.o[n1].iteritems():
                    self.addArc(n1aux, n2+aux, w)
                self.addBiArc(n1, n1aux, w)
        return self """
        if not isinstance(dim, (int, long, float)):
            raise TypeError, "in addNcube: dim must be int, long or float"
        dim = int(round(dim))
        if nodes is None:
            nodes = self.createID(2 ** dim)
        else:
            nodes = _stableUnique(nodes) # To remove duplicated nodes keeping original order.
            if len(nodes) != 2**dim:
                return "Error in addNcube: wrong number of given nodes: " + str(len(nodes)) +\
                       " instead of " + str(2**dim)
            for n in nodes:
                if n in self.o:
                    return 'Error in addNcube: one or more nodeID is already present in the graph. First found: "' \
                           + str(n) + '".'
        if dim == 0:
            self.addNode(nodes[0], nodeData=nodeData)
        for d in xrange(2**dim):
            self.addNode(nodes[d], nodeData=nodeData)
        pos = dict( (e,i) for i,e in enumerate(nodes) )
        self_o = self.o
        self_i = self.i
        for d in xrange(dim):
            aux = 2 ** d
            for in1,n1 in enumerate(nodes[:aux]):
                n1aux = nodes[in1 + aux]
                so = self_o[n1aux]
                for n2,w in self.o[nodes[in1]].iteritems():
                    #The following means: self.addArc(n1aux, nodes[pos[n2]+aux], w)
                    n2aux = nodes[ pos[n2] + aux ]
                    so[n2aux] = w
                    self_i[n2aux][n1aux] = w
                #The following means: self.addBiArc(n1, n1aux, w)
                self_o[n1][n1aux] = w
                self_i[n1aux][n1] = w
                self_o[n1aux][n1] = w
                self_i[n1][n1aux] = w
        self.arcCount += dim * (2**dim) # add two times the edges of a dim-cube.
        return nodes


    def createRandom(self, nodes, arcProbability, nodeData=None, w=None, loops=False, bi=False):
        """createRandom(nodes, arcProbability, nodeData=None, w=None, loops=False, bi=False):
        create a random graph from the given sequence of nodes (and return it).
        Between each couple of nodes it is added a directed arc with given probability.
        If loops==True then nodes can be connected with themselves too.
        If bi==True arcs are created bidirectional (undirected graph)."""
        # A faster threshold can be 0.6, but del doesn't really remove elements from a dictionary:
        treshold = 0.7
        if not isinstance(loops, bool):
            raise TypeError, "in createRandomp: loops isn't a bool but a " + str(type(loops))
        if not isinstance(bi, bool):
            raise TypeError, "in createRandomp: bi isn't a bool but a " + str(type(bi))
        arcProbability = max(0.0, min(1.0, float(arcProbability)))
        self.clear()
        if len(nodes) == 0:
            return # End already.

        if arcProbability == 1.0: # Then adds a complete subgraph (a clique).
            self.addClique(nodes, nodeData=nodeData, w=w, loops=loops)
            return # End.

        if isinstance(nodes, set):
            nodes = list(nodes)
        else:
            nodes = list(set(nodes)) # To remove duplicated nodes (and to cheek their hashability).

        # Set nodeData:
        if nodeData != None:
            self.nodeData = {}.fromkeys(nodes, nodeData)

        if bi: # Undirected graph:
            nnodes = len(nodes)
            skip = int(not loops)
            if arcProbability > treshold:
                # Quickly creates a complete graph and then removes arcs
                self.addClique(nodes, nodeData=nodeData, w=w, loops=loops)
                self_o = self.o
                self_i = self.i
                # Remove arcs:
                for i,n1 in enumerate(nodes):
                    for j in xrange(i+skip, nnodes):
                        n2 = nodes[j]
                        if random() > arcProbability:
                            del self_o[n1][n2]
                            del self_i[n2][n1]
                            if n1 != n2:
                                del self_o[n2][n1]
                                del self_i[n1][n2]
                            self.arcCount -= 2 # Decreses of 2 for self-loops too!
            else:
                # Add all nodes:
                self_o = self.o
                self_i = self.i
                for n in nodes:
                    self_o[n] = {}
                    self_i[n] = {}
                # Add arcs:
                for i,n1 in enumerate(nodes):
                    for j in xrange(i+skip, nnodes):
                        n2 = nodes[j]
                        if random() <= arcProbability:
                            self_o[n1][n2] = w
                            self_i[n2][n1] = w
                            self_o[n2][n1] = w
                            self_i[n1][n2] = w
                            self.arcCount += 2
        else: # Directed graph:
            if arcProbability > treshold:
                # Quickly creates a complete graph and then removes arcs
                self.addClique(nodes, nodeData=nodeData, w=w, loops=loops)
                self_o = self.o
                self_i = self.i
                # Remove arcs:
                if loops:
                    for n1 in nodes:
                        self_o_n1 = self_o[n1]
                        for n2 in nodes:
                            if random() > arcProbability:
                                del self_o_n1[n2]
                                del self_i[n2][n1]
                                if n1 == n2:
                                    self.arcCount -= 2
                                else:
                                    self.arcCount -= 1
                else:
                    for n1 in nodes:
                        self_o_n1 = self_o[n1]
                        for n2 in nodes:
                            if n1!=n2 and random() > arcProbability:
                                del self_o_n1[n2]
                                del self_i[n2][n1]
                                self.arcCount -= 1
            else:
                # Add all nodes:
                self_o = self.o
                self_i = self.i
                for n in nodes:
                    self_o[n] = {}
                    self_i[n] = {}
                # Add arcs:
                if loops:
                    for n1 in nodes:
                        self_o_n1 = self_o[n1]
                        for n2 in nodes:
                            if random() <= arcProbability:
                                self_o_n1[n2] = w
                                self_i[n2][n1] = w
                                if n1 == n2:
                                    self.arcCount += 2
                                else:
                                    self.arcCount += 1
                else:
                    for n1 in nodes:
                        self_o_n1 = self_o[n1]
                        for n2 in nodes:
                            if n1!=n2 and random() <= arcProbability:
                                self_o_n1[n2] = w
                                self_i[n2][n1] = w
                                self.arcCount += 1
        # return self


    def createIntervalgGraph(self, seq, w=None):
        """createIntervalgGraph(seq, w=None): given a list, tuple or set seq containing *distinct*
        pairs (t0,t1) with t0<=t1, where t is int, long, or float, create an interval graph,
        whose nodes are the given pairs, and there is an arc between the (t0a,t1a) and (t0b,t1b)
        nodes if the [t0a,t1a] and [t0b,t1b] intervals intersection isn't empty.
        All intervals are closed, so the intersection between [1,2] and [2,5.1] is the point 2.
        Duplicated intervals are ignored.
        All arcs are created with the specified weight w, or with the default weight=None. Ex:
          g.createIntervalgGraph([ (1,4),(5,7),(8,11),(3,7.1),(5,7),(5,8) ])
          Produces the graph:
          (1,4)>(3,7.1) (3,7.1)>(1,4),(5,7),(5,8) (5,7)>(3,7.1),(5,8) (5,8)>(3,7.1),(5,7),(8,11)
          (8,11)>(5,8) """
        """
        Simple O(n^2) algorithm:
        nseq = len(seq)
        for i,ri in enumerate(seq):
            self.addNode( ri[0],ri[1] )
            for j in xrange(i+1, nseq):
                rj = seq[j]
                if intersection(ri, rj):
                    self.addBiArc(ri, rj)

        Original version of the O(n*log(n)) algorithm (addBiArc isn't expanded):
        s = []
        for i,(t0,t1) in enumerate(seq):
            s.extend( [ (t0,i,0), (t1,i,1) ] )
            self.addNode( (t0, t1) )
        s.sort( key=itemgetter(0) )
        d = set()
        for t1,i,p in s:
            if p:
                d.remove( (seq[i][0], i) )
            else:
                seqi = seq[i]
                for t2,j in d:
                    self.addBiArc(seqi, seq[j])
                d.add( (t1,i) )
        """
        self.clear()
        seq = list(set(seq))
        self_o = self.o
        self_i = self.i
        s = []
        for i,(t0,t1) in enumerate(seq):
            if t0>t1: # Cheek if the interval is okay:
                self.clear()
                raise TypeError, "createIntervalgGraph input error: t0>t1 for one or more intervals."
            s.extend( [ (t0,i,0), (t1,i,1) ] )
            n = (t0,t1)
            if n not in self_o:
                self_o[n] = {}
                self_i[n] = {}
        s.sort( key=itemgetter(0) )
        d = set()
        for t1,i,p in s:
            if p:
                d.remove( (seq[i][0], i) )
            else:
                n1 = seq[i]
                for t2,j in d:
                    n2 = seq[j]
                    if n2 not in self_o[n1]:
                        self.arcCount += 2
                    self_o[n1][n2] = w
                    self_i[n2][n1] = w
                    self_o[n2][n1] = w
                    self_i[n1][n2] = w
                d.add( (t1,i) )


    def createPetersen(self):
        "createPetersen(): delete the graph and create the Petersen Graph."
        self.clear()
        self.addMulti([[0,1,2,5],[1,3,8],[2,6,7],[3,4,7],[4,5,6],[5,9],[6,8],[7,9],[8,9]], bi=True)
        petcoords = [[28,394], [208,948], [264,470], [354,747], [500,299],
                     [500,51], [645,747], [735,470], [791,948], [971,394]]
        self.nodeData = dict( (i,coord) for i,coord in enumerate(petcoords) )


    def randomw(self, randw=None):
        """randomw(randw=None): assign random weights to all the arcs of the graph.
        rand is an optional given function that generates the random weight (default is random).
        Example: g.randomw( lambda:randint(1,6) ) """
        if randw is None:
            randw = random
        self_i = self.i
        self_o = self.o
        for n1,a in self_o.iteritems():
            for n2 in a.iterkeys():
                w = randw()
                self_o[n1][n2] = w
                self_i[n2][n1] = w


    def randomCoords(self, randx=None, randy=None):
        """randomCoords(randx=None, randy=None): assign random coordinates to all the nodes of
        the graph. randx and randy are optional given functions that generates the x and y
        coordinates (default is random). Examples:
          g.randomCoords( lambda:randint(0,100), lambda:randint(0,100) )
          g.randomCoords(lambda:gauss(1,1), lambda:gauss(1,1)) """
        if randx is None: randx = random
        if randy is None: randy = random
        self_nodeData = self.nodeData
        for n in self.o.iterkeys():
            self_nodeData[n] = ( randx(), randy() )


    def circularCoords(self, center=(0,0), radius=1):
        """circularCoords(center=(0,0), radius=1): assign coordinates to all the nodes of
        the graph, putting them on a circle. center and radius are an optional pair of coordinates
        and a number."""
        distance = 2 * pi / len(self.o)
        aux = 0
        if center==(0,0) and radius==1:
            for n in self.o.iterkeys():
                self.nodeData[n] = ( cos(aux), sin(aux) )
                aux += distance
        else:
            xcenter, ycenter = center
            for n in self.o.iterkeys():
                self.nodeData[n] = ( radius*cos(aux) + xcenter, radius*sin(aux) + ycenter )
                aux += distance


    def springCoords(self, iterations=50, restart=False):
        """springCoords(iterations=50, restart=False): spring force model layout.
        iterations: number of iteration of the algorigh, the more the better is the result, but it
          requires more time.
        restart: if it's False then it uses the coordinates of the nodes (stored in nodeData).
          This is useful to apply springLayout more than one time, until results are good enough."""
        # Layout (positioning) algorithms for graph drawing, adaptef from netwrorkX graph library,
        # revision 1033, Copyright (C) 2004,2005 by Aric Hagberg <hagberg@lanl.gov>
        # Dan Schult <dschult@colgate.edu>, Pieter Swart <swart@lanl.gov>
        # Distributed under the terms of the GNU Lesser General Public License
        # http://www.gnu.org/copyleft/lesser.html
        try:
            import numarray as num # faster
        except:
            try:
                import Numeric as num # slower
            except:
                return "springCoords impossibile: no libraries numarray or Numeric."

        dim = 2 # Dimention number of the layout, it's fixed to 2, but this algorithm works for more too.
        iterations = int(round(iterations))
        if iterations < 0:
            iterations = 0
        if restart or self.isEmbedded()!=True:
            # Set the initial positions randomly in 1^dim box
            rangedim = range(dim)
            vpos = dict( (v, num.array([random() for i in rangedim])) for v in self.xnodes() )
        else:
            vpos = dict( (node, num.array(self.nodeData[node])) for node in self )
        if iterations == 0:
            self.nodeData = dict( (k,tuple(v)) for (k,v) in vpos.iteritems() )
            return # Exit
        if self.order() == 0:
            self.nodeData = {}
            return # Exit
        else:
            # optimal distance between nodes
            k = num.sqrt( 1.0 / self.order() )
        disp = {}         # displacements

        # Initial "temperature" (about .1 of domain area) this is the largest step allowed in the
        #   dynamics linearly step down by dt on each iteration so on last iteration it is size dt.
        t = 0.1
        dt = 0.1 / float(iterations + 1)
        for i in xrange(iterations):
            for node1 in self.o.iterkeys(): # for node1 in self.nodes():
                disp[node1] = num.zeros(dim)
                for node2 in self.o.iterkeys(): # for node2 in self.nodes():
                    delta = vpos[node1] - vpos[node2]
                    dn = max(sqrt(num.dot(delta, delta)), 0.01)
                    # Repulsive force between all
                    deltaf = delta * k**2 / dn**2
                    disp[node1] = disp[node1] + deltaf
                    # Attractive force between neighbors
                    if node2 in self.o[node1]: # if self.hasArc(node1, node2):
                        deltaf = -delta * dn**2 / (k*dn)
                        disp[node1] = disp[node1] + deltaf

            # Update positions
            for node1 in self.o.iterkeys(): # for node1 in self.nodes():
                l = max( sqrt(num.dot(disp[node1], disp[node1])), 0.01 )
                vpos[node1] = vpos[node1] + disp[node1]*t/l
            t -= dt
        self.nodeData = dict( (k,tuple(v)) for (k,v) in vpos.iteritems() )


    def euclidify2d(self):
        """euclidify2d(): replace arc weights with the 2D Euclidean distance between incident nodes.
        nodeData must contain the x,y coordinate pair of all nodes."""
        self_nodeData = self.nodeData
        for n1,a in self.o.iteritems():
            n1nd = self_nodeData.get(n1, None)
            if isinstance(n1nd, (list, tuple)) and len(n1nd)==2:
                x1,y1 = n1nd
                for n2 in a.iterkeys():
                    n2nd = self_nodeData.get(n2, None)
                    if isinstance(n2nd, (list, tuple)) and len(n2nd)==2:
                        a[n2] = ( (x1 - self_nodeData[n2][0])**2 +
                                  (y1 - self_nodeData[n2][1])**2 ) ** 0.5


    def __hash__(self):
        # A frozengraph can be added for subgraphs and sets/dicts of graphs,
        #   but probably they aren't frequently useful.
        "__hash__(): a Graph cannot be hashed."
        raise TypeError, "A Graph is a mutable, and cannot be hashed."


    def __iter__(self):
        "__iter__(): for n in g. The same as xnodes."
        return self.o.iterkeys()


    def _regenerate(self):
        """_regenerate(): low level method: regenerate a new graph structure just on the base of
        the outbound arc dictionary and nodeData. It's useful after some "raw" low level
        operations on the graph."""
        self.i = {}
        self_i = self.i
        self_o = self.o
        an = 0
        for n in self_o.iterkeys():
            self_i[n] = {}
        for n1, outa in self.o.iteritems():
            an += len(outa)
            if n1 in outa: an += 1 # Add another 1 for loops.
            for n2, w in outa.iteritems():
                self_i[n2][n1] = w
        self.arcCount = an
        for n in self.nodeData.iterkeys():
            if n not in self_o:
                del self.nodeData[n]
        # for n in (set(self.nodeData) - set(self.o)): del self.nodeData[n] # faster?


    def _new(self, outboundDict, nodeData=None):
        """_new(outboundDict, nodeData=None): low level method: quickly reinitialize the
        graph from a given outbound arcs dictionary (as self.o) like those written by repr(g).
        nodeData dictionary can also be given. No safety cheeks are performed, use
        Graph(outboundDict, nodeData) if you want the safety cheeks."""
        # Few cheeks can be added!
        self.o = outboundDict
        if nodeData != None:
            self.nodeData = nodeData
        self._regenerate()


    # BINARY GRAPH OPERATORS: ===========================================

    def addUpdate(self, other):
        "addUpdate(other): update/overwrite the graph adding nodes and arcs present in another graph."
        self._testBinary(other, "addUpdate")
        for n in other.o.iterkeys():
            if n not in self.o:
                self.o[n] = dict( other.o[n] )
                self.i[n] = dict( other.i[n] )
            else:
                self.o[n].update( other.o[n] )
                self.i[n].update( other.i[n] )
        self.nodeData.update( other.nodeData )
        self.nextNode = max(self.nextNode, other.nextNode)
        self._recountArcs()


    def subUpdate(self, other):
        "subUpdate(other): update the graph deleting nodes and arcs present in a second graph."
        self._testBinary(other, "subUpdate")
        for n1, a1 in other.o.iteritems():
            if n1 in self.o:
                for n2 in a1.iterkeys():
                    self.delArc(n1,n2)
                if not self.o[n1]:
                    self.delNode(n1)
        self._recountArcs()


    def intersection(self, other):
        """intersection(other): return the intersection with a second graph.
        Weights/nodeData for shared arcs/nodes go into the intersection only if they are equal,
        otherwise they become None/absent."""
        # Both graphs must be coherent.
        # Possible oneliner: all but nodeData:
        #   return self.__class__().addNodes( set(self.xarcsw()).intersection(other.xarcsw()) )
        self._testBinary(other, "intersection")
        common = self.__class__() # Necessary for a good subclassing.
        for n1 in set(self.o).intersection(other.o): # filter(d1_has_key, d2)
            if n1 not in common.o:
                common.o[n1] = {} # add empty node.
                common.i[n1] = {}
            for n2 in set(self.o[n1]).intersection(other.o[n1]):
                if n2 not in common.o:
                    common.o[n2] = {} # add empty node.
                    common.i[n2] = {}
                aux = self.o[n1][n2]
                if aux == other.o[n1][n2]:
                    w = aux
                else:
                    w = None
                common.o[n1][n2] = w
                common.i[n2][n1] = w
                if n1 == n2:
                    common.arcCount += 2
                else:
                    common.arcCount += 1
            nd = self.nodeData.get(n1)
            if nd != None and nd == other.nodeData.get(n1):
                common.nodeData[n1] = nd
        common.nextNode = max(self.nextNode, other.nextNode)
        return common


    def nodeIntersection(self, other):
        "nodeIntersection(other): return the list of nodes shared between two graphs."
        # Both graphs must be coherent.
        self._testBinary(other, "nodeIntersection")
        self_o_has_key = self.o.has_key
        other_o = other.o
        return filter(self_o_has_key, other_o)


    def __eq__(self, other):
        "__eq__(): == between graphs."
        if isinstance(other, Graph):
            return self.o == other.o and self.i == other.i and \
                   self.arcCount == other.arcCount and self.nodeData == other.nodeData
        else:
            return False


    def __ne__(self, other):
        "__ne__(): != between graphs."
        if isinstance(other, Graph):
            return self.o != other.o or self.i != other.i or \
                   self.arcCount != other.arcCount or self.nodeData != other.nodeData
        else:
            return True


    def isOrientation(self, other):
        """isOrientation(other): return True if the self graph is an orientation of the other graph.
        This means it returns True if:
        1) Both graphs have one or more node.
        2) The other graph is undirected and without self-loops (in this implementation, a
           graph is undirected if for each node1->node2 arc, the node2->node1 arc exists too).
        3) The two graphs have exactly the same nodes.
        4) For each pair of arcs in the other graph, there is exactly one oriented arc in the
           self graph. In self there aren't other arcs. Arc weights are ignored."""
        self._testBinary(other, "isAnOrientationOf")
        if (not self.o) or (not other.o) or set(self.o) != set(other.o): return False
        if not other.loopCount: return False # Probably useless
        loops = [(n1,n2) for n1,a in self.o.iteritems() for n2 in a.iterkeys()]
        otherarcs = [(n1,n2) for n1,a in other.o.iteritems() for n2 in a.iterkeys()]
        setloops = set(loops)
        setloops.update( (b,a) for (a,b) in loops )
        return setloops==set(otherarcs) and len(loops)*2==len(otherarcs)


    def isIsomorphic(self, other, m):
        """isIsomorphic(other, m): given another graph, and a dictionary m containing
        a partial (or complete) node mapping (from the other to the self graph), return True if
        the two graphs/subgraphs are isomorphic. All arc weights and nodeData are ignored. Ex:
          g = Graph()
          g.addArcs([ (3,1), (3,2), (3,7) ])
          h = Graph()
          h.addArcs([ ("c","a"), ("c","d"), ("a",4) ])
          m = { "d":1, "a":2, "c":3}
          assert g.isIsomorphic(h, m) == True
        """
        self._testBinary(other, "isIsomorphicM")
        so = self.o
        oo = other.o
        smv = set(m.itervalues())
        for k,v in m.iteritems():
            # & is the set intersection.
            if v not in so  or k not in oo  or set(so[v])&smv != set(m[n] for n in oo[k] if n in m):
                return False
        return True


    def isomorphMap(self, other):
        """isomorphMap(other): return the mapping dictionary (from the other to the self graph)
        if the self graph is isomorphic to the other graph, otherwise return None. All arc
        weights and nodeData are ignored. This method is very slow, it can be used only for
        small graphs, up to about 12-13 nodes. For bigger graphs you can use Boost library:
        http://www.boost.org/libs/graph/doc/index.html
        For even bigger graphs (up to 1000 nodes) you can use nauty by Brendan McKay:
        http://cs.anu.edu.au/~bdm/nauty/ """

        def match(m, smv, selfnodesleft, othernodesleft):
            if not selfnodesleft:
                return m # Success
            else:
                for p1 in selfnodesleft:
                    for p2 in othernodesleft:
                        m[p2] = p1
                        smv.add(p1)
                        if p1 in so  and p2 in oo  and set(so[p1])&smv == set(m[n] for n in oo[p2] if n in m) \
                           and p1 in si  and p2 in oi  and set(si[p1])&smv == set(m[n] for n in oi[p2] if n in m):
                            selfnodesleft.remove(p1)
                            othernodesleft.remove(p2)
                            r = match(m, smv, selfnodesleft, othernodesleft)
                            selfnodesleft.add(p1)
                            othernodesleft.add(p2)
                            if r: return r
                        del m[p2]
                        smv.remove(p1)

        self._testBinary(other, "isomorphMap")
        if len(other) != len(self):
            return False
        else:
            so = self.o
            oo = other.o
            si = self.i
            oi = other.i
            return match({}, set(), set(so), set(oo))


    def _testBinary(self, other, sop):
        """_testBinary(other, sop): private method, used to test if the other object is a Graph
        too, useful for binary methods between graphs. Inspired by a similar method in sets module.
        sop is the name of the operation."""
        #if not isinstance(other, Graph):
        if not isinstance(other, type(self.__class__())):  # Is this more correct?
            raise TypeError, sop + " only permitted between graphs."


    # GRAPH STATS AND ANALYSIS: ===========================================

    def order(self):
        "order(): return the order of the graph, that is the number of its nodes."
        return len(self.o)

    def size(self):
        "size(): return the size of the graph, that is the number of its arcs (equal to len(graph))."
        return self.arcCount

    def __len__(self): # len(g)
        "__len__(): return the number of nodes of the graph (its order)."
        return len(self.o)

    def __nonzero__(self): # bool(g)
        "__nonzero__(): return if the graph is not empty."
        return bool(self.o)


    def isUndirected(self):
        """isUndirected(): return True if the graph is undirect. In directed graph, if there
        is an arc i,j with weight w, there there must be the arc j,i with the same weight w."""
        self_i = self.i
        for n1, a in self.o.iteritems():
            for n2, w in a.iteritems():
                if n1 not in self_i or n2 not in self_i[n1] or w != self_i[n1][n2]:
                    return False
        return True


    def isTournament(self):
        """isTournament(): return True is the graph is a tournament. A tournament is a graph with
        exactly one oriented arc between each pair of nodes, and without self-loops.
        An empty graph isn't a tournament."""
        if not self: return False
        self_o = self.o
        nodes = self_o.keys()
        nnodes = len(nodes)
        for i, n1 in enumerate(nodes):
            if n1 in self_o[n1]:
                return False
            for j in xrange(i+1, nnodes):
                n2 = nodes[j]
                if (n1 in self_o[n2]) == (n2 in self_o[n1]):
                    return False
        return True


    def maxDegree(self):
        "maxDegree(): return the maximum degree (the number of inbound + outbound arcs) of any node."
        self_i = self.i
        return max( [len(a)+len(self_i[n]) for n,a in self.o.iteritems()] )


    def loopCount(self):
        "loopCount(): return the number of nodes with an arc to themselves."
        return sum( n in a for n,a in self.o.iteritems() )


    def integerw(self):
        """integerw(): return True if all arcs have int or long weights.
        Return True if there aren't arcs."""
        int_long = (int, long)
        for arcs in self.o.itervalues():
            for w in arcs.itervalues():
                if not isinstance(w, int_long):
                    return False
        return True


    def realw(self):
        """realw(): return True if all arcs have int, long or float weights.
        Rreturn True if there aren't arcs."""
        float_int_long = (float, int, long)
        for arcs in self.o.itervalues():
            for w in arcs.itervalues():
                if not isinstance(w, float_int_long):
                    return False
        return True


    def startNodes(self):
        "startNodes(): return the set of all the nodes of the graph without any incoming arcs."
        return set( n for n,a in self.i.iteritems() if not a )


    def isIndependentSet(self, nodes):
        """isIndependentSet(nodes): a set of nodes in a graph is said to be an independent
        set of nodes if no two nodes in the set are adjacent."""
        if not self:
            return # Empty graph.
        self_o = self.o
        nodes = set(nodes)
        if nodes - set(self_o):
            return # Some nodes aren't present.
        for n in nodes:
            # if filter(self_o[n]._has_key, nodes): can be faster
            if set(self_o[n]).intersection(nodes):
                return False
        return True


    def connectedComponents(self):
        """connectedComponents(): return the list of the Connected Components of the graph.
        Return a list of lists of nodes. The connected components of a graph represent,
        in grossest terms, the pieces of the graph. Two nodes are in the same component if
        and only if there is some path between them. (Each arc is meant as bidirectional)."""
        self_o = self.o
        self_i = self.i
        result = []
        visited = set()
        for root in self.o.iterkeys():
            if root not in visited:
                component = [root]
                visited.add(root)
                Q = deque() # A queue
                Q.append(root)
                while Q:
                    n1 = Q.popleft()
                    for n2 in chain( self_o[n1].iterkeys(), self_i[n1].iterkeys() ):
                        if n2 not in visited:
                            visited.add(n2)
                            Q.append(n2)
                            component.append(n2)
                result.append(component)
        return result


    def shortestPath(self, n1, n2, weights=True):
        """shortestPath(n1, n2, weights=True): return the shortest path (based on arc weights)
        between two given nodes, using a Dijkstra algorithm (at the moment from an external module).
        If weights=False then all arc weights are meant as 1. If you want to use weights,
        self-loops must be all present, and usually their weights must be 0.
        g.shortestPath(n,n) ==> [n]
        Dijkstra's algorithm is only guaranteed to work correctly when all arc weights are positive."""
        return dijkstra.shortestPath(self.o, n1, n2, weights=weights)


    def shortestPaths(self, n, weights=True):
        """shortestPaths(n, weights=True): return the shortest paths (based on arc weights) from
        a given node to each other node, using a Dijkstra algorithm (from an external module).
        The output is a pair (D,P) where D[v] is the distance from start to v and P[v] is the
        predecessor of v along the shortest path from s to v.
        Note that the output containst only the nodes in the same connected component of n.
        If weights=False then all arc weights are meant as 1. If you want to use weights,
        self-loops must be all present, and usually their weights must be 0.
        Dijkstra's algorithm is only guaranteed to work correctly when all arc weights are positive."""
        if weights:
            return dijkstra.dijkstra(self.o, n)
        else:
            return dijkstra.dijkstraOnew(self.o, n)


    def toposort(self):
        """toposort(): return a list with the topological sorting of nodes. NOTE: if this returns
        a list with less nodes than the graph, then the graph contains one or more cycles."""
        # A dict of all (node, node_degree) of the Graph:
        indegree = dict( (n,len(ina)) for n,ina in self.i.iteritems() )
        queue = deque(n for n,deg in indegree.iteritems() if not deg)
        result = []
        while queue:
            n = queue.popleft()
            result.append(n)
            for to in self.o[n].iterkeys():
                indegree[to] -= 1
                if not indegree[to]:
                    queue.append(to)
        return result


    def allPairsShortestPaths(self, weights=True, forceInternal=False):
        """allPairsShortestPaths(weights=True, forceInternal=False): Floyd-Warshall all pairs
        shortest paths. Find the shortest distance between every pair of nodes in the graph. Return
        a matrix of distances, and the node sequence of the rows (it's the same for the columns).
        If there isn't a path between the two nodes, the matrix entry is sys.maxint = 2147483647
        If weights=False then all arc weights are meant as 1. If you want to use weights,
        self-loops must be all present, and usually their weights must be 0.
        If weights are 0, and g.hasLoop(n)==True, then g.shortestPath(n,n) ==> 0.
        forceInternal=True, then it force the use of the python algorithm.
        The algorithm works if there isn't a negative weight cycle in the graph.
        This algorithm should be used to compute shortest paths between
        every pair of nodes for dense graphs."""
        # For sparse graphs, use Johnson algorithm.
        # Code adapted from Program 16.17 of "Data Structures and Algorithms
        #   with Object-Oriented Design Patterns in Python" by Bruno R. Preiss.
        # Copyright (c) 2003 by Bruno R. Preiss, P.Eng. All rights reserved.
        # http://www.brpreiss.com/books/opus7/programs/pgm16_17.txt
        prgName = 'graph_apsp.exe'
        nodes = self.o.keys()
        nodeid = {}
        for i,n in enumerate(nodes):
            nodeid[n] = i
        n = len(nodes)
        for rightPath in filter(None, sys.path): # Find external executable
            try:
                open(rightPath + "\\" + prgName, "r")
            except IOError:
                rightPath = None
            else:
                break

        if rightPath and not forceInternal and not weights and \
            len(self.o)>5 and platform.startswith("win"):
            # call an external Delphi program (useful for "big" graphs):
            distance = []
            for n1,a in self.o.iteritems():
                row = ["0"] * n # matrix row initialization, uses 0 to reduce space
                for n2 in a.iterkeys():
                    row[nodeid[n2]] = "1"
                row.append( "\r" )
                distance.append( "".join(row) )
            p = Popen(prgName, stdin=PIPE, stdout=PIPE, shell=True, cwd=rightPath)
            for row in distance:
                p.stdin.write( row )
            txt = p.communicate()[0]
            distance = partition( map(int, txt.split()), n)
        else:
            # Do it in Python:
            row = [maxint] * n
            distance = [list(row) for i in xrange(n)] # Initialization of matrix of maxint
            if weights:
                for n1,a in self.o.iteritems():
                    distanceidn1 = distance[nodeid[n1]]
                    for n2,w in a.iteritems():
                        distanceidn1[nodeid[n2]] = w
            else: # Maybe there are faster algorithms for this
                for n1,a in self.o.iteritems():
                    distanceidn1 = distance[nodeid[n1]]
                    for n2 in a.iterkeys():
                        distanceidn1[nodeid[n2]] = 1
            for i in xrange(n):
                distancei = distance[i]
                for v in xrange(n):
                    distancev = distance[v]
                    for w in xrange(n):
                        if distancev[i] != maxint and distancei[w] != maxint:
                            d = distancev[i] + distancei[w]
                            if distancev[w] > d: distancev[w] = d

        if not weights:
            for n in nodes:
                nid = nodeid[n]
                distance[nid][nid] = 0
        return distance, nodes


    def stats(self):
        "stats(): return a list containing some statistics about the graph."
        result = []
        nnodes = len(self.o)
        result.append( ("Number of nodes", nnodes) )
        result.append( ("Number of arcs", self.arcCount) )
        if nnodes>0:
            meanout = sum( len(arcs) for arcs in self.o.itervalues() ) / (0.0 + nnodes)
        else:
            meanout = 0
        result.append( ("Average number of outbound (or inbound) neighbours", meanout) )
        result.append( ("Number of node data", len(self.nodeData)) )
        result.append( ("Indirected graph", self.isUndirected()) )
        result.append( ("Number of loops", self.loopCount()) )
        result.append( ("All arcs have int or long weights", self.integerw()) )
        result.append( ("All arcs have int, long or float weights", self.realw()) )
        result.append( ("Number of connected components", len(self.connectedComponents())  ) )
        result.append( ("Density", self.density()) )
        """
        Other possibilities:
        - is it Euclidean? (= arc weights are proportional to node Euclidean distance)
        - is it planar?
        - is it a power law graph?
        """
        return result


    def viewStats(self):
        """viewStats(): call the stats method, and return a formatted string containing some
        statistics on the graph."""
        result = ["Graph stats:"]
        for string, val in self.stats():
            result.append( string + ": " + str(val) )
        return "\n".join(result)


    def density(self):
        """density(): return the density of the graph, computed as:
          DirectedArcNumber / ( NodeNumber * (NodeNumber+1) )
        Note that self-loops count twice.
        output=0.0 means that the graph hasn't any directed arcs (or the graph is empty).
        output=1.0 means that the graph is complete (with self-loops too)."""
        if self:
            return (0.0+self.arcCount) / ( len(self.o) * (len(self.o)+1) )
        else:
            return 0


    def isRegular(self):
        """isRegular(): return True if the graph is regular. An empty graph is not regular.
        A graph is regular if every vertex has the same degree.
        (The degree is the number of inbound + outbound arcs of a node, with loops counted twice)."""
        if not self.o:
            return False
        randomNode = self.o.iterkeys().next()
        self_i = self.i
        degree = len(self.o[randomNode]) + len(self_i[randomNode])
        for n,a in self.o.iteritems():
            if len(a)+len(self_i[n]) != degree:
                return False
        return True

    def isKregular(self, k):
        """isKregular(k): return True if the graph is k-regular. An empty graph is not regular.
        A graph is k-regular if every vertex has degree k.
        (The degree is the number of inbound + outbound arcs of a node, with loops counted twice)."""
        if not self.o:
            return False
        self_i = self.i
        for n,a in self.o.iteritems():
            if len(a)+len(self_i[n]) != k:
                return False
        return True

    def isBiregular(self):
        """isBiregular(): return True if the graph is biregular. An empty graph is not biregular.
        A graph is biregular if it has unequal maximum and minimum degrees and every node
        has one of those two degrees.
        (The degree is the number of inbound + outbound arcs of a node, with loops counted twice)."""
        if not self.o:
            return False
        degrees = set()
        self_i = self.i
        for n,a in self.o.iteritems():
            d = len(a) + len(self_i[n])
            if d not in degrees:
                if len(degrees) >= 2:
                    return False
                else:
                    degrees.add(d)
        return len(degrees) == 2

    def isCubic(self):
        """isCubic(): return True if the graph is cubic. An empty graph is not cubic.
        A 3-regular graph is said to be cubic, or trivalent.
        A graph is k-regular if every vertex has degree k.
        The degree is the number of inbound + outbound arcs of a node, with loops counted twice)."""
        return self.isKregular(3)

    isTrivalent = isCubic


    def isConnected(self):
        """isConnected(): return true if the graph is connected.
        A graph is connected if there is a path connecting every pair of nodes. A graph that is not
        connected can be divided into connected components (disjoint connected subgraphs)."""
        return len(self.o) == len(self.DFS(self.firstNode(), direction=0))


    def eccentricity(self, node=None, weights=False):
        """eccentricity(node=None, weights=False): return the eccentricity of each node n of graph
        (that is the length of the longest shortest path from node), and a list of node mapping.
        If node is given return its eccentricity, without mapping, and return sys.maxint if the node
        isn't connected.
        If weights=True then arc weights count too. This is usually False. If you want to use
        weights, self-loops must be all present, and usually their weights must be 0."""
        # If the graph contains a node called None, then there can be problems.
        if node is None:
            mat, mapping = self.allPairsShortestPaths(weights=weights)
            return map(max, mat), mapping
        else:
            return max( self.shortestPaths(node, weights=weights)[0].values() )


    def diameter(self, weights=False):
        """diameter(weights=False): return the diameter of graph, that is the length of the longest
        shortest path between any two nodes. Return -1 if the graph isn't connected, 0 if empty.
        If weights=True then arc weights count too. This is usually False. If you want to use
        weights, self-loops must be all present, and usually their weights must be 0."""
        if not self.o:
            return 0
        if self.isConnected():
            d = max( self.eccentricity(weights=weights)[0] )
            if d == maxint:
                return -1
            else:
                return d
        else:
            return -1


    def radius(self, weights=False):
        """radius(weights=False): return the radius of graph, that is the minimum eccentricity of any node.
        Return -1 if all the graph nodes are unconnected.
        If weights=True then arc weights count too. This is usually False. If you want to use
        weights, self-loops must be all present, and usually their weights must be 0."""
        if not self.o:
            return 0
        e = min( self.eccentricity(weights=weights)[0] )
        if e == maxint:
            return -1
        else:
            return e


    def diameterRadius(self, weights=False):
        """diameterRadius(weights=False): return the diameter and radius of graph, that is the maximum and minimum
        eccentricity of any node. Return (0,0) if the graph is empty.
        This is faster than calling both methods because it computes the eccentricity one time only.
        Return diameter=-1 if the graph isn't connected.
        Return radius=-1 if all the nodes are unconnected.
        If weights=True then arc weights count too. This is usually False. If you want to use
        weights, self-loops must be all present, and usually their weights must be 0."""
        if not self.o:
            return 0, 0
        e = self.eccentricity(weights=weights)[0]
        r = min(e)
        d = max(e)
        if r == maxint: r = -1
        if d == maxint: d = -1
        return d, r


    def levelStructure(self, rootNode, weights=False):
        """levelStructure(rootNode, weights=False): return the level structure of given root node.
        The result is a dictionary, keys=distances, values=nodes with that distance from rootNode,
        Example: {0: ["A"], 1: ["C"], 2: ["B", "D", "K"]}
        If weights=False then arc weights are meant as 1. Usually it is False. If you want to use
        weights, self-loops must be all present, and usually their weights must be 0.
        A level structure of a graph is a partition of the set of nodes (only nodes in the
        connected component of rootNode) into equivalence classes of nodes with the same distance
        from a given root node. See also: http://en.wikipedia.org/wiki/Level_structure """
        if self and rootNode in self:
            result = {}
            distances = self.shortestPaths(rootNode, weights=weights)[0]
            for n, dist in distances.iteritems():
                if dist in result:
                    result[dist].append(n)
                else:
                    result[dist] = [n]
            return result


    def mostDistantNodes(self, node, weights=False):
        """mostDistantNodes(node, weights=False): return a list of the nodes most distant from the
        given node (in the same connected component), and their distance (that is the eccentricity
        of node). Note that all nodes in the result have the same distance from node.
        If Weights=False then all arc weights are meant as 1. It is usually False. If you want
        to use weights, self-loops must be all present, and usually their weights must be 0."""
        nodesMaxd = []
        maxd = 0
        if self and node in self:
            distances = self.shortestPaths(node, weights=weights)[0]
            for n,d in distances.iteritems():
                if d > maxd:
                    maxd = d
                    nodesMaxd = [n]
                elif d == maxd:
                    nodesMaxd.append(n)
        return nodesMaxd, maxd


    def pseudoperipheralNode(self, startNode=None):
        """pseudoperipheralNode(startNode=None): return one pseudo-peripheral node of the graph.
        A peripheral node is often hard to calculate, but sometimes a pseudo-peripheral node can be
        enough. As starting point it uses the given startNode, or the first node of the graph.
        See: http://en.wikipedia.org/wiki/Pseudo-peripheral_vertex """
        # Algorithm:
        # 1) choose a random node n1
        # 2) compute distance from n1 to each other node
        # 3) mostDistant = {nodes most far away from node}
        # 4) choose a vertex n2 in mostDistant with minimal degree
        # 5) if eccentricity(n2) > eccentricity(n1)
        #   then set node1=node2 and repeat with step 2
        #   else node2 is a pseudo-peripheral node

        # 1) choose a random node n1
        if self:
            if startNode is None or startNode not in self:
                n1 = self.firstNode()
            else:
                n1 = startNode

            # 2) compute distance from n1 to each other node
            # 3) mostDistant = {nodes most far away from node}
            mostDistant, n1Ecc = self.mostDistantNodes(n1)
            while 1:
                # 4) choose a vertex n2 in mostDistant with minimal degree
                n2 = mostDistant[0]
                minDegree = len(self.o[n2]) + len(self.i[n2])
                for n in mostDistant[1:]:
                    ndegree = len(self.o[n]) + len(self.i[n])
                    if ndegree < minDegree:
                        n2 = n
                        minDegree = ndegree

                # 5) if eccentricity(n2) > eccentricity(n1)
                #   then set node1=node2 and repeat with step 2
                #   else node2 is a pseudo-peripheral node
                mostDistant, n2Ecc = self.mostDistantNodes(n2)
                if n2Ecc > n1Ecc:
                    n1 = n2
                    n1Ecc = n2Ecc
                else:
                    break
            return n2


    def isEmbedded(self):
        """isEmbedded(): return True if all nodes of the graph have good 2D coordinates in
        their nodeData, otherwise return an error string message. Return True for an empty graph."""
        if not self:
            return True
        number = (int, long, float)
        for n in self.o.iterkeys():
            if n not in self.nodeData:
                return "Error: one or more node coordinates are lacking."
            else:
                ndata = self.nodeData[n]
                if not isinstance(ndata, (list, tuple)):
                    return "Error: one or more node coordinates aren't a list or tuple."
                else:
                    if len(ndata) != 2:
                        return "Error: one or more node coordinates aren't pairs."
                    else:
                        x,y = ndata
                        if not isinstance(x, number) or not isinstance(y, number):
                            return "Error: one or more node coordinates aren't int, long or float."
        return True


    def _methods(self):
        "_methods(): return a formatted string with all the methods of the class Graph."
        lm = {}.fromkeys( dir(Graph) )
        todelete = """__delattr__ __dict__ __getattribute__ __module__ __new__ __reduce__ __copy__
                   __reduce_ex__ __setattr__ __slot__ __weakref__ __str__ __class__ __doc__""".split()
        for e in todelete:
            del lm[e]
        lm = sorted(lm, key=lambda s: s.lower())
        # this graph can probably become self.__class__
        result = "\n".join( eval( "Graph." + e + ".__doc__" )  for e in lm)
        return result.replace("        ", "   ")


    def __getattr__(self, name):
        """If a wrong method is called, this suggests methods with similar names."""
        toRemove = """__delattr__ __dict__ __getattribute__ __module__ __new__
                      __reduce__ __copy__ __reduce_ex__ __setattr__ __slot__
                      __weakref__ __str__ __class__ __doc__""".split()
        methods = set(dir(self.__class__)).difference(toRemove)
        suggestions = get_close_matches(name.lower(), methods, 5)
        raise_comment = "method '%s' not found.\n" % name
        raise_comment += "Most similar named ones: %s\n\n" % ", ".join(suggestions)
        first_lines = []
        for method in suggestions:
            doc = getattr(self.__class__, method).__doc__
            if doc:
                first_lines.append(doc.splitlines()[0])
            else:
                first_lines.append(method + " - no docstring found.")
        raise AttributeError, raise_comment + "\n".join(first_lines)


    # GRAPH REPRESENTATION: ===========================================

    def __repr__(self):
        """__repr__(): return a textual representation of the graph, suitable, for creating the
        same structure. The representation contains only a dictionary of outbound arcs with their
        weights, and the nodeData, if present. (The __init__ method can be rebuild the other
        information)."""
        if not self.o:
            return "Graph()"
        if self.nodeData:
            return "".join(["Graph(", repr(self.o), ", ", repr(self.nodeData), ")"])
        else:
            return "".join(["Graph(", repr(self.o), ")"])


    def short(self, out=True, showw=False, hidew=None, all=False, separator="  "):
        """short(self, out=True, showw=False, hidew=None, all=False, separator="  "): a short
        representation of the graph without nodeData. You can use ushort for an even shorter
        representation of undirected graphs.
        out=True shows only the outbound arcs of each node.
        out=False shows only the inbound arcs of each node.
        If showw=True show weights too (separated by /), but don't show weights equal to hidew.
        separator is the string that separates the nodes.
        If all=False and the graph is very big, it shows just a shortened representation. If all=True
        then it forces to show all the graph.
        Note that > means outbound, < inbound arcs, and - means bidirectional ones for undirected
        graphs. For exampe, this graph (as adjacency matrix):
             0 1 2
        0: | 0 1 1 |
        1: | 1 0 1 |
        2: | 1 1 0 |
        Prints as:
        0-1,2  1-2 """
        if out:
            aux = self.o
            direction = ">"
        else:
            aux = self.i
            direction = "<"
        if showw:
            def mapw(n):
                if self.o[node][n]==hidew:
                    return str(n)
                else:
                    return str(n) + "/" + str(self.o[node][n])
        else:
            mapw = str

        all_nodes_repr = []
        for node in _mysorted(aux):
            node_repr = []
            node_repr.append(str(node))
            arcs = aux[node].keys()
            if arcs:
                node_repr.append(direction)
                node_repr.append(  ",".join( map(mapw, _mysorted(arcs)) )  ) # append all arcs of node.
            all_nodes_repr.append("".join(node_repr))
        result = separator.join(all_nodes_repr)
        if not all and len(result)>3200:
            truncate = 2500
            trailing = 100
            result2 = result[:truncate] + "... <~"
            result2 += str(int(round(len(result)-truncate-trailing,-1)))
            result2 += " chars> ..." + result[-trailing:]
            result2 += " (Shortened a very big output. Use all=True to see it all.)"
            result = result2
        return result


    def ushort(self, showw=False, hidew=None, all=False, separator="  "):
        """ushort(self, showw=False, hidew=None, all=False, separator="  "): a short representation of
        the undirected graph without nodeData. Arcs are shown only once (use the method "short" to see
        all arcs twice). In this class ushort is the standard textual representation of the graph.
        If showw=True it shows weights too (separated by /), but it doesn't show weights equal to hidew.
        separator is the string that separates the nodes.
        If all=False and the graph is very big, it shows just a shortened representation. If all=True
        then it forces to show all the graph.
        Note that > means outbound, < inbound arcs, and - means bidirectional ones for undirected
        graphs. For exampe, this graph (as adjacency matrix):
             0 1 2
        0: | 0 1 1 |
        1: | 1 0 1 |
        2: | 1 1 0 |
        Prints as:
        0-1,2  1-2 """
        def _mymax(a,b): # Necessary for unsortable nodes.
            if str(a)>str(b):
                return a
            else:
                return b

        def _mymin(a,b): # Necessary for unsortable nodes.
            if str(a)<str(b):
                return a
            else:
                return b

        if not self.isUndirected():
            return self.short(showw=showw, hidew=hidew, all=all, separator=separator)

        auxg = self.copy()
        for n1,n2 in auxg.arcs():
            if n1!=n2:
                auxg.delArc( _mymax(n1,n2), _mymin(n1,n2) )
        nodes = auxg.nodes()
        try:
            nodes.sort()
        except TypeError:
            sortable = False
        else:
            sortable = True
        if sortable:
            arcs = [ (n, sorted(auxg.outNodes(n))) for n in nodes ]
        else:
            arcs = [ (n, auxg.outNodes(n)) for n in nodes ]
        seennodes = set()
        arcs2 = []
        for n,a in arcs:
            if not (n in seennodes and not a):
                arcs2.append( (n,a) )
            seennodes.update(a)

        if showw:
            def mapw(n):
                if self.o[node][n]==hidew:
                    return str(n)
                else:
                    return str(n) + "/" + str(self.o[node][n])
        else:
            mapw = str

        all_nodes_repr = []
        for node, arcs3 in arcs2:
            node_repr = []
            node_repr.append(str(node))
            if arcs3:
                node_repr.append("-")
                node_repr.append(  ",".join( map(mapw, arcs3) )  ) # append all arcs of node.
            all_nodes_repr.append("".join(node_repr))
        result = separator.join(all_nodes_repr)
        if not all and len(result)>3200:
            truncate = 2500
            trailing = 100
            result2 = result[:truncate] + "... <~"
            result2 += str(int(round(len(result)-truncate-trailing,-1)))
            result2 += " chars> ..." + result[-trailing:]
            result2 += " (Shortened a very big output. Use all=True to see it all.)"
            result = result2
        return result


    def __str__(self):
       """__str__(): called by print(agraph). Call short() method, and return a short representation
       of the graph, without weights and nodeData. Shows only the outbound arcs of each node."""
       return self.ushort()


    def __unicode__(self):
        """__unicode__(): return a unicode textual representation of the graph, suitable, for
        creating the same structure. The representation contains only a dictionary of outbound
        arcs with their weights, and the nodeData, if present. (The __init__ method can be
        rebuild the other information)."""
        if not self.o:
            return u"Graph()"
        if self.nodeData:
            return "".join(["Graph(", unicode(self.o), ", ", unicode(self.nodeData), ")"])
        else:
            return "".join(["Graph(", unicode(self.o), ")"])


    def _matrixView(self, mat):
        """_matrixView(mat): private method used by *view methods; it converts mat into a
        string. See aform.__doc__ for the description of the structure of mat."""
        (origmatrix, origxlabels, origylabels, title, mapping) = mat
        xlabels = map(str, origxlabels)
        ylabels = map(str, origylabels)
        if len(xlabels) == 0 or len(ylabels) == 0:
            return "The graph is empty."
        # maps the matrix to strings.
        matrix = [[mapping.get(e, str(e)) for e in row] for row in origmatrix]

        lenmaxy = max(map(len, ylabels)) # Max length of ylabels column.
        ylabels = [e.rjust(lenmaxy) for e in ylabels] # ylabels justification.

        lenmaxx = map(len, xlabels) # Max length of every column.
        for row in matrix:
            for i,e in enumerate(row):
                lenmaxx[i] = max(lenmaxx[i], len(e))

        xlabels = [e.ljust(lenmaxx[i]) for i,e in enumerate(xlabels)] # xlabels justification.

        # matrix justification:
        matrix = [[d.rjust(lenmaxx[x]) for x,d in enumerate(row)] for row in matrix]

        # final string creation:
        rowstrings = [ title + ":" ]
        rowstrings.append( " "  * (lenmaxy+4) + " ".join(xlabels) )
        for y,label in enumerate(ylabels):
            line = label + ": | " + " ".join(matrix[y]) + " |"
            rowstrings.append( line )
        return "\n".join(rowstrings)


    def _compactBitMatrixView(self, mat):
        """_compactBitMatrixView(mat): private method used by *view methods; it converts
        mat into a string. Useful for a compact representation for aview, without labels.
        See aform.__doc__ for the description of the structure of mat."""
        # This outputs a binary matrix, so each loop counts as 1.
        matrix, xlabels, ylabels, title, mapping = mat
        if len(xlabels) == 0 or len(ylabels) == 0: return "The graph is empty."
        result = [ "".join( mapping.get(e, str(e)) for e in row ) for row in matrix ]
        return "\n".join( [title + " (compact version):"] + result )


    def aform(self):
        """aform(): return the graph represented as an Adjacency Matrix, inside a mat structure.
        A graph with n nodes can be represented as a Adjacency Matrix of n rows and n columns;
        the (i,j) entry of the matrix is 1 if there is an arc from node i to node j, 0 otherwise.
        mat is a tuple of: (matrix, xlabels, ylabels, title, mapping):
        - matrix is a list of lists (0,0 is in the upper left).
        - xlabels and ylabels are lists usually containing node or arc IDs.
        - title is the name of the representation (Adjacency Matrix, Incidence Matrix,
          Adjacency Matrix weights).
        - mapping is an optional dictionary that helps mapping elements of the matrices to strings.
            For Incidence Matrix: {0:" .", 1:" 1", -1:"-1", 2:" 2"}
            For Adjacency Matrix: {0:".", 1:"1"} """
        title = 'Adjacency matrix (1=arc present, 2=self loop, "." or 0=absent)'
        xlabels = _mysorted(self.o.keys())
        ylabels = xlabels
        mapping = {0:".", 1:"1"}
        matrix = [ [int(n2 in self.o[n1]) for n2 in xlabels] for n1 in xlabels]
        for i in xrange(len(xlabels)): matrix[i][i] *= 2 # self loops = 2
        return (matrix, xlabels, ylabels, title, mapping)


    def wform(self):
        """wform(): return the graph represented as Adjacency Matrix, but with arc weights instead
        of binary values.
        See aform.__doc__ for the description of mat structure and the Adjacency Matrix."""
        title = 'Adjacency Matrix of weights (values = arc weights, "." = absent arc)'
        xlabels = _mysorted(self.o.keys())
        ylabels = xlabels
        mapping = {}
        matrix = [ [self.o[n1].get(n2, ".") for n2 in xlabels] for n1 in xlabels]
        return (matrix, xlabels, ylabels, title, mapping)


    def iform(self):
        """iform(): return the graph represented as the Incidence Matrix.
        It is a matrix M that represents the incidence of arcs to nodes in the graph.
        If the arc is directed from i to j, then M(i,k)=-1, and M(j,k)=1. In this implementation
        self-loops are represented with 2. See aform.__doc__ for the description of mat structure."""
        """Possibile improvement: for undirected graphs it can show less columns using only:
        1=arc, 2=self loop, "."= nothing.
        und = self.isUndirected()
        if und:
            title = 'Incidence Matrix (1=outbound arc, -1=inbound arc, 2=self loop, 0 or "."= nothing)'
            mapping = {0:" .", 1:" 1", -1:"-1", 2:" 2"}
        else:
            title = 'Incidence Matrix (the graph is indirect) (1=arc, 2=self loop, 0 or "."= nothing)'
            mapping = {0:" .", 1:" 1", 2:" 2"} """
        def auxFun(y, n1, n2):
            if y == n1 == n2:
                return 2
            if y == n1:
                return 1
            if y == n2:
                return -1
            return 0

        ylabels = _mysorted(self.o.keys())
        title = 'Incidence Matrix (1=outbound arc, -1=inbound arc, 2=self loop, 0 or "."= nothing)'
        mapping = {0:" .", 1:" 1", -1:"-1", 2:" 2"}
        arcs = _mysorted(self.arcsw())
        xlabels = [w for (n1,n2,w) in arcs]
        matrix = [ [auxFun(y,n1,n2) for (n1,n2,w) in arcs] for y in ylabels ]
        return (matrix, xlabels, ylabels, title, mapping)


    def lform(self):
        """lform(): return a string with the graph represented as Adjacency List.
        vet is a tuple of: (vector, ylabels, title):
        - vector is the list of outbound neighbours and the weights (n2,w) for each node.
        - ylabels are lists usually containing node IDs.
        - title is the name of the representation (Adjacency List)."""
        title = 'Adjacency List (node: outbound neighbours:weights )'
        ylabels = _mysorted(self.o.iterkeys())
        vector = [ _mysorted(self.o[n1].iteritems()) for n1 in ylabels ]
        return (vector, ylabels, title)


    def aview(self, compact=False):
        """aview(compact=False): return a string with the graph represented as Adjacency Matrix.
        If compact=True, it shows a more compact binary matrix, without node labels.
        A graph with n nodes can be represented as a Adjacency Matrix of n rows and n columns;
        the (i,j) entry of the matrix is 1 if there is an arc from node i to node j, 0 otherwise."""
        if compact:
            return self._compactBitMatrixView(self.aform())
        else:
            return self._matrixView(self.aform())


    def wview(self):
        """wview(): return a string with the graph represented as Adjacency Matrix, but with
        arc weights instead of binary values. See aform.__doc__ for more info."""
        return self._matrixView(self.wform())


    def iview(self):
        """iview(): return a string with the graph represented as Incidence Matrix.
        It is a matrix M that represents the incidence of arcs to nodes in the graph.
        If the arc is directed from i to j, then M(i,k)=-1, and M(j,k)=1. In this implementation
        self-loops are represented with 2. See aform.__doc__ for more info."""
        return self._matrixView(self.iform())


    def lview(self, viewNodeData=False):
        """lview(viewNodeData=False): return a string with the graph represented as Adjacency Lists.
        In each line there is a node (optionally followed by its nodeData), followed by its
        outbound arcs."""
        (vector, ylabels, title) = self.lform()
        if viewNodeData:
            ylabels = [ str(y)+"|"+str(self.nodeData.get(y, "")) for y in ylabels ]
        else:
            ylabels = map(str, ylabels)
        if len(ylabels) == 0: return "The graph is empty."

        lenmaxy = max(map(len, ylabels)) # Max length of ylabels column.
        ylabels = [e.ljust(lenmaxy) for e in ylabels] # ylabels justification.

        # Final string creation:
        result = [ title + ":" ]
        for i,row in enumerate(vector):
            line = ylabels[i] + ": "
            line += " ".join( [str(n2)+":"+str(w) for n2,w in row] )
            result.append( line )
        return "\n".join(result)


    sview = short # Synonim of short method.


    def aplot(self):
        """aplot(): show the adjacency matrix of the graph (structure plot) using MatPlotLib.
        A graph with n nodes can be represented as a Adjacency Matrix of n rows and n columns;
        the (i,j) entry of the matrix is 1 if there is an arc from node i to node j, 0 otherwise.
        Loops are counted as 1."""
        try: # Import MatPlotLib if available.
            from pylab import imshow, show, cm
            from numarray import asarray
        except ImportError:
            return "MatPlotLib library (http://matplotlib.sourceforge.net) cannot be imported."
        else:
            lmax = 400
            sortedNodes = _mysorted(self.o.keys())
            if len(sortedNodes) <= lmax: # If the sparse matrix is small enough:
                # Then show it:
                matrix = [ [int(n2 in self.o[n1]) for n2 in sortedNodes] for n1 in sortedNodes]
                matrix = asarray(matrix, type="UInt8") # for numarray
                imshow(matrix, cmap=cm.gray, interpolation="nearest")
            else:
                # Else show a 2D density plot, with lmax*lmax bins.
                div = len(sortedNodes) / (0.0+lmax)
                pos = {}
                for i,n in enumerate(sortedNodes): pos[n] = int(i // div) # node=>bin conversion
                # This is much faster than filling a numarray matrix!
                row = [0] * lmax # Row of matrix full of 0
                matrix = [ list(row) for n in xrange(lmax)] # matrix full of 0
                del row
                for n1, a in self.o.iteritems():
                    for n2 in a.iterkeys():
                        matrix[pos[n1]][pos[n2]] += 1
                matrix = asarray(matrix)
                imshow(matrix, interpolation="nearest")
            show()
            return "MatPlotLib successiful structure plot show."


    def plot2d(self, arcs=True, nodes=True, plotRange=None, grid=None, axes=False, nodeLabels=True):
        """plot2d(arcs=True, nodes=True, plotRange=None, grid=None, axes=False, nodeLabels=True):
        plot the graph in 2D using node coordinates contained in nodeData.
        If arcs=False don't show arcs. If nodes=False don't show nodes. Directed arcs are blue,
        undirected arcs are black. Bidirectional arcs with different weights are black too.
        Self-loops are green. plotRange must be a sequence of 4 coordinates (minx, miny, maxx, maxy).
        plotRange=None ==> full auto.
        grid must be a number, representing the space between the grid lines.
          grid=None ==> no grid and axes.
        If axes=True show axes too.
        If NodeLabels=True show node IDs too beside nodes."""
        if plotRange!=None and not isinstance(plotRange, (list, tuple)):
            raise TypeError, "in plot2d: plotRange isn't None, list or tuple."
        if grid!=None and not isinstance(grid, (int, long, float)):
            raise TypeError, "in plot2d: grid isn't None, int, long or float."
        if grid <= 1e-10: grid = None
        if plotRange!=None and len(plotRange)!=4:
            raise TypeError, "len(plotRange) != 4."
        number = (int, long, float)
        p = []
        nlabels = self.o.keys()
        for n in nlabels:
            if n not in self.nodeData:
                return "Error: one or more node coordinates are lacking."
            else:
                ndata = self.nodeData[n]
                if not isinstance(ndata, (list, tuple)):
                    return "Error: one or more node coordinates aren't a list or tuple."
                else:
                    if len(ndata) != 2:
                        return "Error: one or more node coordinates aren't pairs."
                    else:
                        x,y = ndata
                        if not isinstance(x, number) or not isinstance(y, number):
                            return "Error: one or more node coordinates aren't int, long or float."
                        else:
                            p.append(ndata)
        arr = []
        li = []
        lo = set()
        if arcs:
            self_o = self.o
            self_nodeData = self.nodeData
            l = set()
            for n1,a in self_o.iteritems():
                for n2 in a.iterkeys():
                    if n1 in self_o[n2]:
                        if (n2,n1) not in l:
                            if n1==n2:
                                lo.add(n1)
                            else:
                                l.add( (n1,n2) )
                    else:
                        arr.append( (self_nodeData[n1],self_nodeData[n2]) )
            li = [ (self_nodeData[n1],self_nodeData[n2]) for (n1,n2) in l]
            lo = [ self_nodeData[n] for n in lo]
        if not nodes:
            p = None
        if not nodeLabels:
            nlabels = None
        cartesianPlot(windowTitle="Graph plot", points=p, lines=li, arrows=arr, loops=list(lo),
                      plotRange=plotRange, gridSpacing=grid, axes=axes, pointLabels=nlabels)


    # GRAPH VISITS: ===========================================

    def DFS(self, startNode, sort=False, direction=1):
        """DFS(startNode, sort=False, direction=1): depth-first search list of nodes,
        starting from the given node. It walks inbound arcs too.
        If sort==True then it sorts the nodes at each step (gives an error on unsortable node IDs).
        direction= 1  normal (downward) BFS use outgoing arcs.
        direction=-1  backward BFS use incoming arcs.
        direction= 0  bidirectional BFS use incoming and outgoing arcs."""
        # Can the extends be slow?
        self_a = self.o
        self_b = self.i
        if direction == -1: # backward BFS
            self_b, self_a = self_a, self_b
        bidirect = direction == 0
        assert startNode in self_a
        unprocessed = [startNode]
        visited = set() # This to avoid a slow "in" into result, that is a list.
        result = []
        if sort:
            while unprocessed:
                n = unprocessed.pop()
                if n not in visited:
                    result.append(n)
                    visited.add(n)
                    if bidirect:
                        unprocessed.extend( sorted(self_a[n].keys() + self_b[n].keys(), reverse=True) )
                    else:
                        unprocessed.extend( sorted(self_a[n], reverse=True) )
        else:
            while unprocessed:
                n = unprocessed.pop()
                if n not in visited:
                    result.append(n)
                    visited.add(n)
                    if bidirect:
                        unprocessed.extend( self_a[n].keys() + self_b[n].keys() )
                    else:
                        unprocessed.extend( self_a[n] )
        return result


    def BFS(self, startNode, sort=False, direction=1):
        """BFS(startNode, sort=False, direction=1): return a breadth-first search list of nodes
        starting from the given node.
        If sort==True then it sorts the nodes at each step (gives an error on unsortable node IDs).
        direction= 1  normal (downward) BFS use outgoing arcs.
        direction=-1  backward BFS use incoming arcs.
        direction= 0  bidirectional BFS use incoming and outgoing arcs."""
        # Can the extends be slow?
        self_a = self.o
        self_b = self.i
        if direction == -1: # backward BFS
            self_b, self_a = self_a, self_b
        bidirect = direction == 0
        assert startNode in self_a
        unprocessed = deque()
        unprocessed.append(startNode)
        visited = set() # This to avoid a slow "in" into result, that is a list.
        result = []
        if sort:
            while unprocessed:
                n = unprocessed.popleft()
                if n not in visited:
                    result.append(n)
                    visited.add(n)
                    if bidirect:
                        unprocessed.extend( sorted(self_a[n].keys() + self_b[n].keys()) )
                    else:
                        unprocessed.extend( sorted(self_a[n]) )
        else:
            while unprocessed:
                n = unprocessed.popleft()
                if n not in visited:
                    result.append(n)
                    visited.add(n)
                    if bidirect:
                        unprocessed.extend( self_a[n].keys() + self_b[n].keys() )
                    else:
                        unprocessed.extend( self_a[n] )
        return result


    def xDFS(self, startNode, sort=False, direction=1):
        """xDFS(startNode, sort=False, direction=1): iterable depth-first search list of nodes,
        starting from the given node.
        If sort==True then it sorts the nodes at each step (gives an error on unsortable node IDs).
        direction= 1  normal (downward) BFS use outgoing arcs.
        direction=-1  backward BFS use incoming arcs.
        direction= 0  bidirectional BFS use incoming and outgoing arcs."""
        # Can the extends be slow?
        self_a = self.o
        self_b = self.i
        if direction == -1: # backward BFS
            self_b, self_a = self_a, self_b
        bidirect = direction == 0
        assert startNode in self_a
        unprocessed = [startNode]
        visited = set() # This to avoid a slow "in" into result, that is a list.
        if sort:
            while unprocessed:
                n = unprocessed.pop()
                if n not in visited:
                    yield n
                    visited.add(n)
                    if bidirect:
                        unprocessed.extend( sorted(self_a[n].keys() + self_b[n].keys(), reverse=True) )
                    else:
                        unprocessed.extend( sorted(self_a[n], reverse=True) )
        else:
            while unprocessed:
                n = unprocessed.pop()
                if n not in visited:
                    yield n
                    visited.add(n)
                    if bidirect:
                        unprocessed.extend( self_a[n].keys() + self_b[n].keys() )
                    else:
                        unprocessed.extend( self_a[n] )


    def xBFS(self, startNode, sort=False, direction=1):
        """xBFSstartNode, sort=False, direction=1): iterable breadth-first search list of nodes
        starting from the given node.
        If sort==True then it sorts the nodes at each step (gives an error on unsortable node IDs).
        direction= 1  normal (downward) BFS use outgoing arcs.
        direction=-1  backward BFS use incoming arcs.
        direction= 0  bidirectional BFS use incoming and outgoing arcs."""
        # Can the extends be slow?
        self_a = self.o
        self_b = self.i
        if direction == -1: # backward BFS
            self_b, self_a = self_a, self_b
        bidirect = direction == 0
        assert startNode in self_a
        unprocessed = deque()
        unprocessed.append(startNode)
        visited = set() # This to avoid a slow "in" into result, that is a list.
        if sort:
            while unprocessed:
                n = unprocessed.popleft()
                if n not in visited:
                    yield n
                    visited.add(n)
                    if bidirect:
                        unprocessed.extend( sorted(self_a[n].keys() + self_b[n].keys()) )
                    else:
                        unprocessed.extend( sorted(self_a[n]) )
        else:
            while unprocessed:
                n = unprocessed.popleft()
                if n not in visited:
                    yield n
                    visited.add(n)
                    if bidirect:
                        unprocessed.extend( self_a[n].keys() + self_b[n].keys() )
                    else:
                        unprocessed.extend( self_a[n] )


    # GRAPH I/O: ===========================================


    def save(self, fileName="graph.pik", compressed=False):
        """save(fileName="graph.pik", compressed=False): save the graph with cPickle.
        If compressed=True, compresses the graph with BZ2 (compresslevel=3).
        In some situations it doesn't work, for example:
          g = Graph()
          g.addNode(1, nodeData=lambda:0)
        Now g.nodeData is:
          {1: <function <lambda> at 0xhhhhhhhh>}
        This nodeData cannot be saved in the file."""
        if compressed:
            fout = BZ2File(fileName, "w", compresslevel=3)
        else:
            fout = open(fileName, "wb")
        cPickle.dump(self.o, fout, 2)
        cPickle.dump(self.nodeData, fout, 2)
        fout.close()


    def load(self, fileName="graph.pik", compressed=False):
        """load(fileName="graph.pik", compressed=False): load the graph with cPickle.
        If compressed=True, read the graph compresses with BZ2."""
        try:
            fileSize = os.stat(fileName)[stat.ST_SIZE]
        except os.error:
            fileSize = 0
        self.clear()
        if fileSize > 0:
            if compressed:
                fin = BZ2File(fileName, "r")
            else:
                fin = open(fileName, "rb")
            self.o = cPickle.load(fin)
            self.nodeData = cPickle.load(fin)
            self.nextNode = 0
            fin.close()
            self._regenerate() # This is faster than loading self.i too.


    def textSave(self, fileName="graph.txt"):
        """textSave(fileName="graph.txt"): save graph in a text file, with a simple method.
        In some situations it doesn't work, for example:
          g = Graph()
          g.addNode(1, nodeData=lambda:0)
        Now g.nodeData is:
          {1: <function <lambda> at 0xhhhhhhhh>}
        This nodeData cannot be saved in the textual file."""
        # This method is fragile, and it can be made faster.
        f = file( str(fileName), 'w')

        # Write the node on the first file line:
        f.write(  "\t".join(repr(node) for node in self.o.iterkeys())  + "\n")

        # Write the arcs:
        for node1 in self.o.iterkeys():
            ls1 = repr(node1) + '\t'
            ls = []
            for node2 in self.o[node1].iterkeys():
                ls.extend([ls1, repr(node2), '\t', repr(self.o[node1][node2]), '\n' ])
            f.write("".join(ls))

        # Write the nodeData:
        f.write("\t\t\n")
        ls = []
        for n, ndata in self.nodeData.iteritems():
            ls.append(  repr(n) + '\t' + repr(ndata)  )
        f.write("\n".join(ls))
        f.close()


    def textLoad(self, fileName="graph.txt"):
        """textLoad(fileName="graph.txt"): load graph from text file."""
        # This method is fragile, and it can be made faster.
        try:
            f = file(fileName)
        except IOError:
            raise Exception, "file" + fileName + "cannot be read."
        else:
            self.clear()
            self.nextNode = 0
            # The first line contains the node names:
            for n in f.readline().split('\t'):
               self.addNode(eval(n))

            # The successive lines are the arcs:
            for line in f:
                if line == "\t\t\n": break # Until there's an "\t\t\n"
                sline = line.split("\t")
                self.addArc( eval(sline[0]), eval(sline[1]), eval(sline[2]) )

            # and after "\t\t\n" there are the nodeData:
            for line in f:
                sline = line.split("\t")
                n = eval(sline[0])
                if n in self.o:
                    self.nodeData[n] = eval(sline[1])
            f.close()


    def saveDot(self, fileName="graph.dot", nodeLabels=True, arcLabels=False, hideArcLabel=None,
                nodeDataLabels=False, colorConnectedComponents=False):
        """saveDot(fileName="graph.dot", nodeLabels=True, arcLabels=False, hideArcLabel=None,
                   nodeDataLabels=False, colorConnectedComponents=False):
        save the graph in a file suitable for Graphviz, a program for visualising graphs:
          http://www.research.att.com/sw/tools/graphviz/
        If nodeLabels=True show node labels too as a string.
        If arcLabels=True show weights too as labels (but don't show weights equal to hideArcLabel).
        If nodeDataLabels=True, show nodeData too (under node IDs) as a string.
        If colorConnectedComponents=True use a different node color for each connected component. Ex:
            def savegraph(f, nl=True):
                g.saveDot(fileName=f+".dot", nodeLabels=nl, arcLabels=False, hideArcLabel="a",
                          nodeDataLabels=True, colorConnectedComponents=True)
                subprocess.call("neato -Tpng -o" + f + ".png " + f + ".dot")
            g = graph.Graph()
            g.addClique(range(8), w="a", loops=True)
            savegraph("clique", nl=False)
            g.createRandom(range(28), 0.023, nodeData="hello")
            savegraph("random")
            g.createNcube(4)
            savegraph("tesseract")
            g.create2dGrid(range(49), 7)
            savegraph("2dgrid7x7", nl=False)"""
        tresh = 0.3
        try:
            f = open(fileName, 'w')
        except IOError: return "File opening error."
        undirected = self.isUndirected()
        if undirected:
            f.write('graph G{\n')
            sep = " -- "
        else:
            f.write('digraph G{\n')
            sep = " -> "
        f.write("graph [splines=true overlap=scale]\n")
        if len(self.o)>5 and (0.0+self.arcCount)/len(self.o)**2 > tresh:
            f.write("edge [len=4]\n")
        idNodes = _mysorted(self.o)
        nodesPos = dict( (n,i) for i,n in enumerate(idNodes) )

        if colorConnectedComponents:
            colors = """red black blue green3 gold orange gray50 gray30 gray80 chocolate tan
                        navy darkorange limegreen magenta maroon pink yellowgreen sienna wheat
                        violet turquoise sienna red2 olivedrab red3 plum lightsteelblue peru purple
                        turquoise wheat2""".split()
            cc = dict( (n,i) for i,group in enumerate(self.connectedComponents()) for n in group )

        for n1 in idNodes:
            nbrs = self.o[n1].keys()
            n1str = str(nodesPos[n1])
            label = ""
            if nodeLabels: label = str(n1)
            if nodeDataLabels and n1 in self.nodeData:
                if label: label += "\\n"
                label += str(self.nodeData[n1])
            if colorConnectedComponents:
                color = colors[ cc[n1] % len(colors) ]
            else:
                color = "red"
            if label:
                label = ' [color=' + color + ' label="' + label + '"]\n'
            else:
                label = ' [style=filled color=white fillcolor=' + color + ' label="" shape=circle width=0.08]\n'
            f.write(n1str + label)
            for n2 in nbrs:
                w = self.o[n1][n2]
                attrstr = ""
                if arcLabels and w!=hideArcLabel:
                    attrstr = " [label=" + str(self.o[n1][n2]) + "]"
                n2str = str(nodesPos[n2])
                if n2str >= n1str or not undirected:
                    f.write(n1str + sep + n2str + attrstr + "\n")
        f.write('}')
        f.close()


    def savePajek(self, fileName="graph.net"):
        """"savePajek(fileName="graph.net"): save the graph in format readable by Pajek:
        http://vlado.fmf.uni-lj.si/pub/networks/pajek/ """
        """
        The file format accepted by Pajek provides information on the vertices, arcs (directed
        edges), and undirected edges. A short example showing the file format is given below:
        -------------------------------------
        *Vertices 3
        1 "Doc1" 0.0 0.0 0.0 ic Green bc Brown
        2 "Doc2" 0.0 0.0 0.0 ic Green bc Brown
        3 "Doc3" 0.0 0.0 0.0 ic Green bc Brown
        *Arcs
        1 2 3 c Green
        2 3 5 c Black
        *Edges
        1 3 4 c Green
        -------------------------------------
        Herein there are 3 vertices Doc1, Doc2 and Doc3 denoted by numbers 1, 2 and 3. The (fill)
        color of these nodes is Green and the border color is Brown. The initial layout location of
        the nodes is (0,0,0). Note that the (x,y,z) values can be changed interactively after drawing.

        There are two arcs (directed edges). The first goes from node 1 (Doc1) to node 2 (Doc2)
        with a weight of 3 and in color Green.

        For edges, there is one from node 1 (Doc1) to node 3 (Doc3) of weight of 4, and in Green
        color. """
        try:
            f = open(fileName, 'w')
        except IOError:
            return "File opening error."
        nodes = self.o.keys()
        f.write("*Vertices " + str(len(nodes)) + "\n")
        list_tuple = (list, tuple)
        int_long_float = (int, long, float)
        for i,n in enumerate(nodes):
            m = self.nodeData.get(n, None)
            if isinstance(m, list_tuple) and len(m)==2 \
               and isinstance(m[0], int_long_float) and isinstance(m[1], int_long_float):
                f.write( str(i+1) + ' "' + str(n) + '" ' + str(m[0]) + " " + str(m[1]) + " ic Red\n" )
            else:
                f.write( str(i+1) + ' "' + str(n) + '"  ic Red\n' )

        conv = dict( (k,str(i+1)) for i,k in enumerate(nodes) )
        isreal = self.realw()
        f.write("*Edges\n")
        for n1,n2 in self.undirectedArcs():
            if isreal:
                f.write( conv[n1] + " " + conv[n2] + " " + str(self.getArcw(n1, n2)) + "\n" )
            else:
                f.write( conv[n1] + " " + conv[n2] + "\n" )
        f.write("*Arcs\n")
        for n1,n2 in self.directedArcs():
            if isreal:
                f.write( conv[n1] + " " + conv[n2] + " " + str(self.getArcw(n1, n2)) + "\n" )
            else:
                f.write( conv[n1] + " " + conv[n2] + "\n" )
        f.close()


    def fromAmatrix(self, amatrix, nodes=None, w=None, nodeData=None):
        """fromAmatrix(amatrix, nodes=None, w=None, nodeData=None): clear the graph, and
        create a new graph based on the given (square) adjacency matrix. Parameters:
        - matrix can be a list of lists containing values that can be casted to True or False,
          a True means that there is an oriented arc. Otherwise amatrix can be a square 2D
          array of numarray (arcs are numbers !=0).
        - nodes is optional, it can be None, or it can be a Python list of hashable node IDs
          to be used to create the graph.
          If nodesID!=None, nodesID must be long as the side of the (square) amatrix.
          If nodesID=None, the nodes are created with ID as sequential integers starting from 0.
        - All the arcs can be created with the given weight w, or the default weight None.
        - nodeData is the optional value assigned as nodeData of all the created nodes.
          Default is None, it means no nodeData at all.
        Example:
          g = Graph()
          g.createRandom(range(100), 0.03, w=0, nodeData=1)
          matrix, xlabels, ylabels, title, mapping = g.aform()
          h = Graph()
          h.fromAmatrix(matrix, nodes=xlabels, w=0, nodeData=1)
          assert g == h """
        if not isinstance(amatrix, (list, tuple)):
            raise TypeError, "in fromAmatrix: amatrix isn't list or tuple."
        if nodes!=None and not isinstance(nodes, (int, long, float)):
            raise TypeError, "in fromAmatrix: nodes isn't None, list or tuple."
        self.clear()
        if not amatrix:
            return # Empty graph.
        size = len(amatrix)
        if nodes is None:
            nodes = self.createID(size)
        if size != len(nodes):
            return "Error in fromAmatrix: len(amatrix) != len(nodes)."
        for n in nodes:
            self.o[n] = {}
            self.i[n] = {}
        for i,row in enumerate(amatrix):
            if len(row) != size:
                self.clear()
                return "Error in fromAmatrix: amatrix isn't square."
            n1 = nodes[i]
            for j,a in enumerate(row):
                if a: self.addArc(n1, nodes[j], w)
        if nodeData != None:
            self.nodeData = dict.fromkeys(nodes, nodeData)
        # return self


    def fromMap(self, m, good=None, coords=True, w=1):
        """fromMap(m, good=None, coords=True, w=1): clear the graph, and convert the given
        matrix m (list or tuple of list or tuples) into an undirected graph, with 4-connectivity.
        good is a given boolean function that returns True for the matrix elements to insert into
          the graph. Default: def good(x): return bool(x)
        If coords=True then nodeData of nodes contains (x,y) coordinates of the node in m.
        w is the arc weight for all undirected arcs created. Default=1. Example:
          m = [[1,1,1],
               [0,0,1],
               [0,1,1]]
          g.fromMap(m)
          print g
          ==> (0, 0)-(1, 0)  (1, 0)-(2, 0)  (1, 2)-(2, 2)  (2, 0)-(2, 1)  (2, 1)-(2, 2) """
        self.clear()
        if m and isinstance(m, (list, tuple)):
            if good != None:
                m = [[good(e) for e in row] for row in m]
            maxy = len(m)-1
            maxx = len(m[0])-1
            add = self.addBiArc
            for y, row in enumerate(m):
                for x, e in enumerate(row):
                    if e:
                        self.addNode((x,y)) # Necessary for isolated nodes.
                        if x>0 and m[y][x-1]: add( (x,y), (x-1,y), w=w)
                        if x<maxx and m[y][x+1]: add( (x,y), (x+1,y), w=w)
                        if y>0 and m[y-1][x]: add( (x,y), (x,y-1), w=w)
                        if y<maxy and m[y+1][x]: add( (x,y), (x,y+1), w=w)
            if coords:
                for n in self.o.iterkeys(): # Update nodedata with node coords. Y is inverted.
                    self.nodeData[n] = n
        # return self


    def _fastLoad(self, fileName, compressed=False):
        """_fastLoad(fileName, compressed=False): low level method: load the graph with cPickle.
        If compressed=True read the graph compresses with BZ2. This doesn't perform the
        final regenerate."""
        try:
            fileSize = os.stat(fileName)[stat.ST_SIZE]
        except os.error:
            fileSize = 0
        self.clear()
        self.nextNode = 0
        if fileSize > 0:
            if compressed:
                fin = BZ2File(fileName, "r")
            else:
                fin = open(fileName, "rb")
            self.o = cPickle.load(fin)
            self.nodeData = cPickle.load(fin)
            fin.close()


try: # Import Psyco if available. You can find it here: http://psyco.sourceforge.net/
    import psyco
except ImportError:
    pass
else:
    # Psyco improves the speed of the following methods:
    psyco.bind(dijkstra.shortestPath)
    methods="""addNodes DFS BFS sumw arcs makeUndirected degreeDict inboundDict randomw integerw
    realw addSource addSink isUndirected maxDegree short aform wform iform lform lview aview wview
    _matrixView connectedComponents toposort loopCount textSave textLoad load subgraphExtract
    addArcs addMulti addUpdate subUpdate intersection nodeIntersection delManyNodes _regenerate
    _cleanDeadArcs allPairsShortestPaths addNcube renameNode euclidify2d complement createID
    isTournament fromMap""".split()
    for m in methods: eval( "psyco.bind(Graph." + m + ")" )
    #>>> x = 'my_var'
    #>>> globals()[x] = 7
    #>>> my_var
    #7

__all__ = ["Graph"] # Export Graph class only.

#lambda:dir(x) # A mistery, useless code.

# See graph_test.py for some demo and tests.