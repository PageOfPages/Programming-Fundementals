# CS 111 Problem Set 6
# Simulating robots
#
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import matplotlib.pyplot as plt

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

        self.width = width
        self.height = height
        self.tiles = []

        #raise NotImplementedError
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.tiles.append(pos)


        #raise NotImplementedError

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        for i in self.tiles:
            if i == Position(m,n):
                return True
        return False
        
        #raise NotImplementedError
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

        #raise NotImplementedError

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.tiles)
        
        #raise NotImplementedError

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        w = random.random() * self.width
        h = random.random() * self.height
        return Position(w,h)

        #raise NotImplementedError

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if (pos.getX() <= self.width) and (pos.getY() <= self.height):
            return True
        return False
        
        #raise NotImplementedError


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
        self.room = room
        self.speed = speed
        self.position = room.getRandomPosition()
        self.direction = random.randint(0, 360)
        #raise NotImplementedError

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
        #raise NotImplementedError
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction
        #raise NotImplementedError

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position
        #raise NotImplementedError

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction
        #raise NotImplementedError

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError


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
        if self.room.isPositionInRoom(self.position.getNewPosition(self.direction, self.speed)):
            updated_pos = self.position.getNewPosition(self.direction, self.speed)
        else:
            direction = self.getRobotDirection()
            updated_pos = self.position.getNewPosition(direction, self.speed)

        self.room.cleanTileAtPosition(updated_pos)
        self.setRobotPosition(updated_pos)

        
        #raise NotImplementedError

# === Problem 3

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
    anim = ps6_visualize.RobotVisualization(num_robots, width, height)

    room = RectangularRoom(width, height)
    robots = [robot_type(room, speed)]*num_robots
    c = 0
    clicks = []
    total_clicks = 0
    for i in range(num_trials):
        while (room.getNumCleanedTiles()/room.getNumTiles()) < min_coverage:
            for robot in robots:
                robot.updatePositionAndClean()
            c += 1
            anim.update(room, robots)
        clicks.append(c)
        c = 0
    for c in clicks:
        total_clicks += c

    anim.done()
    return total_clicks/num_trials

    
    #raise NotImplementedError

#print(runSimulation(10,1.0,15,20,0.8,30, StandardRobot))

# === Problem 4
#
# 1) How long does it take to clean 80% of a 20◊20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20◊20, 25◊16, 40◊10, 50◊8, 80◊5, and 100◊4?

def showPlot1():
    plt.suptitle('Time to clean 80% of a 20◊20 room, for ranging number of robots')
    plt.ylabel('Cleaning Time')
    plt.xlabel('Number of Robots')

    robotsX = [1,2,3,4,5,6,7,8,9,10]
    cleaning_timeY = []
    for i in robotsX:
        cleaning_timeY.append(runSimulation(i, 1.0, 20, 20, 0.8, 1000, StandardRobot))

    plt.show(plt.show(plt.plot(robotsX, cleaning_timeY)))
    #plt.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    plt.suptitle('Time for two robots to clean 80% of a 400 room of varying ratios of Width and Height')
    plt.ylabel('Cleaning Time')
    plt.xlabel('Ration of Width to Height')

    dimentions = [(20,20), (25,16), (40,10), (50,8), (80,5), (100,4)]
    ratios = []
    cleaning_timeY = []


    for a, b in dimentions:
        ratios.append(a/b)
        cleaning_timeY.append(runSimulation(2, 1.0, a, b, 0.8, 1000, StandardRobot))

    plt.show(plt.plot(ratios, cleaning_timeY))
    #raise NotImplementedError



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
        nextPos = self.getRobotPosition().getNewPosition(random.randint(0.359), self.speed)
        if self.room.isPositionInRoom(nextPos):
            self.setRobotPosition(nextPos)
            self.setRobotDirection(random.randint(0,359))
            self.room.cleanTileAtPostion(nextPos)
        else:
            self.setRobotDirection(random.randint(0,359))

    # raise NotImplementedError


# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    plt.suptitle('Time to clean 80% of a 20*20 room using two robot strategies')
    plt.ylabel('Cleaning Time')
    plt.xlabel('Ration of Width to Height')

    plt.xlabel('Number of Robots')

    robotsX = [1,2,3,4,5,6,7,8,9,10]
    cleaning_timeY1 = []
    cleaning_timeY2 = []
    for i in robotsX:
        cleaning_timeY1.append(runSimulation(i, 1.0, 20, 20, 0.8, 1000, StandardRobot))
        print('Y1 = ', runSimulation(i, 1.0, 20, 20, 0.8, 1000, StandardRobot))
        cleaning_timeY2.append(runSimulation(i, 1.0, 20, 20, 0.8, 1000, RandomWalkRobot))
        print('Y2 = ', runSimulation(i, 1.0, 20, 20, 0.8, 1000, RandomWalkRobot))

    plt.plot(robotsX, cleaning_timeY1, label='Cleaning Time 1')
    plt.plot(robotsX, cleaning_timeY2, label='Cleaning Time 2')
    plt.show()

showPlot1()


    #raise NotImplementedError

