import math
import random
import matplotlib.pyplot as plt

# global variables
#each location will be given a specific x and y coordinate and extend in a 0.05 radius to form a circle
partyLocation_x = 0
partyLocation_y = 0

gymLocation_x = 0
gymLocation_y = 0

libraryLocation_x = 0
libraryLocation_y = 0

agent_list = []
academic_data = []
party_data = []
sports_data = []


interactionsDict = {}
totalInteractions = 0

class Agent:
    # Initialize the agent properties 
    x_coordinate = 0 # The agent's x coordinate
    y_coordinate = 0 # The agent's y coordinate 
    type = ""
    
    # meters for visiting locations
    studyingMeter = 0
    partyMeter = 0
    excerciseMeter = 0

    #thresholds their meters must be at depending on type
    studyThreshold = 0
    partyThreshold = 0
    excerciseThreshold = 0

    # use the __init__() function to set the properties when you make a new agent
    def __init__(self, x_coordinate, y_coordinate, type) :
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.type = type
        self.studyingMeter = random.randint(80, 100)
        self.partyMeter = random.randint(80, 100)
        self.exerciseMeter = random.randint(80, 100)

        if type == "academic":
            self.studyThreshold = 30
            self.partyThreshold = 50
            self.excerciseThreshold = 50
        if type == "sports":
            self.studyThreshold = 50
            self.partyThreshold =  30
            self.excerciseThreshold = 30
        if type == "party":
            self.studyThreshold = 30
            self.partyThreshold = 50
            self.excerciseThreshold = 30


     # This function uses the distance formula to calculate the distance between two coordinates  
    def distanceTo(self, other_x, other_y):
        dx = other_x - self.x_coordinate
        dy = other_y - self.y_coordinate
        return math.sqrt(dx**2 + dy**2)
        
def initialize() :
    # Each time this for loop runs, an gentsaisrandomly created 
    for type in ["academic", "sports", "party"] :
        for i in range(100) : # There are 100 of each type of agent             
            x_coord = random.random()
            y_coord = random.random()
            agent_type = type
            new_agent = Agent(x_coord, y_coord, agent_type)
            
            agent_list.append(new_agent)
            if agent_type == "academic"  # add the new agent to the list of agents :
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
    neighbors = []
    neighborsCount = 0

    for neigh_agent in agent_list:
        # get neighbors x and y coordinates
        neigh_x_coordinate = neigh_agent.x_coordinate
        neigh_y_coordinate = neigh_agent.y_coordinate

        # if distance of current agent to potential neighbor is less than 0.04 add to our list
        if agent.distanceTo(neigh_x_coordinate, neigh_y_coordinate) <= 0.02 and agent.type != neigh_agent.type and (interactionsDict(agent) != neigh_agent or interactionsDict(neigh_agent) != agent):
            neighbors.append(neigh_agent)
            neighborsCount+= 1

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
        totalInteractions += 1



def move(current_agent):
    # get current state of an agents meters
    studyingMeter = current_agent.studyingMeter
    partyMeter = current_agent.partyMeter
    excerciseMeter = current_agent.excerciseMeter

    # initialize meters as a dict
    meters = {
        'library': studyingMeter,
        'party' : partyMeter,
        'gym' : excerciseMeter
    }

    # find the meter that is the lowest
    # returns the location that the agent needs to move to 
    moveTo = min(meters, key=meters.get())

    #depending on which meter is the smallest the agent will move to the appropriate location
    belowMeter = False

    if moveTo == "library":
        target_x, target_y = libraryLocation_x, libraryLocation_y
        if current_agent.studyingMeter < current_agent.studyingThreshold:
            belowMeter = True
    elif moveTo == "party":
        target_x, target_y = partyLocation_x, partyLocation_y
        if current_agent.partyMeter < current_agent.partyThreshold:
            belowMeter = True
    elif moveTo == "gym":
        target_x, target_y = gymLocation_x, gymLocation_y
        if current_agent.excerciseMeter < current_agent.excerciseThreshold:
            belowMeter = True

    if belowMeter == True:
        stepSize = 0.06
    else:
        stepSize = 0.03

    #calculate the vector length from agents current location to target + normalize
    vector_x = target_x - current_agent.x_coordinate
    vector_y = target_y - current_agent.y_coordinate
    
    totalDistance = math.sqrt(vector_x**2 + vector_y**2)
    toMove_x = vector_x / totalDistance
    toMove_y = vector_y / totalDistance

    current_agent.x_coordinate += toMove_x * stepSize
    current_agent.y_coordinate += toMove_y * stepSize

    keepInBounds(current_agent)



def rules(current_agent) :
    #random move
    #count number of opposite neighbors
    #rules for each kind
    
    move(current_agent)

    countNeighbors(current_agent)

    
    for agent in agent_list :
        for other_agent in agent_list :
            if agent.distanceTo(other_agent.x_coordinate, other_agent.y_coordinate) <= .01 and agent != other_agent:
                agent.x_coordinate = random.uniform(-.03, .03)
                agent.y_coordinate = random.uniform(-.03, .03)
                other_agent.x_coordinate = random.uniform(-.03, .03)
                other_agent.y_coordinate = random.uniform(-.03, .03) 

    
    
    num_academic = 0
    num_sports = 0
    num_party = 0

    for current_agent in agent_list :
        if current_agent.type == "academic" :
            num_academic += 1
        elif current_agent.type == "sports" :
            num_sports += 1
        else :
            num_party += 1
    
    academic_data.append(num_academic)
    sports_data.append(num_sports)
    party_data.append(num_party)

    return

def update():
    
    if len(agent_list > 0) :
        random.shuffle(agent_list)
        for current_agent in agent_list :
            rules(current_agent)
    
    return

def observe():

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
        ax[0].plot(x, y, 'ro')
        
    # Make a list of athletes
    sports = [ag for ag in agent_list if ag.type == "sports"]
    if len(sports) > 0:
        # Pull the coordinates of all of the athletes and make x and y lists
        x = [ag.x_coordinate for ag in sports]
        y = [ag.y_coordinate for ag in sports]
        # We use these x and y lists to plot our athletes as green dots
        ax[0].plot(x, y, 'go')

    ax[0].axis([0, 1, 0, 1]) # Sets the bounds of the x and y axes

    # This makes our second subplot, located in axis 1 (graph of populations over time, bottom)
    # This plot is much easier. We just plot(typ).
    # Automatically, plot() will put the list index (time) on the x axis and the list value (population) of the y.
    # The label helps us make a color key/legend.
    ax[1].plot(academic_data, label = 'academic')
    ax[1].plot(sports_data, label = 'sports')
    ax[1].plot(party_data, label = 'party')
    ax[1].legend()

    # Makes the plot bigger
    fig.set_figwidth(6)
    fig.set_figheight(8)
    
    # Place the current timestep in the title
    fig.suptitle("Current Timestep: " + str(current_timestep + 1))

    return

def main():
    return

if __name__ == "__main__":
    main()

#used code from lab 4


    








        