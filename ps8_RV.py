# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:

from __future__ import division 

import numpy
import random
import pylab
from ps7_RV import *

import matplotlib.pyplot as plt

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb
        



    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        if drug in self.resistances:
            return self.resistances[drug]
            print 'in key'
        else:
            return False


    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """

        #check if the virus is resistant to all the active drugs
        resistToDrugs = True
        for drug in activeDrugs:
            #self.isResistantTo(drug)
            if self.isResistantTo(drug) == False:
                resistToDrugs = False

        #if the virus is resistant to the active drugs than determine if it repoduces
        if resistToDrugs == True: 
            repro = random.randint(1,100)
            if repro < self.maxBirthProb*100*(1-popDensity):
                newVirus = ResistantVirus(self.maxBirthProb, self.clearProb, self.resistances, self.mutProb)
                newVirus.updateResistances()
                return newVirus
##            else:
##                return None

    def updateResistances(self):
        #updates the resistances of a virus
        #this method is used in the reproduce method above

        for drug in self.resistances:
            probability = random.randint(1,100)
            if probability < self.mutProb*100:
                self.changeResistance(drug)

    def changeResistance(self,drug):
        #this method is used in the updateResistances metod above
        if self.resistances[drug] == True:
            self.resistances[drug] = False
        else:
            self.resistances[drug] = True
        

            

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop
        self.TotalPop = len(viruses)
        self.Drugs = []
    

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """

        if newDrug not in self.Drugs:
            self.Drugs.append(newDrug)


    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.Drugs
        

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        resistantPop = 0

        for virus in self.viruses:
            addToPop = True
            for drug in self.Drugs:
                if virus.isResistantTo(drug) == False:
                    addToPop = False
            if addToPop == True:
                resistantPop += 1    


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
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

         #step 3
        for virus in self.viruses:
            #self.viruses.append(virus.reproduce(self.TotalPop/self.maxPop, self.Drugs))
            newVirus = virus.reproduce(self.TotalPop/self.maxPop, self.Drugs)
            if newVirus is not None:
                self.viruses.append(newVirus)
        self.TotalPop = len(self.viruses)


#
# PROBLEM 2
#

def simulationWithDrug(NumberSteps,NumberVirusesInitial,MaxNumberOfViruses,ClearRate,RepoRate, resistances, mutProb):

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """

    #Creates the initial list of viruses
    LstOfViruses = []
    for x in range(NumberVirusesInitial):
        LstOfViruses.append(ResistantVirus(RepoRate,ClearRate,resistances,mutProb))

    #Creates the patient 
    Patient1 = Patient(LstOfViruses, MaxNumberOfViruses)

    #Creates the lists to track the population
    VirusPopulation = []

    for i in range(NumberSteps):
        VirusPopulation.append(Patient1.getTotalPop())
        Patient1.update()

    Patient1.addPrescription('guttagonol')

    for i in range(150):
        VirusPopulation.append(Patient1.getTotalPop())
        Patient1.update()   

    
    plt.plot(VirusPopulation,'rs')
    plt.ylabel('Virus Population')
    plt.xlabel('Time')
    plt.title('Virus Pupulation Through Time')
    plt.show()


#Create a list of resistances for testing
resistancesList = {'guttagonol':True}

#Create a list of active drugs


simulationWithDrug(150,10,500,0.05,0.5,resistancesList,0.02)

#
# PROBLEM 3
#        

def simulationDelayedTreatment():

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """

    # TODO

#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    # TODO



#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations():

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    #TODO



