""" bank12: Multiple runs of the bank with a Monitor"""
from SimPy.Simulation import *
from random import expovariate, seed
from SimPy.SimPlot import *
import pylab
## Model components ------------------------


class Source(Process):
    """ Source generates customers randomly"""

    def generate(self, number, interval, resource, mon):
        for i in range(number):
            c = Customer(name="Customer%02d" % (i))
            activate(c, c.visit(b=resource,M=mon))     #1
            t = expovariate( interval)
            yield hold, self, t


class Customer(Process):
    """ Customer arrives, is served and leaves """

    def visit(self, b,M):        
        M.observe(len(b.waitQ)+len(b.activeQ) )
        yield request, self, b
        tib = expovariate( timeInBank)
        yield hold, self, tib        
        yield release, self, b

## Experiment data -------------------------

maxNumber = 100000
maxTime = 10000000.0  # minutes
timeInBank = 1.0   # service rate 1/mu mean, minutes
ARRint = 1.0/0.5     # mean, minutes
Nc = 1            # number of servers
theSeed = 99997
thelambda =1.0/0.5  #mean, arrival rate  1/lambda
## Model  ----------------------------------


def model(thelambda):                             #2
    seed(theSeed)
    k = Resource(capacity=Nc, name="Clerk", monitored=True, monitorType=Monitor)
    nM = Monitor()                                      #3

    initialize()
    s = Source('Source')
    activate(s, s.generate(number=maxNumber, interval=thelambda,
                          resource=k, mon = nM), at=0.0)  #4
    simulate(until=maxTime)
    return ( k.waitMon.mean()+k.actMon.mean(), nM.mean()  ) 
    #print('(TimeAverage no. waiting: %s' % k.waitMon.mean())
    #return ( k.waitMon.mean()+k.actMon.mean())                      #5
## Experiment/Result  ----------------------------------

thelambdas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7 , 0.8 ,0.9, 0.95]     #6
SimTimeResults=[]
SimNumResults=[]
for Sd in thelambdas:
    result = model(Sd)
    SimTimeResults.append(result[0])
    SimNumResults.append(result[1])
print SimTimeResults   #7
print SimNumResults    
### Numerical result
timeAver=[]
numAver=[]
time2=[]
for Sd in thelambdas:
   timeAver.append(1/(timeInBank-Sd)) # time average 1/ (mu - lambda)
   numAver.append(Sd/(timeInBank-Sd))  # number of customer average lambda/(mu-lambda)
    

###Ploting   

p1,=pylab.plot(thelambdas,numAver,'r:' )
p2,=pylab.plot(thelambdas,SimNumResults,'y^' )
pylab.xlabel("Arrival rate")
pylab.ylabel("The average number of customer in the system" )
pylab.grid(True)
pylab.legend([p1,p2], [" Analysis", "Simulation"])
pylab.show()


p3,=pylab.plot(thelambdas,timeAver,'r--' )
p4,=pylab.plot(thelambdas,SimTimeResults,'yo' )
pylab.xlabel("Arrival rate")
pylab.ylabel("The average waiting time in the system" )
pylab.grid(True)

pylab.legend([p3,p4], [" Analysis", "Simulation"])
pylab.show()
