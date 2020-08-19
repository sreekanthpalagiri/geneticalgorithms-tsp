"""
Basic TSP Example
file: Individual.py
"""

import random
import math

class Individual:
    def __init__(self, _size, _data,method):
        """
        Parameters and general variables
        """
        self.fitness    = 0
        self.distance   = 0
        self.genes      = []
        self.genSize    = _size
        self.data       = _data

        self.genes = list(self.data.keys())

        if method == 'random':
            for i in range(0, self.genSize):
                n1 = random.randint(0, self.genSize-1)
                n2 = random.randint(0, self.genSize-1)
                tmp = self.genes[n2]
                self.genes[n2] = self.genes[n1]
                self.genes[n1] = tmp
        elif method == 'NearestNeighbour':
            tmp=self.genes.copy()
            e = random.randint(0, self.genSize-1)
            e = self.genes[e]
            newgene=[e]
            tmp.remove(e)
            while tmp:
                e=self.getNearestNeighbour(e,tmp)
                tmp.remove(e)
                newgene.append(e)
            self.genes=newgene
    def getNearestNeighbour(self,e,tmp):
        bestdist = float("inf")
        for i in tmp:
            dist=self.euclideanDistance(e,i)
            if dist < bestdist:
                bestdist = dist
                index=i
        return index
        
    def setGene(self, genes):
        """
        Updating current choromosome
        """
        self.genes = []
        for gene_i in genes:
            self.genes.append(gene_i)

    def copy(self):
        """
        Creating a new individual
        """
        ind = Individual(self.genSize, self.data,'random')
        for i in range(0, self.genSize):
            ind.genes[i] = self.genes[i]
        ind.fitness = self.getFitness()
        ind.distance = self.getDistance()
        return ind

    def euclideanDistance(self, c1, c2):
        """
        Distance between two cities
        """
        d1 = self.data[c1]
        d2 = self.data[c2]
        return math.sqrt( (d1[0]-d2[0])**2 + (d1[1]-d2[1])**2 )

    def getFitness(self):
        return self.fitness

    def getDistance(self):
        return self.distance

    def computeFitness(self):
        """
        Computing the cost or fitness of the individual
        """
        self.fitness    = self.euclideanDistance(self.genes[0], self.genes[len(self.genes)-1])
        for i in range(0, self.genSize-1):
            self.fitness += self.euclideanDistance(self.genes[i], self.genes[i+1])
        
        self.distance=self.fitness
        self.fitness=10000000000/self.fitness