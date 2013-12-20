#introduction  Simpy example: 2 machines, sometimes break down.
#up time exponentially distributed with mean 1, repair time is 
#exponentially distributed with mean 0.5. 2 repairman
#output is long-run proportion of up time 
import SimPy.Simulation #required
import random
class G: #global variables
    Rnd=random.Random(12345)
class MachineClass(SimPy.Simulation.Process):
    UpRate=1/1.0 # reciprocal(ca hai ben, thuan nghich) of mean up time
    RepairRate=1/0.5 #reciprocal of mean repair time
    TotalUpTime=0.0 #total up time for all machines
    NextID=0 #next available ID number for MachineClass objects
    
    def __init__(self): #required constructor
        SimPy.Simulation.Process.__init__(self) #must call parent constructor
        #instance variable   
        self.StartUpTime =0.0 # time the current up period started
        self.ID=MachineClass.NextID #ID for this MachineClass object
        MachineClass.NextID+=1
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
            RepairTime=G.Rnd.expovariate(MachineClass.RepairRate)
            #hold for exponentially distributed repair time
            print"I am repairing ar ",SimPy.Simulation.now()
            yield SimPy.Simulation.hold,self,RepairTime
def main():
    SimPy.Simulation.initialize() #required
    #set up the two machine threads
    for I in range(3):
    #create a machineClass object
        M=MachineClass()
    #register thread M, excuting M's Run() method
        SimPy.Simulation.activate(M,M.Run()) #required
        #run until simulated time 10000
    MaxSimtime =10.0
    SimPy.Simulation.simulate(until=MaxSimtime) #required
    print "the percentage of up time was", MachineClass.TotalUpTime/(2*MaxSimtime)
if __name__ == '__main__': main()
