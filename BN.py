# 86411 - Filipe dos Santos Oliveira Marques - Grupo 97
class Node():
    def __init__(self, prob, parents = []):
        self.parents = parents
        self.prob = prob

    def computeProb(self, evid):
        prob = self.prob
        if not self.parents:
            return [1-prob[0], prob[0]]
        for parent in self.parents:
            prob = prob[evid[parent]]
        return [1-prob, prob]

# Extends a list? can't understand the algorithm line that
# says 'extend With X = xi' but i guess it does this? idk
def extend(e, pos, val):
        e[pos] = val
        return e

# Algorithm: Enumeration-Ask on page 525 of the book
def enumerationAsk(X, e, bn):
    # Distribution over X, represented as an empty list
    # with Q[0] begin the false value and Q[1] the true
    Q = [0, 0]
    for xi in [0, 1]:
        # We need to copy evidence list because otherwise on the
        # next iteration of the loop the list has the wrong values
        e_xi = e.copy()
        Q[xi] = enumerateAll(bn.getVars(), extend(e_xi, X, xi), bn)
    return [Q[0]/sum(Q), Q[1]/sum(Q)]

def enumerateAll(variables, e, bn):
    if not variables:
        return 1

    Y = variables[0]
    node = bn.getNode(Y)

    rest = variables[1:]
    if isinstance(e[Y], int):
        return node.computeProb(e)[e[Y]]*enumerateAll(rest, e, bn)
    else:
        sumation = 0
        for y in [0, 1]:
            # We copy the list for the same reason as the evidence
            # list in the enumeration ask algorithm
            e_y = e.copy()
            sumation += node.computeProb(e_y)[y]*enumerateAll(rest,extend(e_y, Y, y), bn)
        return sumation


class BN():
    def __init__(self, gra, prob):
        self.gra = gra
        self.prob = prob
        self.variables = []
        for i in range(len(prob)):
            self.variables.append(i)

    def getVars(self):
        return self.variables

    def getNode(self, var):
        return self.prob[var]

    def computePostProb(self, evid):
        # We make evidence a list so it is easier to manipulate
        e = list(evid)
        X = e.index(-1)
        return enumerationAsk(X, e, self)[1]

    def computeJointProb(self, evid):
        prob = 1
        for i in range(len(self.prob)):
            prob *= self.prob[i].computeProb(evid)[evid[i]]
        return prob
