import math
import random

class Agent:
    x_coordinate = 0
    y_coordinate = 0
    type = ""
    
    #percent chance for agent to be in specific locations
    chanceOfParty = 0
    chanceOfGym= 0
    chanceOfClass = 0
    chanceOfGame = 0

    def __init__(self, x_coordinate, y_coordinate, type):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        type = self.type

        #depending on certain agent types set percentages for how likely they are to go to an event
        if type == "academic":
            self.chanceOfParty = .05
            self.chanceOfGym= .20
            self.chanceOfClass = .6
            self.chanceOfGame = .20

        elif type == "sports":
            self.chanceOfParty = .45
            self.chanceOfGym= .55
            self.chanceOfClass = .6
            self.chanceOfGame = .8

        elif type == "party":
            self.chanceOfParty = .8
            self.chanceOfGym= .15
            self.chanceOfClass = .15
            self.chanceOfGame = .6

        
    
    def distanceTo(self, other_x, other_y):
        dx = other_x - self.x_coordinate
        dy = other_y - self.y_coordinate
        return math.sqrt(dx**2 + dy**2)
        
def initialize() :
    agent_list = []
    academic_data = []
    party_data = []
    sports_data = []
    
    for type in ["academic", "sports", "party"] :
        for i in range(100) :
            x_coord = random.random()
            y_coord = random.random()
            agent_type = type
            new_agent = Agent(x_coord, y_coord, agent_type)
            agent_list.append(new_agent)
            if agent_type == "academic" :
                academic_data.append(new_agent)
            if agent_type == "party" :
                party_data.append(new_agent)
            if agent_type == "sports" :
                sports_data.append(new_agent)


def keepInBounds(agent) :
    if agent.x_coordinate > 1 :
        agent.x_coordinate = 1
    elif agent.x_coordinate < 0 :
        agent.x_coordinate = 0
    if agent.y_coordinate > 1 :
        agent.y_coordinate = 1
    elif agent.y_coordinate < 0 :
        agent.y_coordinate = 0

def countNeighbors(agent, agent_list):
    neighbors = []

    for neigh_agent in agent_list:
        # get neighbors x and y coordinates
        neigh_x_coordinate = neigh_agent.x_coordinate
        neigh_y_coordinate = neigh_agent.y_coordinate

        # if distance of current agent to potential neighbor is less than 0.04 add to our list
        if agent.distanceTo(neigh_x_coordinate, neigh_y_coordinate) <= 0.04:
            neighbors.append(neigh_agent)

    return neighbors



def rules() :
    return

def update():
    return

def observe():
    return

def main():
    return

if __name__ == "__main__":
    main()

#used code from lab 4


    








        