import math, random

class Graph:
    '''
    A bipartite graph.
    n is the number of nodes on each side
    E is a list of edges, where each edge is a tuple (u, v)
    '''

    def __init__(self, n, E):
        self.n = n
        self.E = E 
        self.X = [x + 1 for x in range(n)]
        self.Y = [y * -1 - 1 for y in range(n)]
        self.neighbors = {}
        for e in self.E:
            x, y = e
            self.neighbors[x] = self.neighbors.get(x, []) + [y]
            self.neighbors[y] = self.neighbors.get(y, []) + [x]

    def random_edge(self):
        return random.sample(self.E, 1)[0]

    def construct_matching(self, k):
        '''returns a matching of size k'''
        M = Matching(k, [self.E[0]])
        while M.size() < k:
            # we will create an augmenting path that we can use to increase the size of our matching
            # R = unmatched nodes in the left side
            R = [node for node in [x + 1 for x in range(n)] if a not in M.X]
            T = []
            for node in R:
                # we want to find an unmatched edge that comes from here
                for edge in E:
                    if node in edge and edge not in M.E:
                        T.append(edge[1])
class Matching:
    def __init__(self, k, E):
        '''
        E is the set of edges in the matching
        k is the max size this matching can take
        '''
        self.k = k
        self.E = E
        self.update()

    def update(self):
        self.X_pair = {x:y for (x,y) in self.E}
        self.Y_pair = {y:x for (x,y) in self.E}

    def size(self):
        '''return the size of our matching'''
        return len(self.E)

    def transition(self, e):
        '''
        Consider transitioning M_k -> M_k-1
        or M_k-1 -> M_k-1 or M_k-1 -> M_k
        '''
        changed = False

        if self.size() == self.k:
            if e in self.E:
                self.E.remove(e)
                changed = True
        else:
            u,v = e
            if (u in self.X_pair) != (v in self.Y_pair): 
                # XOR
                if u in self.X_pair:
                    self.E.remove((u, self.X_pair[u]))
                elif v in self.Y_pair:
                    self.E.remove((self.Y_pair[v], v))
                self.E.append(e)
                changed = True
            elif (u not in self.X_pair) and (v not in self.Y_pair):
                self.E.append(e)
                changed = True
            
        if changed:
            self.update()    
            assert self.size() == self.k or self.size() == self.k-1
        
        return changed
