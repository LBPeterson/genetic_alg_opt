### GENETIC ALGORITHM EXAMPLE TSP
### LUKE PETERSON 06/30/2016
### INFO: https://en.wikipedia.org/wiki/Genetic_algorithm
import numpy as np
from scipy.spatial import distance as dist
import copy
import matplotlib.pyplot as plt

num_gen = 500
num_cities = 30
num_ind = 100
cross_rate = .85
mut_rate = .25
coords = np.random.randint(100, size=(num_cities,2));

def create_population():
    initial = np.array([np.zeros(num_cities)] * num_ind)
    for i in range(0, num_ind):
        initial[i] = np.random.permutation(num_cities)
    return initial

def get_distance(path):
    total = 0
    for i in range(0,num_cities-1):
        cur = path[i]
        nex = path[i+1]
        total += dist.euclidean(coords[cur], coords[nex])
    total += dist.euclidean(coords[0], coords[num_cities-1])
    return total**3

# Selection is using the roulette wheel process
def selection():
    wheel = []
    normal = [sum(score)/x for x in score]
    for i in range(1, num_ind+1):
        wheel.append(sum(normal[:i]))
    
    parents = np.array(np.zeros(num_ind * 2))    
    wheel = np.array([wheel])
    
    sum_normal = sum(normal)
    for i in range(num_ind * 2):
        parents[i] = np.argmax(wheel > np.random.rand() * sum_normal )
        
    parents = np.reshape(parents, (num_ind,2))
    return parents
    
# This takes the parent matrix and returns the next generation
# Crossover method is "MX" modified crossover
def crossover(parents):
    next_gen = np.array([np.zeros(num_cities)])
    
    for couple in parents:
        if np.random.rand() < cross_rate:
            p1 = pop[couple[1]]
            p2 = pop[couple[0]]
            child = np.array([])
            split = np.random.randint(1, num_cities+1)
            
            child = np.append(child, p1[:split])
            for each in p2:
                if each not in child:
                    child = np.append(child, each)
            next_gen = np.append(next_gen, [child], axis=0)
        else:
            p1 = pop[couple[1]]
            next_gen = np.append(next_gen, [p1], axis=0)
    return next_gen[1:]
                
        
# mutation will take in the next generation array and randomly mutate 
# some individuals by switching them         
def mutation(pop):
    for each in pop:
        if np.random.rand() < mut_rate:
            places = np.random.randint(0, num_cities, size=(2))
            temp = each[places[0]]
            each[places[0]] = each[places[1]]
            each[places[1]] = temp
            
    
### START ###
pop = create_population()
for i in range(0,num_gen+1):
    score = np.array([ get_distance(x) for x in pop])
    parents = selection()
    new = crossover(parents)
    mutation(new)  

    newscore = np.array([ get_distance(x) for x in new])   
    bestold = np.argmin(score) 
    worstnew = np.argmax(newscore)
           
    if i % 10 == 0:
        plotx = [ coords[x][0] for x in pop[bestold] ]
        ploty = [ coords[x][1] for x in pop[bestold] ]
        plt.plot(coords[:,0], coords[:,1], 'ro' )
        plt.plot(plotx, ploty)
        #plt.show()
        #print("Generation %s Best Score: %d" % (i,min(score)))
        
        name = "0000000" + str(i)
        name = name[-4:] + '.png'
        plt.savefig(name, bbox_inches='tight')
        plt.close("all")
        
    
	# Elitism: The best individual will carry on to the next generation
    new[worstnew] = pop[bestold]
    pop = copy.deepcopy(new)

   