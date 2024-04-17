import math
import random
import matplotlib.pyplot as plt
import numpy as np
from IPython import display
import time

# global variables
#each location will be given a specific x and y coordinate and extend in a 0.1 radius to form a circle
global partyLocation_x, partyLocation_y, gymLocation_x, gymLocation_y, libraryLocation_x, libraryLocation_y, agent_list,  interactionsDict, totalInteractions, current_timestep


class Agent:
    # Initialize the agent properties 
    x_coordinate = 0 # The agent's x coordinate
    y_coordinate = 0 # The agent's y coordinate 
    type = ""
    
    # meters for visiting locations
    studyingMeter = 0
    partyMeter = 0
    exerciseMeter = 0

    #thresholds their meters must be at depending on type
    studyThreshold = 0
    partyThreshold = 0
    exerciseThreshold = 0

    # use the __init__() function to set the properties when you make a new agent
    def __init__(self, x_coordinate, y_coordinate, type) :
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.type = type
        # start agents meters from any values between 50 and 70
        self.studyingMeter = random.randint(50, 70)
        self.partyMeter = random.randint(50, 70)
        self.exerciseMeter = random.randint(50, 70)

        # set the thresholds for their meters depending on what type of agent they are
        if type == "academic":
            self.studyThreshold = 70
            self.partyThreshold = 30
            self.exerciseThreshold = 30
        if type == "sports":
            self.studyThreshold = 30
            self.partyThreshold =  30
            self.exerciseThreshold = 70
        if type == "party":
            self.studyThreshold = 30
            self.partyThreshold = 70
            self.exerciseThreshold = 30


     # This function uses the distance formula to calculate the distance between two coordinates  
    def distanceTo(self, other_x, other_y):
        dx = other_x - self.x_coordinate
        dy = other_y - self.y_coordinate
        return math.sqrt(dx**2 + dy**2)
        
def initialize() :

    global partyLocation_x, partyLocation_y, libraryLocation_x, libraryLocation_y, gymLocation_x, gymLocation_y, agent_list

    # Each time this for loop runs, an agent is randomly created 
    for type in ["academic", "sports", "party"] :
        for i in range(50) : # There are 50 of each type of agent  
                  
            #to prevent agents from being initialized inside a location, we regenrate their coordinates until they are not  
            overlapped = True # boolean to keep track if an agent is in a location
            while overlapped:
                x_coord = random.uniform(0,1) # resets agents x coord
                y_coord = random.uniform(0,1) # resets agents y coord
                if np.abs(x_coord - libraryLocation_x) <= .1 and np.abs(y_coord - libraryLocation_y) <= .1 : # checks if agent is within library
                    overlapped = True # if so, overlapped becomes true
                elif np.abs(x_coord - partyLocation_x) <= .1 and np.abs(y_coord - partyLocation_y) <= .1 :# checks if agent is within party
                    overlapped = True
                elif np.abs(x_coord - gymLocation_x) <= .1 and np.abs(y_coord - gymLocation_y) <= .1 :# checks if agent is within gym
                    overlapped = True
                else :
                    overlapped = False

            agent_type = type 
            new_agent = Agent(x_coord, y_coord, agent_type) # creates our agent
            
            agent_list.append(new_agent) # appends new agent to our list
           


#makes sure that the agent stays within the array
def keepInBounds(agent):
    if agent.x_coordinate > 1 : # if agents x coordinate is above 1
        agent.x_coordinate = 1 # x = 1
    elif agent.x_coordinate < 0 : # if agents x coordinate is below 0
        agent.x_coordinate = 0 # x = 0
    if agent.y_coordinate > 1 : # if agents y coordinate is above 1
        agent.y_coordinate = 1 # y = 1
    elif agent.y_coordinate < 0 :# if agents y coordinate is below 0
        agent.y_coordinate = 0 # y=0

def countNeighbors(agent):
    global totalInteractions, current_timestep
    numInteractions = 0
    
    neighbors = []
    neighborsCount = 0

    for neigh_agent in agent_list:
        # get neighbors x and y coordinates
        neigh_x_coordinate = neigh_agent.x_coordinate
        neigh_y_coordinate = neigh_agent.y_coordinate

        # if distance of current agent to potential neighbor is less than 0.05 add to our list
        if agent.distanceTo(neigh_x_coordinate, neigh_y_coordinate) <= 0.03 and agent.type != neigh_agent.type :
            neighborsCount+= 1
            neighbors.append(neigh_agent)

    # to make sure we do not double count interactions between agent and neighbor
    # run through all the agents neighbors
    for neighbor in neighbors:
        # if the neighbor has already been calculated as having an interaction 
        if neighbor in interactionsDict:
            neighbors_interactions = interactionsDict[neighbor]
            # check to make sure that interaction is not with our current agent
            # if it is then we skip this neighbor
            if agent in neighbors_interactions:
                continue

        # add our current agent to our interactions dict
        if agent not in interactionsDict:
            interactionsDict[agent] = [neighbor]
        else:
            interactionsDict[agent].append(neighbor)

        # increase our total interactions by 1
        numInteractions += 1
    
    return numInteractions



def move(current_agent):
    global libraryLocation_x, libraryLocation_y, gymLocation_x, gymLocation_y, partyLocation_x, partyLocation_y
    # get current state of an agents meters
    studyingMeter = current_agent.studyingMeter
    partyMeter = current_agent.partyMeter
    exerciseMeter = current_agent.exerciseMeter

    # initialize meters as a dict
    meters = {
        'library': studyingMeter,
        'party' : partyMeter,
        'gym' : exerciseMeter
    }

    #if in a location, and meter below 80%, stay there
    if current_agent.distanceTo(libraryLocation_x, libraryLocation_y) < .1 :
        if studyingMeter < 80 :
            return
    elif current_agent.distanceTo(partyLocation_x, partyLocation_y)< .1 :
        if partyMeter < 80 :
            return
    elif current_agent.distanceTo(gymLocation_x, gymLocation_y) < .1 :
        if exerciseMeter < 80 :
            return
        

    

    # find the meter that is the lowest
    # returns the location that the agent needs to move to 
    moveTo = min(meters, key=meters.get)

    if current_agent.type == "academic":
        if studyingMeter < current_agent.studyThreshold:
            moveTo = 'library'
    elif current_agent.type == "party":
        if partyMeter < current_agent.partyThreshold:
            moveTo = 'party'
    elif current_agent.type == "sports":
        if exerciseMeter < current_agent.exerciseThreshold:
            moveTo = 'gym'

    #depending on which meter is the smallest the agent will move to the appropriate location
    belowMeter = False

    # set the target_x, target_y to be the location corresponding to their lowest meter
    if moveTo == "library":
        target_x, target_y = libraryLocation_x, libraryLocation_y
        if current_agent.studyingMeter < current_agent.studyThreshold: # if their lowest meter is below their required threshold set belowMeter to be true
            belowMeter = True
    elif moveTo == "party":
        target_x, target_y = partyLocation_x, partyLocation_y
        if current_agent.partyMeter < current_agent.partyThreshold:
            belowMeter = True
    elif moveTo == "gym":
        target_x, target_y = gymLocation_x, gymLocation_y
        if current_agent.exerciseMeter < current_agent.exerciseThreshold:
            belowMeter = True

    # if below meter is true agents' step size will be 0.12
    if belowMeter == True:
        stepSize = 0.12
    else: # otherwise it will be 0.06
        stepSize = 0.06

    #calculate the vector length from agents current location to target + normalize
    vector_x = target_x - current_agent.x_coordinate
    vector_y = target_y - current_agent.y_coordinate
    
    totalDistance = math.sqrt(vector_x**2 + vector_y**2)
    toMove_x = vector_x / totalDistance
    toMove_y = vector_y / totalDistance

    # move the agent in the specified direction
    current_agent.x_coordinate += toMove_x * stepSize
    current_agent.y_coordinate += toMove_y * stepSize

    # makes sure agent stays in bound
    keepInBounds(current_agent)



def rules(current_agent) :
    #random move
    #count number of opposite neighbors
    #rules for each kind
    
    # moves agent
    move(current_agent)

    # count the number of interactions an agent has with agents of dissimilar types (i.e. agents that are in a 0.05 radius)
    numInteractions = countNeighbors(current_agent)

    # if two agents are within 0.01 of each other, randomly move them so they do not end up right on top of each other
    for agent in agent_list :
        for other_agent in agent_list :
            if agent.distanceTo(other_agent.x_coordinate, other_agent.y_coordinate) <= .01 and agent != other_agent: # if agents are within a 0.1 radius of each other
                agent.x_coordinate += random.uniform(-.03, .03) # move their x and y locations 0.03 away from eachother
                agent.y_coordinate += random.uniform(-.03, .03)
                other_agent.x_coordinate += random.uniform(-.03, .03)
                other_agent.y_coordinate += random.uniform(-.03, .03) 


    return numInteractions



def updateMeters(agent):
    global libraryLocation_x, libraryLocation_y, gymLocation_x, gymLocation_y, partyLocation_x, partyLocation_y
    # if an agent is within the party
    if agent.distanceTo(partyLocation_x, partyLocation_y) < 0.1:
        if agent.type == "academic":
            agent.partyMeter += 15 # increase the party meter by 15
            agent.studyingMeter -= 5 # decrease the studying meter by 5
            agent.exerciseMeter -= 5 # decrease the excercise meter by 5
        elif agent.type == "sports":
            agent.partyMeter += 15 # increase the party meter by 15
            agent.studyingMeter -= 5 # decrease the studying meter by 5
            agent.exerciseMeter -= 5 # decrease the excercise meter by 5
        elif agent.type == "party":
            agent.partyMeter += 8 # increase the party meter by 8
            agent.studyingMeter -= 5 # decrease the studying meter by 5
            agent.exerciseMeter -= 5 # decrease the excercise meter by 5

    # if an agent is within the library
    elif agent.distanceTo(libraryLocation_x, libraryLocation_y) < .1:
        if agent.type == "academic":
            agent.partyMeter -= 5 # decrease the party meter by 5
            agent.studyingMeter += 8 # increase the studying meter by 8
            agent.exerciseMeter -= 5 # decrease the excercise meter by 5
        elif agent.type == "sports":
            agent.partyMeter -= 5 # decrease the party meter by 5
            agent.studyingMeter += 15 # increase the studying meter by 15
            agent.exerciseMeter -= 5 # decrease the excercise meter by 5
        elif agent.type == "party":
            agent.studyingMeter -= 5 # decrease the study meter by 5
            agent.partyMeter += 15 # increase the party meter by 15
            agent.exerciseMeter -= 5 # decrease the excercise meter by 5
        
    # if an agent is within the gym
    elif agent.distanceTo(gymLocation_x, gymLocation_y) < .1 :
        if agent.type == "academic":
            agent.partyMeter -= 5 # decrease the party meter by 5
            agent.studyingMeter -= 5 # decrease the studying meter by 5
            agent.exerciseMeter += 15 # increase the excercise meter by15
        elif agent.type == "sports":
            agent.partyMeter -= 5 # decrease the party meter by 5
            agent.studyingMeter -= 5 # decrease the studying meter by 5
            agent.exerciseMeter += 8 # increase the excercise meter by 8
        elif agent.type == "party":
            agent.studyingMeter -= 5 # decrease the study meter by 5
            agent.partyMeter -= 5 # decrease the party meter by 5
            agent.exerciseMeter += 15 # increase the excercise meter by 15

    # if an agent is not within any location
    else:
        if agent.type == "academic":
            agent.studyingMeter -= 5 # decrease study meter by 5
            agent.partyMeter -= 3 # decrease party meter by 3
            agent.exerciseMeter -= 3 # decrease excercise meter by 3
        elif agent.type == "sports":
            agent.studyingMeter -= 3 # decrease study meter by 3
            agent.partyMeter -= 3 # decrease party meter by 3
            agent.exerciseMeter -= 5 # decrease excercise meter by 5
        elif agent.type == "party":
            agent.studyingMeter -= 3 # decrease study meter by 3
            agent.partyMeter -= 5 # decrease party meter by 5
            agent.exerciseMeter -= 3 # decrease excercise meter by 3
    
    # used to keep meters of our agents in bounds
    if agent.studyingMeter < 0 : # if an agents meter is below 0
        agent.studyingMeter = 0 # meter is equal to 0
    elif agent.studyingMeter > 100 : # if an agents meter is above 100
        agent.studyingMeter = 100 # meter is equal to 100
    if agent.partyMeter < 0 :
        agent.partyMeter = 0
    elif agent.partyMeter > 100 :
        agent.partyMeter = 100
    if agent.exerciseMeter < 0 :
        agent.exerciseMeter = 0
    elif agent.exerciseMeter > 100 :
        agent.exerciseMeter = 100

    return


def observe():

    global totalInteractions, libraryLocation_x, libraryLocation_y, gymLocation_x, gymLocation_y, partyLocation_x, partyLocation_y

    fig, axes = plt.subplots(nrows = 2, ncols = 1, gridspec_kw={'height_ratios': [3, 1]})
    ax = axes.flatten()

    # This makes our first subplot, located in axis 0 (the world, top)
    # Make a list of academic students
    academic = [ag for ag in agent_list if ag.type == "academic"]
    if len(academic) > 0:
        # Pull the coordinates of all of the academic students and make x and y lists
        x = [ag.x_coordinate for ag in academic]
        y = [ag.y_coordinate for ag in academic]
        # We use these x and y lists to plot our academic students as blue dots
        ax[0].plot(x, y, 'b.')

    # Make a list of party goers
    party = [ag for ag in agent_list if ag.type == "party"]
    if len(party) > 0:
        # Pull the coordinates of all of the party goers and make x and y lists
        x = [ag.x_coordinate for ag in party]
        y = [ag.y_coordinate for ag in party]
        # We use these x and y lists to plot our party goers as red dots
        ax[0].plot(x, y, 'r.')
        
    # Make a list of athletes
    sports = [ag for ag in agent_list if ag.type == "sports"]
    if len(sports) > 0:
        # Pull the coordinates of all of the athletes and make x and y lists
        x = [ag.x_coordinate for ag in sports]
        y = [ag.y_coordinate for ag in sports]
        # We use these x and y lists to plot our athletes as green dots
        ax[0].plot(x, y, 'g.')
    
    library = plt.Circle((libraryLocation_x, libraryLocation_y), .1, color = 'silver', label = 'library')
    gym = plt.Circle((gymLocation_x, gymLocation_y), .1, color = 'linen', label = 'gym')
    partyL = plt.Circle((partyLocation_x, partyLocation_y), .1, color = 'lavender', label = 'party')

    ax[0].add_patch(library)
    ax[0].add_patch(gym)
    ax[0].add_patch(partyL)
    
    ax[0].legend()

    ax[0].axis([0, 1, 0, 1]) # Sets the bounds of the x and y axes

    # This makes our second subplot, located in axis 1 (graph of populations over time, bottom)
    
    ax[1].plot(totalInteractions, label = 'Total Interactions')
    ax[1].legend()

    # set x and y axis labels
    ax[1].set_xlabel('Timestep')
    ax[1].set_ylabel('Number of Interactions')
    

    # Makes the plot bigger
    fig.set_figwidth(6)
    fig.set_figheight(8)
    
    # Place the current timestep in the title
    fig.suptitle("Current Timestep: " + str(current_timestep + 1))

    plt.savefig("figure")

    return

def main():
    f = open("outputFile", 'w')
    global partyLocation_x, partyLocation_y, gymLocation_x, gymLocation_y, libraryLocation_x, libraryLocation_y, agent_list,  interactionsDict, totalInteractions, current_timestep
    
    #List of location coordinates for parameter sweep
    locations = [[.9, .9, .1, .9, .5, .1], [.4, .4, .6, .4, .5, .6], [.5, .9, .5, .5, .5, .1], [.1, .1, .3, .1, .9, .9], [.9, .9, .1, .1, .3, .1]] # 5 different layouts of our three locations
    
    for coords in locations : # runs for each of the layout
        # prints current layout to file
        f.write("Location Coordinates: party: (" + str(coords[0]) + ", " + str(coords[1]) + ") gym: ("  + str(coords[2]) + ", " + str(coords[3]) + ") library: (" + str(coords[4]) + ", " + str(coords[5]) + ') \n')
        totalForLayout= 0 # used to calculate averages
        avgPeakForLayout = 0

        for i in range(3) : # run each layout 3 times
            f.write("Iteration " + str(i) + '\n')

            # sets the locations of party, gym, library to their respective coordinates for this layout
            partyLocation_x = coords[0]
            partyLocation_y = coords[1]

            gymLocation_x = coords[2]
            gymLocation_y = coords[3]

            libraryLocation_x = coords[4]
            libraryLocation_y = coords[5]


            agent_list = [] # giant list of all 150 of our agents

            interactionsDict = {} # keeps track of interactions between agents to make sure we do not double count interactions between the same agents in a single timnestep
            totalInteractions = [] # keeps track of interactions that occur in each timestep
            finalInteractions = 0 # keeps track of total interactions that occur in a run

            current_timestep = 0 # used to keep track of our timestep

            # create our needed agents 
            initialize()
            
            # run our model for 200 timesteps
            for timestep in range(200):
                current_timestep = timestep # set current_timestep to the timestep we are on
                interactionsDict = {} # clear our interactions
                numInteractions = 0 # counter to keep track of interactions in a given run
                
                copy_agent_list = agent_list # copy our list of agents so that we can shuffle the order they move in
                random.shuffle(copy_agent_list)

                for agent in copy_agent_list: # for each agent in our agent list
                    numInteractions += rules(agent) # update their movement and keep track of how many interactions they have
                    updateMeters(agent) # update an agents meters based on if they are in a location or not
                
                totalInteractions.append(numInteractions) # append the number of interactions in this timestep to the list containing total interactions
                finalInteractions += numInteractions # add the interactions for this timestep to our total

                plt.close()
                observe() # plot our data
                display.clear_output(wait=True)
                display.display(plt.gcf())
            plt.close()

            # used for output file to record data
            f.write("Peak interactions: " + str(max(totalInteractions)) + '\n')
            f.write("Total interactions: " + str(finalInteractions) +  '\n') 

            totalForLayout += finalInteractions # add total number of interactions that occured during this round to the total
            avgPeakForLayout += max(totalInteractions) # add the peak number of interactions that occured during this round to total

        totalForLayout /= 3 # takes the average of the total number of interactions in each round for this layout
        avgPeakForLayout /=3 # takes the average of the peak number of interactions in each round for this layout

        # print our data to file
        f.write("For this layout the average total interactions was " + str(totalForLayout) +  '\n')
        f.write("For this layout the average peak number of interactions was " + str(avgPeakForLayout) + '\n')
        f.write( '\n')
        



if __name__ == "__main__":
    main()

#used code from lab 4


#first triangle
##library (.9, .9)
##gym (.1 , .9)
##party (.5, .1)


#second close in middle
##library (.4, .3)
##gym (.6,.3)
##party(.5, .6)

#third line
##libraru (.5, .9)
#gym (.5 ,.5)
##party (.5, .1)

#two close 1 far
## gym( .1, .1)
## party (.3, .1)
##library (.9, .9)


## two close 1 far
## party(.1, .1)
## library (.3, .1)
## gym (.9, .9)

    








        