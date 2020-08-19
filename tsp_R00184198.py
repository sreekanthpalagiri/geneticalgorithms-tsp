"""
Author: Sreekanth Palagiri
file:
Rename this file to TSP_x.py where x is your student number 
"""
import os
import sys 
import random
import string
import logging
from datetime import datetime
import numpy as np
from prolibs.plotmodule import plotfit
from matplotlib.lines import Line2D
from prolibs.Individual import Individual
import statistics
import csv

# set system path
directory = os.getcwd()
sys.path.insert(0,directory+"/prolibs")
sys.path.insert(0,directory+"/TSPdataset")
sys.path.insert(0,directory+"/files")

logging.basicConfig(level=logging.ERROR, filename=directory+"/files/"+"logfile.txt",
                    format="%(message)s")

# seed program for consistent results with student id
myStudentNum = 184198 
random.seed(myStudentNum)

config = {1:['random','uniformCrossover','inversionMutation','randomSelection'],
            2:['random','pmxCrossover','reciprocalExchangeMutation','randomSelection'],
            3:['random','uniformCrossover','reciprocalExchangeMutation','stochasticUniversalSampling'],
            4:['random','pmxCrossover','reciprocalExchangeMutation','stochasticUniversalSampling'],
            5:['random','pmxCrossover','inversionMutation','stochasticUniversalSampling'],
            6:['random','uniformCrossover','inversionMutation','stochasticUniversalSampling'],
            7:['NearestNeighbour','pmxCrossover','inversionMutation','stochasticUniversalSampling'],
            8:['NearestNeighbour','uniformCrossover','inversionMutation','stochasticUniversalSampling']
            }

#variables for plotting
iteration = []
timeperiter=[]
bestdistance=[]
bestfitness=[]
averagefitness=[]
minfitness=[]
maxfitness=[]
medianfitness=[]


class BasicTSP:
    def __init__(self, _fName, _popSize, _mutationRate, _maxIterations):
        """
        Parameters and general variables
        """
        self.population     = []
        self.matingPool     = []
        self.best           = None
        self.popSize        = _popSize
        self.genSize        = None
        self.mutationRate   = _mutationRate
        self.maxIterations  = _maxIterations
        self.iteration      = 0
        self.now            = datetime.now()
        self.fName          = _fName
        self.data           = {}

        self.readInstance()
        self.initPopulation()

    def readInstance(self):
        """
        Reading an instance from fName
        """
        file = open(directory+'//TSPdataset//'+self.fName, 'r')
        self.genSize = int(file.readline())
        self.data = {}
        for line in file:
            (id, x, y) = line.split()
            self.data[int(id)] = (int(x), int(y))
        file.close()
 
    def initPopulation(self):
        """
        Creating random individuals in the population
        """
        for i in range(0, self.popSize):
            individual = Individual(self.genSize, self.data,config[confignum][0])
            individual.computeFitness()
            self.population.append(individual)

        self.best = self.population[0].copy()
        for ind_i in self.population:
            if self.best.getFitness() > ind_i.getFitness():
                self.best = ind_i.copy()
            logging.error(ind_i.genes)
        print ("Best initial sol: Distance",self.best.getDistance(),' Fitness:', self.best.getFitness())

    def updateBest(self, candidate):
        if self.best == None or candidate.getFitness() > self.best.getFitness():
            self.best = candidate.copy()
            print('Best Fitness:',candidate.getFitness(),' Iteration:',self.iteration)
           

    def randomparentSelection(self):
        """
        Random (uniform) selection of two individuals
        """
        indA = self.matingPool[ random.randint(0, self.popSize-1) ]
        indB = self.matingPool[ random.randint(0, self.popSize-1) ]
        return [indA, indB]

    def stochasticUniversalSampling(self):
        """
        Your stochastic universal sampling Selection Implementation
        """
        logging.info('Population before stochastic selection at iteration:'+ str(self.iteration))
        popfit=[] # Use to log population fitness in log, not used in logic 
        for i in range(self.popSize):
            logging.info(self.population[i].genes) # logging info for validation   
            popfit.append(self.population[i].fitness)
        logging.info(popfit)

        self.matingPool = []
        f=sum(i.fitness for i in self.population) #Sum of fitness values
        p=f/self.popSize # Distance between successive points
        rn = random.uniform(0,p)  #generating random number rn as starting point
        logging.info('f:'+str(f)+' p:'+str(p)+' rn:'+str(rn)+' popsize:'+str(self.popSize)) # logging info for validation
        """
        creating N pointers of length rn+p*1,rn+P*2,...rn+P*N  where p is distance between points 
        and N is popsize. We are considering population size as no. of parents 
        """
        pointers =[ rn + i*p for i in range(self.popSize) ]
        logging.info('pointers:')# logging info for validation
        logging.info(pointers)# logging info for validation
        """Pseudo code:
            For each pointer i in pointers, while fitness sum of Population[0..j] < P
             j++
             add Population[j] to matingpool. 
        """
        for i in range(len(pointers)):
            j,fitsubtotal=0,self.population[0].fitness
            while (fitsubtotal <= pointers[i]):
                j+=1
                fitsubtotal+=self.population[j].fitness
            self.matingPool.append(self.population[j].copy())
        logging.info('Population After stochastic selection (selection of mating pool):')
        for i in range(len(self.matingPool)):
            logging.info(self.matingPool[i].genes) # logging info for validation  
            
    def uniformCrossover(self, indA, indB):
        """
        Uniform Crossover Implementation
        """
        selector = [random.randint(0, 1) for i in range(self.genSize)]#1 position doesnt change, 0 position changes
        selector = ['' if a==0 else 1 for a in selector] #replace space with empty
        A=[a if b!= '' else '' for a,b in zip(indA.genes,selector)] #make a new child with spaces where genes can be replaced
        B=[a if b!= '' else '' for a,b in zip(indB.genes,selector)] #make a new child with spaces where genes can be replaced
        #iterate trough parent, if gene is not present in child add it at first empty space
        for i in indB.genes:
            if i in A:
                pass
            else:
                for j in range(len(A)):
                    if A[j] == '':
                        A[j]=i
                        break
        for i in indA.genes:
            if i in B:
                pass
            else:
                for j in range(len(B)):
                    if B[j] == '':
                        B[j]=i
                        break
        indA.genes,indB.genes= A,B

    def pmxCrossover(self, indA, indB):
        """
        PMX Crossover Implementation
        """
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)
        A = ['']* min(indexA,indexB) + indA.genes[min(indexA,indexB):max(indexA,indexB)] + [''] * (self.genSize - max(indexA,indexB))
        B = ['']* min(indexA,indexB) + indB.genes[min(indexA,indexB):max(indexA,indexB)] + [''] * (self.genSize - max(indexA,indexB))
        for a, b in zip(indA.genes[min(indexA,indexB):max(indexA,indexB)],indB.genes[min(indexA,indexB):max(indexA,indexB)]):
            if b not in A:
                x=indB.genes.index(a)
                while A[x] !='':
                    x=indB.genes.index(A[x])
                A[x]=b  
            if a not in B:
                y=indA.genes.index(b)
                while B[y] !='':
                    y=indA.genes.index(B[y])
                B[y]=a  
        for i in range(self.genSize):
            if A[i] == '':
                A[i] = indB.genes[i]
            if B[i] == '':
                B[i] = indA.genes[i]

        indA.genes=A
        indB.genes=B

    def reciprocalExchangeMutation(self, ind):
        """
        Your Reciprocal Exchange Mutation implementation
        """
        if random.random() > self.mutationRate:
            return
            
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp
        
    def inversionMutation(self, ind):
        """
        Inversion Mutation implementation
        """
        if random.random() > self.mutationRate:
            return
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)
        tmp=ind.genes[min(indexA,indexB):max(indexA,indexB)]
        tmp.reverse()
        ind.genes[min(indexA,indexB):max(indexA,indexB)]=tmp
        
    def crossover(self, indA, indB):
        """
        Executes a 1 order crossover and returns a new individual
        """
        child = []
        tmp = {}

        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        for i in range(0, self.genSize):
            if i >= min(indexA, indexB) and i <= max(indexA, indexB):
                tmp[indA.genes[i]] = False
            else:
                tmp[indA.genes[i]] = True
        aux = []
        for i in range(0, self.genSize):
            if not tmp[indB.genes[i]]:
                child.append(indB.genes[i])
            else:
                aux.append(indB.genes[i])
        child += aux
        return child

    def mutation(self, ind):
        """
        Mutate an individual by swaping two cities with certain probability (i.e., mutation rate)
        """
        if random.random() > self.mutationRate:
            return
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp

        ind.computeFitness()
        self.updateBest(ind)

    def randomSelection(self):
        """
        Updating the mating pool before creating a new generation
        """
        self.matingPool = []
        for ind_i in self.population:
           self.matingPool.append( ind_i.copy() )
 
    def newGeneration(self):
        for i in range(0, round(self.popSize/2)):
            """
            Depending of your experiment you need to use the most suitable algorithms for:
            1. Select two candidates
            2. Apply Crossover
            3. Apply Mutation
            """
            indA, indB = self.randomparentSelection()
            logging.info('Randomly selected parents for mating:'+ str(indA.genes)  + str(indB.genes))
            getattr(ga,config[confignum][1])(indA, indB)
            logging.info('After '+ config[confignum][1] +':'+ str(indA.genes)  + str(indB.genes))
            getattr(ga,config[confignum][2])(indA)
            logging.info('After Parent 1 '+ config[confignum][2] +':'+ str(indA.genes)  + str(indB.genes))
            getattr(ga,config[confignum][2])(indB)
            logging.info('After Parent 2 '+ config[confignum][2] +':'+ str(indA.genes)  + str(indB.genes))
            
        print ("iteration: ",self.iteration, "Best Distance: ",self.best.getDistance(),"Best Fitness: ",self.best.getFitness())
        logging.info ("iteration: "+ str(self.iteration)+" best distance:"+ str(self.best.getDistance())+" best Fitness:"+str(self.best.getFitness()))
        logging.info ("Gene with best Fitness:"+ str(self.best.genes))
            
    def GAStep(self):
        """
        One step in the GA main algorithm
        1. Updating mating pool with current population
        2. Creating a new Generation
        """
        getattr(ga,config[confignum][3])()
        self.newGeneration()
    
        #updating fitness of new generation and catpuring statistics    
        iteration.append(self.iteration)
        fitness =[]
        for ind in self.matingPool:
            ind.computeFitness()
            self.updateBest(ind)
            fitness.append(ind.getFitness())
        self.population=self.matingPool
                    
        bestdistance.append(self.best.getDistance())
        bestfitness.append(self.best.getFitness())
        averagefitness.append(statistics.mean(fitness))
        minfitness.append(min(fitness))
        maxfitness.append(max(fitness))
        medianfitness.append(statistics.median(fitness))
        timetaken = datetime.now() - self.now
        timeperiter.append(timetaken.microseconds/1000)
        self.now = datetime.now()
       
    def search(self):
        """
        General search template.
        Iterates for a given number of steps
        """
        self.iteration = 0
        while self.iteration < self.maxIterations:
            self.GAStep()
            self.iteration += 1
        print ("Total iterations: ",self.iteration)
        print ("Best Solution: Distance - ",self.best.getDistance(),' Fitness:', self.best.getFitness())
        print("Gene with best Fitness:", str(self.best.genes))
        with open(directory+"/files/"+"configstats.csv", mode='a') as stats_file:
            stats_file_writer = csv.writer(stats_file)
            stats_file_writer.writerow(['Configuration '+str(confignum),self.iteration,self.best.getFitness(),self.best.getDistance(),statistics.mean(timeperiter),(sum(timeperiter)/1000)])
        stats_file.close()

if len(sys.argv) < 2:
    print ("Error - Incorrect input")
    print ("Expecting python BasicTSP.py [instance] ")
    sys.exit(0)

problem_file = sys.argv[1]

print('Please choose configuration from below:')
for i in config:
    print(i,':',config[i])
confignum = int(input())

if confignum < 1 or confignum > 8 :
    print ("Error - Incorrect input for config")
    sys.exit(0)

ga = BasicTSP(problem_file, 300, 0.1, 500)
ga.search()
filename = directory+"/files/"+'Configuration '+str(confignum)
plotfit(iteration,bestfitness,averagefitness,medianfitness,minfitness,maxfitness,filename,'Configuration '+str(confignum))
