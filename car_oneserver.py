#introduction  Simpy example: 2 machines, sometimes break down.
#up time exponentially distributed with mean 1, repair time is 
#exponentially distributed with mean 0.5. 1 repairman
#output is long-run proportion of up time 
from SimPy.Simulation import* 
from random import Random, expovariate, uniform
class G: #global variables
    Rnd=Random(12345)
    #creat the repairperson
    RepairPerson= Resource(1)
class MachineClass(SimPy.Simulation.Process):
    NRep=0 # number of times the machines have broken down
    NImmedRep=0 # number of breakdowns in which the machine started repair service right away
    UpRate=1/1.0 # reciprocal(ca hai ben, thuan nghich) of mean up time
    RepairRate=1/0.5 #reciprocal of mean repair time
    TotalUpTime=0.0 #total up time for all machines
    NextID=0 #next available ID number for MachineClass objects
    NUp=0 # number of machines currently up
    def __init__(self): #required constructor
        SimPy.Simulation.Process.__init__(self) #must call parent constructor
        #instance variable   
        self.StartUpTime =0.0 # time the current up period started
        self.ID=MachineClass.NextID #ID for this MachineClass object
        MachineClass.NextID+=1
        MachineClass.NUp+=1 #machines start in the up mode
    def Run(self): #required constructor
        while 1:
            #record current time, now(), so can see how long machine is up
            self.StartUpTime=SimPy.Simulation.now()
            print ("Car",self.ID,"is driving at ",self.StartUpTime)
            #hold for exponentially distributed up time
            UpTime=G.Rnd.expovariate(MachineClass.UpRate)#get the rate for exp
            yield SimPy.Simulation.hold,self,UpTime #simulation UpTime (giu den UpTime)
            #update up time total
            MachineClass.TotalUpTime=SimPy.Simulation.now()-self.StartUpTime
            MachineClass.NRep+=1
            #check whether we get repair service immediately
            if G.RepairPerson.n==1:
                MachineClass.NImmedRep+=1
            #need to request, and possibly queue for, the repairperson
            RepairTime=G.Rnd.expovariate(MachineClass.RepairRate)
            #hold for exponentially distributed repair time
            print"I am repairing ar ",SimPy.Simulation.now()
            yield request,self,G.RepairPerson
            #Ok, obtained access to the repairperson; hold for repair time
            yield hold,self,RepairTime
            #repair done, release the repairperson
            yield release, self,G.RepairPerson
def main():
    SimPy.Simulation.initialize() #required
    #set up the two machine threads
    for I in range(2):
    #create a machineClass object
        M=MachineClass()
    #register thread M, excuting M's Run() method
        SimPy.Simulation.activate(M,M.Run()) #required
        #run until simulated time 10000
    MaxSimtime =10.0
    SimPy.Simulation.simulate(until=MaxSimtime) #required
    print'proportion of up time:',MachineClass.TotalUpTime/(2*MaxSimtime)
    print'proportion of times was immediate:',float(MachineClass.NImmedRep)/MachineClass.NRep
    print "the percentage of up time was", MachineClass.TotalUpTime/(2*MaxSimtime)

if __name__ == '__main__': main()
