import math, random
from graph import *
from hopcroftkarp import *
from operator import mul


class MarkovChain:
    '''
    M is the current state (a matching of size k or k-1)
    G is the underlying graph
    k is the max size of a matching
    '''
    def __init__(self, k, G, M):
        self.k = k
        self.G = G
        self.M = M
    
    def run(self, num_transitions):
        '''Run the markov chain n steps'''
        for i in range(num_transitions):
            e = self.G.random_edge()
            self.M.transition(e) 

class MonteCarloEstimator:
    
    def __init__(self, G, k):
        self.G = G
        self.k = k

        hc = HopcroftKarp(G)
        self.M = hc.match(k)
        self.MC = MarkovChain(k, G, self.M)

    def estimate(self, num_transitions, num_samples):
        num_k = 0
        num_k_minus_1 = 0
        for i in range(num_samples):
            self.MC.run(num_transitions)
            if self.M.size() == self.k:
                num_k += 1
            elif self.M.size() == self.k - 1:
                num_k_minus_1 += 1

        return float(num_k) / num_k_minus_1

class Approximator:

    def __init__(self, G, num_transitions="n ** 9", num_samples="n ** 5"):
        self.G = G
        self.r = [len(G.E)]

        n = self.G.n
        self.num_transitions = eval(num_transitions)
        self.num_samples = eval(num_samples)
        print self.num_transitions, self.num_samples
        
    def run(self):
        for k in range(2, self.G.n + 1):
            MCE = MonteCarloEstimator(self.G, k)
            self.r.append(MCE.estimate(self.num_transitions, self.num_samples))
        
        return reduce(mul, self.r, 1)


def main():
    n = 4
    g = Graph(n, [(1,-3), (1,-4), (2,-2), (3,-1), (4,-3), (4,-4)])
    #m = Matching(n, [(1,-3), (2, -2), (3, -1), (4, -4)])
    #mc = MarkovChain(n, g, m)

    a = Approximator(g)
    print a.run()

if __name__ == "__main__":
    main()
