import math
import random
import matplotlib.pyplot as plt
import numpy as np
from IPython import display
import time

# global variables
#each location will be given a specific x and y coordinate and extend in a 0.1 radius to form a circle
global partyLocation_x, partyLocation_y, gymLocation_x, gymLocation_y, libraryLocation_x, libraryLocation_y, agent_list, academic_data, party_data, sports_data, interactionsDict, totalInteractions, current_timestep


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
        # start agents meters from any values between 50 -70
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

    global partyLocation_x, partyLocation_y, libraryLocation_x, libraryLocation_y, gymLocation_x, gymLocation_y, agent_list, academic_data, party_data, sports_data

    # initialize the location of the party, library, and gym


    # Each time this for loop runs, an agent is randomly created 
    for type in ["academic", "sports", "party"] :
        for i in range(50) : # There are 100 of each type of agent        
                 
            overlapped = True
            while overlapped:
                x_coord = random.uniform(0,1)
                y_coord = random.uniform(0,1)
                if np.abs(x_coord - libraryLocation_x) <= .1 and np.abs(y_coord - libraryLocation_y) <= .1 :
                    overlapped = True
                elif np.abs(x_coord - partyLocation_x) <= .1 and np.abs(y_coord - partyLocation_y) <= .1 :
                    overlapped = True
                elif np.abs(x_coord - gymLocation_x) <= .1 and np.abs(y_coord - gymLocation_y) <= .1 :
                    overlapped = True
                else :
                    overlapped = False

            agent_type = type
            new_agent = Agent(x_coord, y_coord, agent_type)
            
            agent_list.append(new_agent)
            if agent_type == "academic":  # add the new agent to the list of agents 
                academic_data.append(new_agent)
            if agent_type == "party" :
                party_data.append(new_agent)
            if agent_type == "sports" :
                sports_data.append(new_agent)


#makes sure that the agent stays within the array# ensures
def keepInBounds(agent):
    if agent.x_coordinate > 1 :
        agent.x_coordinate = 1
    elif agent.x_coordinate < 0 :
        agent.x_coordinate = 0
    if agent.y_coordinate > 1 :
        agent.y_coordinate = 1
    elif agent.y_coordinate < 0 :
        agent.y_coordinate = 0

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
    if np.abs(current_agent.x_coordinate - libraryLocation_x) < .1 and np.abs(current_agent.y_coordinate - libraryLocation_y) < .1 :
        if studyingMeter < 80 :
            return
    elif np.abs(current_agent.x_coordinate - partyLocation_x) < .1 and np.abs(current_agent.y_coordinate - partyLocation_y) < .1 :
        if partyMeter < 80 :
            return
    elif np.abs(current_agent.x_coordinate - gymLocation_x) < .1 and np.abs(current_agent.y_coordinate - gymLocation_y) < .1 :
        if exerciseMeter < 80 :
            return

    # find the meter that is the lowest
    # returns the location that the agent needs to move to 
    moveTo = min(meters, key=meters.get)

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

    # if below meter is true agents' step size will be 0.06
    if belowMeter == True:
        stepSize = 0.06
    else: # otherwise it will be 0.03
        stepSize = 0.03

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

    # if two agents are within 0.01 of eachother move them 0.03 away so they do not end up right on top
    for agent in agent_list :
        for other_agent in agent_list :
            if agent.distanceTo(other_agent.x_coordinate, other_agent.y_coordinate) <= .01 and agent != other_agent:
                agent.x_coordinate += random.uniform(-.03, .03)
                agent.y_coordinate += random.uniform(-.03, .03)
                other_agent.x_coordinate += random.uniform(-.03, .03)
                other_agent.y_coordinate += random.uniform(-.03, .03) 


    return numInteractions



def updateMeters(agent):
    # if an agent is within the party
    if agent.x_coordinate > (partyLocation_x - 0.1) and agent.x_coordinate < (partyLocation_x + 0.1) and agent.y_coordinate > (partyLocation_y - 0.1) and agent.y_coordinate < (partyLocation_y + 0.1):
        if agent.type == "academic":
            agent.partyMeter += 10 # increase the party meter by 10
            agent.studyingMeter -= 5 # decrease the studying meter by 5
            agent.exerciseMeter -= 5 # decrease the excercise meter by 5
        elif agent.type == "sports":
            agent.partyMeter += 10 # increase the party meter by 10
            agent.studyingMeter -= 5 # decrease the studying meter by 5
            agent.exerciseMeter -= 5 # decrease the excercise meter by 5
        elif agent.type == "party":
            agent.partyMeter += 5 # increase the party meter by 10
            agent.studyingMeter -= 5 # decrease the studying meter by 5
            agent.exerciseMeter -= 5 # decrease the excercise meter by 5

    # if an agent is within the library
    elif agent.x_coordinate > (libraryLocation_x - 0.1) and agent.x_coordinate < (libraryLocation_x + 0.1) and agent.y_coordinate > (libraryLocation_y- 0.1) and agent.y_coordinate < (libraryLocation_x + 0.1):
        if agent.type == "academic":
            agent.partyMeter -= 5 # increase the party meter by 10
            agent.studyingMeter += 5 # decrease the studying meter by 5
            agent.exerciseMeter -= 5 # decrease the excercise meter by 5
        elif agent.type == "sports":
            agent.partyMeter -= 5 # increase the party meter by 10
            agent.studyingMeter += 10 # decrease the studying meter by 5
            agent.exerciseMeter -= 5 # decrease the excercise meter by 5
        elif agent.type == "party":
            agent.studyingMeter -= 5 # increase the study meter by 10
            agent.partyMeter += 10 # decrease the party meter by 5
            agent.exerciseMeter -= 5 # decrease the excercise meter by 5
        
    # if an agent is within the gym
    elif agent.x_coordinate > (gymLocation_x- 0.1) and agent.x_coordinate < (gymLocation_x + 0.1) and agent.y_coordinate > (gymLocation_y - 0.1) and agent.y_coordinate < (gymLocation_y + 0.1):
         if agent.type == "academic":
            agent.partyMeter -= 5 # increase the party meter by 10
            agent.studyingMeter -= 5 # decrease the studying meter by 5
            agent.exerciseMeter += 10 # decrease the excercise meter by 5
         elif agent.type == "sports":
            agent.partyMeter -= 5 # increase the party meter by 10
            agent.studyingMeter -= 5 # decrease the studying meter by 5
            agent.exerciseMeter += 5 # decrease the excercise meter by 5
         elif agent.type == "party":
            agent.studyingMeter -= 5 # increase the study meter by 10
            agent.partyMeter -= 5 # decrease the party meter by 5
            agent.exerciseMeter += 10 # decrease the excercise meter by 5

    # if an agent is not within any location
    else:
        if agent.type == "academic":
            agent.studyingMeter -= 8 # decrease study meter by 5
            agent.partyMeter -= 5 # decrease party meter by 5
            agent.exerciseMeter -= 5 # decrease excercise meter by 5
        elif agent.type == "sports":
            agent.studyingMeter -= 5 # decrease study meter by 5
            agent.partyMeter -= 5 # decrease party meter by 5
            agent.exerciseMeter -= 8 # decrease excercise meter by 5
        elif agent.type == "party":
            agent.studyingMeter -= 5 # decrease study meter by 5
            agent.partyMeter -= 8 # decrease party meter by 5
            agent.exerciseMeter -= 5 # decrease excercise meter by 5

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
    # This plot is much easier. We just plot(typ).
    # Automatically, plot() will put the list index (time) on the x axis and the list value (population) of the y.
    # The label helps us make a color key/legend.
    
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
    global partyLocation_x, partyLocation_y, gymLocation_x, gymLocation_y, libraryLocation_x, libraryLocation_y, agent_list, academic_data, party_data, sports_data, interactionsDict, totalInteractions, current_timestep
    
    #REMEMBER initialize locations differently on different runs


    partyLocation_x = 0.8
    partyLocation_y = 0.8

    gymLocation_x = .4
    gymLocation_y = .4

    libraryLocation_x = .1
    libraryLocation_y = .6

    agent_list = []
    academic_data = []
    party_data = []
    sports_data = []


    interactionsDict = {}
    totalInteractions = []

    current_timestep = 0

    # create our needed agents 
    initialize()
    
    # run our model for XXXX timesteps
    for timestep in range(50):
        current_timestep = timestep # set current_timestep to the timestep we are on
        interactionsDict = {} # clear our interactions
        numInteractions = 0 # counter to keep track of interactions in a given run
        
        copy_agent_list = agent_list # copy our list of agents so that we can shuffle the order they move in
        random.shuffle(copy_agent_list)

        for agent in copy_agent_list: # for each agent in our agent list
            numInteractions += rules(agent) # update their movement and keep track of how many interactions they have
            updateMeters(agent) # update an agents meters based on if they are in a location or not
        
        totalInteractions.append(numInteractions) # append the number of interactions in this timestep to the list containing total interactions

        plt.close()
        observe() # plot our data
        display.clear_output(wait=True)
        display.display(plt.gcf())
    plt.close()



if __name__ == "__main__":
    main()

#used code from lab 4


    








        