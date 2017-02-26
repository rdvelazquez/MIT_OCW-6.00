# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab
import matplotlib.pyplot as plt

#close all pre-opned plt windows
plt.close("all")

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False
    
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """

        self.RoomWidth = width
        self.RoomHeight = height
        self.CleanTiles = []
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """

        IntPosition = Position(int(pos.getX()),int(pos.getY()))
        
        if self.isTileCleaned(IntPosition) != True:  
            self.CleanTiles.append(IntPosition)

    def isTileCleaned(self, pos):
        """
        Return True if the tile (pos) has been cleaned. NOTE: original had (m,n) instead of pos

        Assumes that (pos) represents a valid tile inside the room.

        returns: True if (pos) is cleaned, False otherwise
        """

        IntPosition = Position(int(pos.getX()),int(pos.getY()))
        
        if IntPosition in self.CleanTiles:
            return True
        return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.RoomWidth * self.RoomHeight
        
    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """

        return len(self.CleanTiles)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """

        Randomx = random.randint(1,self.RoomWidth)
        Randomy = random.randint(1,self.RoomHeight)
        RandomPos = Position(Randomx,Randomy)
        return RandomPos

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """

        if 0 < pos.getX() <= self.RoomWidth and 0< pos.getY() <= self.RoomHeight:
            return True
        else:
            return False

    def RefreshRoom(self):
        #makes all tiles dirty by clearing the CleanTiles list
        self.CleanTiles[:] = []

    #A method for testing
    #Gets the list of position objects from the 
    def getCleanTiles(self):
        return self.CleanTiles

        

#TEST 1-----------------
#print "test1"
Room1 = RectangularRoom(3,6)

##Test1 = Room1.getWidth1()
##print "the room width is: %d" % Test1
##
##TotalTiles = Room1.getNumTiles()
##print "the room has %d tiles" % TotalTiles
##
##RandomPositionTest = Room1.getRandomPosition()
##X1 = RandomPositionTest.getX()

#Room1.cleanTileAtPosition(Position(1,1))
#test1 = Room1.getNumCleanedTiles()
#print test1

#Room1.cleanTileAtPosition(Position(1,1))
#test2 = Room1.getNumCleanedTiles()
#print test2

#Pos1 = Position(1,2)
#Pos2 = Position(1,2)




class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """

        self.RobotRoom = room
        self.RobotSpeed = speed
        self.RobotPosition = room.getRandomPosition()
        self.RobotDirection = random.randint(1,360)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """

        return self.RobotPosition      
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """

        return self.RobotDirection

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """

        self.RobotPosition = position
        
    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """

        self.RobotDirection = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        #Clean tile at original position
        self.RobotRoom.cleanTileAtPosition(self.RobotPosition)
        
        #Move Robot to new position using the method from the Position class
        self.RobotPosition = self.RobotPosition.getNewPosition(self.RobotDirection,self.RobotSpeed)

        
# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        #Clean tile at original position
        self.RobotRoom.cleanTileAtPosition(self.RobotPosition)
        
        #Move Robot to new position using the method from the Position class
        RobotPositionTrial = self.RobotPosition.getNewPosition(self.RobotDirection,self.RobotSpeed)

        if self.RobotRoom.isPositionInRoom(RobotPositionTrial) is True:
            self.RobotPosition = RobotPositionTrial
        else:
            self.RobotDirection = random.randint(1,360)    


#Test 2------------
##TestRoom = Room1
##print "test2"
##
##TestRobot = StandardRobot(TestRoom,1)
##
##TestRobotPositionInitial = TestRobot.getRobotPosition()
##print 'Robot initial position is X=%d, Y=%d' % (TestRobotPositionInitial.getX(), TestRobotPositionInitial.getY())
##print 'Robot initial direction is %d' %TestRobot.getRobotDirection()
##TestRobot.updatePositionAndClean()


#Cleaned Tile List Printout----------------------------------
##print '\n   CleanedTileList \n'
##print 'There are %d clean tiles' % TestRoom.getNumCleanedTiles()
##CleanTileList = TestRoom.getCleanTiles()
##
##
##for i in CleanTileList:
##
##    print 'Tile number %d' % ListIndex
##    print 'X = %d' % i.getX()
##    print 'Y = %d \n' % i.getY()

        
        

# === Problem 3

def CheckCoverage(room):
    """
    Checks the coverage of a room and returns a decimal percent: if 50% of the rooms tiles are clean the function
    will return 0.50 as a float
    """

    TotalTilesFloat = float(room.getNumTiles())
    CleanedTilesFloat = float(room.getNumCleanedTiles())
    CoverageFloat = CleanedTilesFloat / TotalTilesFloat
    return CoverageFloat
    

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """



    #try with one trial and one robot first (iteration 1 of 3)
##    SimulationRoom = RectangularRoom(width,height)
##    Robot1 = robot_type(SimulationRoom,speed)
##    Coverage = CheckCoverage(SimulationRoom)
##
##    TimeStep = 0
##    while Coverage < min_coverage:
##        Robot1.updatePositionAndClean()
##        Coverage = CheckCoverage(SimulationRoom)
##        print 'number of clean tiles: %f' % SimulationRoom.getNumCleanedTiles()
##        print 'number of tiles: %f' % SimulationRoom.getNumTiles()
##        print 'Percent cleaned: %f' % Coverage
##        TimeStep +=1
##        print 'Timestep %d \n' % TimeStep
##
##    return TimeStep

    #Add multiple trials (iteration 2 of 3)
##    SimulationRoom = RectangularRoom(width,height)
##    Robot1 = robot_type(SimulationRoom,speed)
##    Coverage = CheckCoverage(SimulationRoom)
##
##    TrialNum = 1
##    TimeStepList = []
##    
##    while TrialNum <= num_trials:
##        Coverage = CheckCoverage(SimulationRoom)
##        TimeStep = 0
##        while Coverage < min_coverage:
##            Robot1.updatePositionAndClean()
##            Coverage = CheckCoverage(SimulationRoom)
##            TimeStep +=1
##            
##        TrialNum += 1
##        TimeStepList.append(TimeStep)
##        print '------------------------------ \n'
##        print TimeStep
##        print TimeStepList[TrialNum - 2]
##        SimulationRoom.RefreshRoom()
##
##    avg = sum(TimeStepList)/len(TimeStepList)
##    print 'The average is: %d' %avg
        

#Now add multiple robots (iteration 3 of 3)
    SimulationRoom = RectangularRoom(width,height)
    Coverage = CheckCoverage(SimulationRoom)

    #Create a list of robots based on the functions input (num_robots)
    ListOfRobots = []
    for X in range(num_robots):
        ListOfRobots.append(robot_type(SimulationRoom, speed))

    #Create two placeholder variables
    TrialNum = 1
    TimeStepList = []
    
    while TrialNum <= num_trials:

        #ANIMATION
        #anim = ps6_visualize.RobotVisualization(num_robots, width, height)

        Coverage = CheckCoverage(SimulationRoom)
        TimeStep = 0
        while Coverage < min_coverage:
            for IndividualRobot in ListOfRobots:
                
                IndividualRobot.updatePositionAndClean()
                Coverage = CheckCoverage(SimulationRoom)
            TimeStep +=1

            #ANIMATION
            #anim.update(SimulationRoom, ListOfRobots)
            
        TrialNum += 1
        TimeStepList.append(TimeStep)
##        print '------------------------------ \n'
##        print TimeStep
##        print TimeStepList[TrialNum - 2]
        SimulationRoom.RefreshRoom()
#--------------------------------------------
#--------------------------------------------------------------------------------------------
#               NEED TO FIX SO THE ANIMATION DOESN'T FREEZE WHEN IT'S FINIISHED
#--------------------------------------------------------------------------------------------
#-------------------------------------------
        #ANIMATION
        #anim.done()
        
    avg = sum(TimeStepList)/len(TimeStepList)
    #print 'The average is: %d' %avg
    return avg
          


#TEST 3 ---------
##print '\n Test 3 \n'
##print runSimulation(3,1,20,20,0.8,3,StandardRobot)

#print 'it took %d to do it' %runSimulation(1,1,10,10,0.5,1,StandardRobot)
    


### === Problem 4
###
# 1) How long does it take to clean 80% of a 20×20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20×20, 25×16, 40×10, 50×8, 80×5, and 100×4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """ 

    #Constant for number of robots to test
    NumberOfRobotsToTest = 10

    TimePerRobot = []
    for numberOfRobots in range(1,NumberOfRobotsToTest+1):
        TimePerRobot.append(runSimulation(numberOfRobots, 1, 20, 20, 0.2, 20,
                  StandardRobot))

    TimePerRobotXAxis = []
    for numberOfRobots in range(1,NumberOfRobotsToTest+1):
        TimePerRobotXAxis.append(numberOfRobots)
    
    


    plt.plot(TimePerRobotXAxis,TimePerRobot)
    plt.ylabel('Cleaning Time')
    plt.xlabel('Number of Robots')
    plt.title('Number of Robots vs. Cleaning Time')
    plt.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    
    plt.plot(TimePerRobotXAxis,TimePerRobot)
    plt.ylabel('Cleaning Time')
    plt.xlabel('Number of Robots')
    plt.title('Number of Robots vs. Cleaning Time')
    plt.show()

#showPlot1()


# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        #Clean tile at original position
        self.RobotRoom.cleanTileAtPosition(self.RobotPosition)

        #Chose a new direction
        self.RobotDirection = random.randint(1,360)
        
        #Move Robot to new position using the method from the Position class
        RobotPositionTrial = self.RobotPosition.getNewPosition(self.RobotDirection,self.RobotSpeed)

        if self.RobotRoom.isPositionInRoom(RobotPositionTrial) is True:
            self.RobotPosition = RobotPositionTrial
        else:
            self.RobotDirection = random.randint(1,360)  

# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """

    #Constant for number of robots to test
    NumberOfRobotsToTest = 10

    TimePerRobotStandard = []
    for numberOfRobots in range(1,NumberOfRobotsToTest+1):
        TimePerRobotStandard.append(runSimulation(numberOfRobots, 1, 20, 20, 0.2, 20,
                  StandardRobot))

    TimePerRobotRandom = []
    for numberOfRobots in range(1,NumberOfRobotsToTest+1):
        TimePerRobotRandom.append(runSimulation(numberOfRobots, 1, 20, 20, 0.2, 20,
                  RandomWalkRobot))

    TimePerRobotXAxis = []
    for numberOfRobots in range(1,NumberOfRobotsToTest+1):
        TimePerRobotXAxis.append(numberOfRobots)
    
    plt.plot(TimePerRobotXAxis,TimePerRobotStandard, 'bs', TimePerRobotXAxis,TimePerRobotRandom, 'g^')
    plt.ylabel('Cleaning Time')
    plt.xlabel('Number of Robots')
    plt.title('Number of Robots vs. Cleaning Time')
    plt.show()
    
