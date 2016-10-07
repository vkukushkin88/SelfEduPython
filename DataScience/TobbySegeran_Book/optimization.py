import time
import random
import math

people = [
    ('Seymour', 'BOS'),
    ('Franny', 'DAL'),
    ('Zooey', 'CAK'),
    ('Walt', 'MIA'),
    ('Buddy', 'ORD'),
    ('Les', 'OMA'),
]

destination = 'LGA'

flights = {}

for line in open('schedule.txt').readlines():
    origin, dest, depart, arrive, price = line.strip().split(',')
    flights.setdefault((origin, dest), [])
    flights[(origin, dest)].append((depart, arrive, int(price)))

def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3] * 60 + x[4]

def printschedule(r):
    for d in range(len(r)/2):
        try:
            name = people[d][0]
            origin = people[d][1]
            out = flights[(origin, destination)][r[d]]
            ret = flights[(destination, origin)][r[d + 1]]
            print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (
                name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2])
        except KeyError:
            print 'No data for ', (destination, origin)

def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24 * 60

    for d in range(len(sol)/2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d])]
        returnf = flights[(destination, origin)][int(sol[d + 1])]

        totalprice += outbound[2]
        totalprice += returnf[2]

        if latestarrival < getminutes(outbound[1]):
            latestarrival = getminutes(outbound[1])

        if earliestdep > getminutes(returnf[0]):
            earliestdep = getminutes(returnf[0])

    totalwait = 0
    for d in range(len(sol)/2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d])]
        returnf = flights[(destination, origin)][int(sol[d + 1])]

        totalwait += latestarrival - getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep

    if latestarrival > earliestdep: totalprice += 50

    return totalprice + totalwait

def randomoptimize(domain, costf):
    best = 999999999
    bestr = None
    for i in range(1000):
        r = [random.randint(domain[el][0], domain[el][1]) for el in range(len(domain))]
        cost = costf(r)

        if cost < best:
            best = cost
            best = r
    return r

def geneticoptimize(domain, costf, popsize=50, step=1, multprob=0.2, elite=0.2, maxiter=100):
    def mutate(vec):
        i = random.randint(0, len(domain) - 1)
        if random.random() < 0.5 and vec[i] > domain[1][0]:
            return vec[0:i] + [vec[i] - step] + vec[i + 1:]
        elif vec[i] < domain[i][1]:
            return vec[0:i] + [vec[i] + step] + vec[i+1:]

    def crossover(r1, r2):
        i = random.randint(1, len(domain) -2)
        return r1[0:1] + r2[1:]

    pop = []
    for i in range(popsize):
        vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        pop.append(vec)

    topelite = int(elite * popsize)

    for i in range(maxiter):
        scores = [(costf(v), v) for v in pop]
        scores.sort()
        ranked = [v for (s,v) in scores]

        pop = ranked[0:topelite]

        while len(pop) < popsize:
            if random.random() < multprob:
                c = random.randint(0, topelite)
                pop.append(mutate(ranked[c]))
            else:
                c1 = random.randint(0, topelite)
                c2 = random.randint(0, topelite)
                pop.append(crossover(ranked[c1], ranked[c2]))

    return scores[0][1]



