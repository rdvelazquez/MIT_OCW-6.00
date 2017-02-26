# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name:
# Collaborators:
# Time:
from __future__ import division 
import numpy
import random
import pylab
import matplotlib.pyplot as plt


''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """

        clear = random.randint(1,100)
        if clear < self.clearProb*100:
            return True
        else:
            return False

    
    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        repro = random.randint(1,100)
        if repro < self.maxBirthProb*100*(1-popDensity):
            return True
        else:
            return False

    def getMaxBirthProb(self):
        return self.maxBirthProb

    def getClearProb(self):
        return self.clearProb
    

class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a  of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop
        self.TotalPop = len(viruses)

    def getTotalPop(self):

        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """

        return self.TotalPop


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        #step 1
        newViruses = []
        for virus in self.viruses:
            if virus.doesClear() is False:
                newViruses.append(virus)
        self.viruses = newViruses
        
        #step 2
        self.TotalPop = len(self.viruses)
##        print 'The population after clearing is:'
##        print self.TotalPop

        #step 3
        NumNewViruses = 0
        for virus in self.viruses:
            if virus.reproduce(self.TotalPop/self.maxPop) is True:
                NumNewViruses += 1
##	print 'NumNewViruses: %i' %NumNewViruses
        for i in range(NumNewViruses):
            self.viruses.append(self.viruses[0])
        self.TotalPop = len(self.viruses)
##        print 'and after reproducing:'
##        print self.TotalPop
   
        
        
                


###test for update Only works with the print statments in the update function which will be commented out
##print 'UPDATE TEST'
##
###make a list of 10 viruses to test
##LstOfViruses = []
##for x in range(100):
##    LstOfViruses.append(SimpleVirus(0.95,0.25))
##
##Patient1 = SimplePatient(LstOfViruses,1000)
##
##print Patient1.getTotalPop()
##
##Patient1.update()    
##Patient1.update()
##Patient1.update()
##Patient1.update()


#
# PROBLEM 2
#
def simulationWithoutDrug(NumberSteps,NumberVirusesInitial,MaxNumberOfViruses,ClearRate,RepoRate):

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """

    #Creates the initial list of viruses
    LstOfViruses = []
    for x in range(NumberVirusesInitial):
        LstOfViruses.append(SimpleVirus(RepoRate,ClearRate))

    #Creates the patient 
    Patient1 = SimplePatient(LstOfViruses, MaxNumberOfViruses)

    #Creates the lists to track the population
    VirusPopulation = []

    for i in range(NumberSteps):
        VirusPopulation.append(Patient1.getTotalPop())
        Patient1.update()

    
    plt.plot(VirusPopulation)
    plt.ylabel('Virus Population')
    plt.xlabel('Time')
    plt.title('Virus Pupulation Through Time')
    plt.show()


simulationWithoutDrug(300,100,2000,0.05,0.1)

#
#PROBLEM 3
#

#Yahtzee! Simulation

def RollDice():
    return random.randint(1,6)

def RollNumDice(numberOfDice):
    result = []

    for x in range(numberOfDice):
        result.append(RollDice())

    return result

def TestIfYahtzee(SixDice):
    Yahtzee = True
    for i in range(1,7):
        if i not in SixDice:
            Yahtzee = False

    return Yahtzee


def SimulationTest(NumberOfTrials):
    for i in range(1,NumberOfTrials+1):
        Roll = RollNumDice(6)
        print str(Roll).strip('[]')
        print TestIfYahtzee(Roll)
        TestIfYahtzee(Roll)
        

def MonteCarlo(NumberOfTrials):
    NumberOfYahtzees = 0
    for i in range(1,NumberOfTrials+1):
        Roll = RollNumDice(6)
        #print str(Roll).strip('[]')
        #print TestIfYahtzee(Roll)
        if TestIfYahtzee(Roll):
            NumberOfYahtzees += 1
    YahtzeeProb = 100*round((int(NumberOfYahtzees)/NumberOfTrials),4)
    print 'The probability of getting Yahtzee is %.2f percent' %YahtzeeProb    


#MonteCarlo(10000)
