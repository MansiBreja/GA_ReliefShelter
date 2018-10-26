import csv
import geopy as gp
import os
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import folium
import time
import random
from datetime import datetime
import sys
from random import randint
import geopy.geocoders
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="GA")
from geopy.exc import GeocoderTimedOut
from geopy import distance
random.seed(7561)
#Choosing population size
POP_SIZE = 30
Number_of_gens=100
P= 7
Budget = 100000000
K= 30 # the number of times of current population that can be handled by a shelter
NUM_LOCATIONS= 50
CROSSOVER_RATE =0.7
MUTATION_RATE  =0.01

datafile=pd.read_csv('dataset2.csv')
data= datafile[175:225]
AreaLocations= [ ]
locations= list(data['Location'])
AreaPopulations= list(data['Population'])
AreaNODLs=list(data['Number of days before submerging'])
AreaCosts=list(data['Cost of setup'])
AreaLatitudes=list(data['latitude'])
AreaLongitudes=list(data['longitude'])


def sigmoid(x):
        #print "inside sigmoid"
        # sys.stdout.flush()
        return 1 / (1 + math.exp(-x))

def nearestShelter(Shelterset,locn):
        #print "inside nearestShelter"
        distances= np.zeros(P)
        for i in range(P):
                distances[i]= distance.vincenty((AreaLatitudes[ Shelterset[i]],AreaLongitudes[Shelterset[i]]),(AreaLatitudes[locn],AreaLongitudes[locn])).miles
        return np.argmin(distances)

def AssignShelters(chromosome):
        #print "inside AssignShelters"
        sys.stdout.flush()
        ShelterList= [ [ ] for i in range(P) ]
        for i in range(NUM_LOCATIONS):
                if i not in chromosome:
                        ShelterList[nearestShelter(chromosome,i)].append(i)
        return ShelterList

def checkConstraints(chromosome,ShelterList,test=1):
        #print "inside Checkconstraints"
        for i in range(P):
                sumPopulation=0
                if(AreaNODLs[chromosome[i]]==0):
                        if(not test):
                                print("zero NODL constraint violated")
                        return False
                for j in range(len(ShelterList[i])):

                        #if AreaNODLs[ShelterList[i][j]]>AreaNODLs[chromosome[i]]:
                                #return False
                        sumPopulation+= AreaPopulations[ShelterList[i][j]]
                sumPopulation+=AreaPopulations[chromosome[i]]
                if sumPopulation>K*AreaPopulations[chromosome[i]]:
                        if(not test):
                                print("K times constraint violated")
                                print(sumPopulation//AreaPopulations[chromosome[i]])
                        return False
        return True



def calcPopScore(chromosome,ShelterList):
        PopScore=0
        for i in range(P):
                for j in range(len(ShelterList[i])):
                        PopScore+= AreaPopulations[ShelterList[i][j]]/(1.0000+(gp.distance.vincenty( (AreaLatitudes[chromosome[i]],AreaLongitudes[chromosome[i]]),(AreaLatitudes[ShelterList[i][j]],AreaLongitudes[ShelterList[i][j]])).miles ))
        return PopScore

def calcMaxAvgDist(chromosome,ShelterList):
        maxDist=0
        for i in range(P):
                sumDist=0
                for j in range(len(ShelterList[i])):
                        sumDist+= gp.distance.vincenty( (AreaLatitudes[chromosome[i]],AreaLongitudes[chromosome[i]]),(AreaLatitudes[ShelterList[i][j]],AreaLongitudes[ShelterList[i][j]])).miles
                if len(ShelterList[i]):
                        maxDist=max(maxDist,sumDist/len(ShelterList[i]))
        return maxDist

def calcCost(chromosome,ShelterList):
        cost = 0
        for i in range(P):
                cost_i=0
                days_i=AreaNODLs[chromosome[i]]
                nodls_of_surrounding=[AreaNODLs[j] for j in ShelterList[i]]
                if len(nodls_of_surrounding):
                        days_i=min(days_i,max(nodls_of_surrounding))
                for j in range(len(ShelterList[i])):
                        if AreaNODLs[ShelterList[i][j]]<days_i:
                                cost_i= cost_i+ (AreaPopulations[ShelterList[i][j]]*(days_i-AreaNODLs[ShelterList[i][j]]) )
                cost = cost + (cost_i * AreaCosts[chromosome[i]])
        return cost

def generateChromosome() :
        a_set = set()
        while True:

                a_set.add(randint(0,NUM_LOCATIONS-1))
                if len(a_set)==P:
                        break

        chromosome = (list(a_set))
        print(chromosome)
        sys.stdout.flush()
        return chromosome
# Generating initial population
def initialpop() :

        i = 0
        pop = []
        while i != POP_SIZE :
                chromosome = generateChromosome()
                while  True :
                        if(isValid(chromosome)):
                                break
                        # time.sleep(0.8)
                        chromosome = generateChromosome()
                i = i + 1
                # print("%s chromosomes accepted" %i)
                pop.append(chromosome)
        return pop

# Checking if all  locations of the chromosome follow the constraints
def isValid(chromosome):
        ShelterList= AssignShelters(chromosome)
        cost=calcCost(chromosome,ShelterList)
        print(cost)
        if( (not checkConstraints(chromosome,ShelterList,0))):
                return False
        if(cost>Budget):
                print("Cost constraint violated")
                return False
        return True

def fitness_chromosome(chromosome):
        ShelterList= AssignShelters(chromosome)
        cost= calcCost(chromosome,ShelterList)
        if( (not checkConstraints(chromosome,ShelterList)) or cost>Budget):
                return 0
        popsc=calcPopScore(chromosome,ShelterList)
        dist=calcMaxAvgDist(chromosome,ShelterList)
        cost=calcCost(chromosome,ShelterList)
        # print(popsc)
        # print(cost)
        # print(dist)
        return ((popsc/(10**3))+ (cost/(10**5)))/(dist)

# Returns list of fitness values of all the chromosomes of my population
def fitness_pop(pop) :
        pop_fitness_list = []
        for i in range(0, POP_SIZE) :
                pop_fitness_list.append(fitness_chromosome(pop[i]))
        return pop_fitness_list

def avg_fitness_pop(pop):
        fitness=0
        for i in range(0, POP_SIZE) :
                fitness += fitness_chromosome(pop[i])
        return fitness/POP_SIZE

def best_chromosome(pop):
        maxFitness=0
        for i in range(POP_SIZE):
                temp_fitness= fitness_chromosome(pop[i])
                if temp_fitness>maxFitness:
                        best=pop[i]
                        maxFitness=temp_fitness
        return best

def probability_calc(pop):
    fitness = fitness_pop(pop)
    total_fit = float(sum(fitness))
    relative_fitness = [f/total_fit for f in fitness]
    probabilities = [sum(relative_fitness[:i+1]) for i in range(len(relative_fitness))]
    return probabilities

def roulette_wheel_pop(pop, probabilities):
        r = random.random()
        for (i, individual) in enumerate(pop):
                if r < probabilities[i]:
                        return list(individual)



def mutate(chromo):
        for i in range(P):
                r=random.random()
                if(r<MUTATION_RATE):
                        new_val=random.randint(0,NUM_LOCATIONS-1)
                        while new_val in chromo:
                                new_val=random.randint(0,NUM_LOCATIONS-1)
                        chromo[i]=new_val


def crossover(chromo1,chromo2):
        new_chromo1=[]
        new_chromo2=[]
        for i in range(P):
                new_chromo1.append(chromo1[i])
                new_chromo2.append(chromo2[i])
        r=random.random()
        if( r<CROSSOVER_RATE):
                crossover_point=random.randint(0,P-1)
                j= 0
                for i in range(P):
                        if chromo2[i] not in chromo1:
                                new_chromo1[j]=chromo2[i]
                                j= j+1
                                if(j>crossover_point):
                                        break
                j=0
                for i in range(P):
                        if(chromo1[i]) not in chromo2:
                                new_chromo2[j]=chromo1[i]
                                j= j+1
                                if(j>crossover_point):
                                        break
        for i in range(P):
                chromo1[i]=new_chromo1[i]
                chromo2[i]=new_chromo2[i]

def next_gen(pop,probabilities):
        next_gen=[]
        for i in range(POP_SIZE//2):
                chromo1=roulette_wheel_pop(pop,probabilities)
                chromo2=roulette_wheel_pop(pop,probabilities)
                crossover(chromo1,chromo2)
                mutate(chromo1)
                mutate(chromo2)
                next_gen.append(chromo1)
                next_gen.append(chromo2)
        return next_gen


#Run main code
current_population= initialpop()
#print(current_population)
gen_fitness=[]
for i in range(Number_of_gens):
        probabilities=probability_calc(current_population)
        print(avg_fitness_pop(current_population) )
        gen_fitness.append(avg_fitness_pop(current_population))
        sys.stdout.flush()
        current_population=next_gen(current_population,probabilities)

bc=best_chromosome(current_population)
print(bc)

m = folium.Map(
    location=[10.850516,76.271080],
    zoom_start=12,
    # tiles='Stamen Terrain'
)

tooltip = 'Click me!'
for i in range(0, P) :
    folium.Marker([AreaLatitudes[bc[i]],AreaLongitudes[bc[i]]], popup=locations[bc[i]], tooltip=tooltip).add_to(m)

m.save('index.html')

plt.plot(list(range(1,101)), gen_fitness)
plt.ylabel('Avg fitness values')
plt.xlabel('Generations')
plt.show()
