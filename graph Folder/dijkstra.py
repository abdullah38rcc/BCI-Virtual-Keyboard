class priorityDictionary(dict):
    # $Id: priodict.py,v 1.2 2003/12/09 23:40:33 kdart Exp $
    # Priority dictionary using binary heaps
    # David Eppstein, UC Irvine, 8 Mar 2002
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117228
    def __init__(self):
        """Initialize priorityDictionary by creating binary heap of pairs (value,key). Note
        that changing or removing a dict entry will not remove the old pair from the heap
        until it is found by smallest() or until the heap is rebuilt."""
        self.__heap = []
        dict.__init__(self)

    def smallest(self):
        "Find smallest item after removing deleted items from heap."
        if len(self) == 0:
            raise IndexError, "smallest of empty priorityDictionary"
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            lastItem = heap.pop()
            insertionPoint = 0
            while 1:
                smallChild = 2*insertionPoint+1
                if smallChild+1 < len(heap) and heap[smallChild] > heap[smallChild+1]:
                    smallChild += 1
                if smallChild >= len(heap) or lastItem <= heap[smallChild]:
                    heap[insertionPoint] = lastItem
                    break
                heap[insertionPoint] = heap[smallChild]
                insertionPoint = smallChild
        return heap[0][1]

    def __iter__(self):
        "Create destructive sorted iterator of priorityDictionary."
        def iterfn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]
        return iterfn()

    def __setitem__(self,key,val):
        """Change value stored in dictionary and add corresponding pair to heap. Rebuilds
        the heap if the number of deleted items grows too large, to avoid memory leakage."""
        dict.__setitem__(self,key,val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v,k) for k,v in self.iteritems()]
            self.__heap.sort()  # builtin sort likely faster than O(n) heapify
        else:
            newPair = (val,key)
            insertionPoint = len(heap)
            heap.append(None)
            while insertionPoint > 0 and newPair < heap[(insertionPoint-1)//2]:
                heap[insertionPoint] = heap[(insertionPoint-1)//2]
                insertionPoint = (insertionPoint-1)//2
            heap[insertionPoint] = newPair

    def setdefault(self,key,val):
        "Reimplement setdefault to call our customized __setitem__."
        if key not in self:
            self[key] = val
        return self[key]


def dijkstra(G, start, end=None):
    """Find shortest paths from the start vertex to all vertices nearer than or equal to the end.

    The input graph G is assumed to have the following representation: A vertex can be any
    object that can be used as an index into a dictionary.  G is a dictionary, indexed by
    vertices.  For any vertex v, G[v] is itself a dictionary, indexed by the neighbors of
    v.  For any edge v->w, G[v][w] is the length of the edge.  This is related to the
    representation in http://www.python.org/doc/essays/graphs.html
    where Guido van Rossum suggests representing graphs as dictionaries mapping vertices
    to lists of neighbors, however dictionaries of edges have many advantages over lists:
    they can store extra information (here, the lengths), they support fast existence
    tests, and they allow easy modification of the graph by edge insertion and removal.
    Such modifications are not needed here but are important in other graph algorithms.
    Since dictionaries obey iterator protocol, a graph represented as described here could
    be handed without modification to an algorithm using Guido's representation.

    Of course, G and G[v] need not be Python dict objects; they can be any other object
    that obeys dict protocol, for instance a wrapper in which vertices are URLs and a call
    to G[v] loads the web page and finds its links.

    The output is a pair (D,P) where D[v] is the distance from start to v and P[v] is the
    predecessor of v along the shortest path from s to v.

    Dijkstra's algorithm is only guaranteed to work correctly when all edge lengths are
    positive. This code does not verify this property for all edges (only the edges seen
    before the end vertex is reached), but will correctly compute shortest paths even for
    some graphs with negative edges, and will raise an exception if it discovers that a
    negative edge has caused it to make a mistake."""
    # Dijkstra's algorithm for shortest paths
    # David Eppstein, UC Irvine, 4 April 2002
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/119466
    D = {}  # Dictionary of final distances.
    P = {}  # Dictionary of predecessors.
    Q = priorityDictionary()   # Estimated distance of non-final vertices.
    Q[start] = 0
    for v in Q:
        D[v] = Q[v]
        if v == end: break # If the graph contains the None node, then there can be problems.

        for w in G[v]:
            vwLength = D[v] + G[v][w]
            if w in D:
                if vwLength < D[w]:
                    raise ValueError, "Dijkstra: found better path to already-final vertex."
            elif w not in Q or vwLength < Q[w]:
                Q[w] = vwLength
                P[w] = v
    return D, P


def dijkstraOnew(G, start, end=None):
    """dijkstraOnew(G, start, end=None): find shortest paths from the start vertex to all
    vertices nearer than or equal to the end. All arc weights are ignored and meant as 1.
    See dijkstra() docstring for more explanations."""
    D = {}  # Dictionary of final distances.
    P = {}  # Dictionary of predecessors.
    Q = priorityDictionary()   # Estimated distance of non-final vertices.
    Q[start] = 0
    for v in Q:
        D[v] = Q[v]
        if v == end: break # If the graph contains the None node, then there can be problems.

        for w in G[v]:
            vwLength = D[v] + 1
            if w in D:
                if vwLength < D[w]:
                    raise ValueError, "Dijkstra: found better path to already-final vertex."
            elif w not in Q or vwLength < Q[w]:
                Q[w] = vwLength
                P[w] = v
    return D, P


def shortestPath(g, start, end, weights=True):
    """shortestPath(g, start, end, weights=True): find a single shortest path from the given
    start vertex to the given end vertex. The input has the same conventions as dijkstra().
    The output is a list of the vertices in order along the shortest path.
    If a vertex or a path between them doesn't exists, the result is an empty list.
    If weights=False then all arc weights are meant as 1."""
    if start not in g or end not in g:
        return []
    if weights:
        D, P = dijkstra(g, start, end)
    else:
        D, P = dijkstraOnew(g, start, end)
    path = []
    while 1:
        path.append(end)
        if end == start:
            break
        if end in P:
            end = P[end]
        else:
            path = [] # The end cannot be reached.
            break
    path.reverse()
    return path


__all__ = ["dijkstra", "shortestPath", "dijkstraOnew"] # Export.


if __name__ == '__main__': #test -----------------------------------------------------
    from random import randint
    n, g = 50, {}
    for i in xrange(1,n+1): g[i] = {}
    for i in xrange(n*3): g[randint(1,n)][randint(1,n)] = 1
    print dijkstra(g,1)

    print "\n\nUndirected graph:"
    g = {'A':{'C':5,'B':1,'D':8}, 'C':{'A':5,'B':3,'F':1}, 'D':{'A':8,'F':1}, 'G':{'E':2,'F':1},
         'E':{'B':2,'G':2,'F':4}, 'B':{'A':1,'C':3,'E':2}, 'F':{'C':1,'E':4,'D':1,'G':1}}
    gdraw = r"""
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
    #print g
    for n,e in sorted(g.items()):
        print n+":", " ".join([n1+":"+str(w) for n1,w in sorted(e.items())])
    print gdraw
    print 'shortestPath(g, "A", "G"):', shortestPath(g, "A", "G")
    print 'shortestPath(g, "D", "E"):', shortestPath(g, "D", "E")
    print
    print "dijkstra(g, 'A', end=None):", dijkstra(g, 'A', end=None)
    print "\n"

    g = {1: {2: 1}, 2: {3: 1}, 3: {}, 4: {1: 1}}
    print "g =", g
    print "shortestPath(g, 1, 3):", shortestPath(g, 1, 3)
    print "shortestPath(g, 1, 4):", shortestPath(g, 1, 4)