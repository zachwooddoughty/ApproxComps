import collections
from graph import *

### Zach Wood-Doughty
### 2014 March 5
### Code available on Github.com/zachwooddoughty/ApproxComps

class HopcroftKarp(object):
    '''
    Hopcroft-Karp algorithm for finding a matching of size k in a bipartite graph
    Adapted from Wikipedia and http://stackoverflow.com/questions/4697228/hopcroftkarp-algorithm-in-python
    '''

    INFINITY = -1

    def __init__(self, G):
        self.G = G

    def match(self, k):
        '''construct a matching of size k'''
        self.pair = {}
        self.dist = {}
        self.q = collections.deque()

        #init
        for v in self.G.X + self.G.Y:
            self.pair[v] = None
            self.dist[v] = HopcroftKarp.INFINITY

        matching = 0

        while matching < k and self.bfs():
            for v in self.G.X:
                if matching >= k:
                    break
                if self.pair[v] is None and self.dfs(v):
                    matching = matching + 1
                    #print matching, [(u, self.pair[u]) for u in self.pair.keys() if u > 0 and self.pair[u] is not None]
                    if matching == k:
                        break

        # construct matching object
        edges = [(u, self.pair[u]) for u in self.pair.keys() if u > 0 and self.pair[u] is not None]
        M = Matching(k, edges)

        return M

    def dfs(self, v):
        if v != None:
            for u in self.G.neighbors[v]:
                if self.dist[ self.pair[u] ] == self.dist[v] + 1 and self.dfs(self.pair[u]):
                    self.pair[u] = v
                    self.pair[v] = u

                    return True

            self.dist[v] = HopcroftKarp.INFINITY
            return False

        return True

    def bfs(self):
        for v in self.G.X:
            if self.pair[v] == None:
                self.dist[v] = 0
                self.q.append(v)
            else:
                self.dist[v] = HopcroftKarp.INFINITY

        self.dist[None] = HopcroftKarp.INFINITY

        while len(self.q) > 0:
            v = self.q.popleft()
            if v != None:
                for u in self.G.neighbors[v]:
                    if self.dist[ self.pair[u] ] == HopcroftKarp.INFINITY:
                        self.dist[ self.pair[u] ] = self.dist[v] + 1
                        self.q.append(self.pair[u])

        return self.dist[None] != HopcroftKarp.INFINITY


def main():
    n = 4
    g = Graph(n, [(1,-3), (1,-4), (2,-2), (3,-1), (4,-3), (4,-4)])
    hc = HopcroftKarp(g)
    for k in range(1, 5):
        for i in range(3):
            print k, hc.match(k).E

if __name__ == "__main__":
    main()
