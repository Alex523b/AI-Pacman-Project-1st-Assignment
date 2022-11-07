# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    frontier.push((problem.getStartState(), None, None)) # node representation: (state, parent state, action to get to state)
    expanded = {} # Expanded set representation: Basically, we use a dictionary with the current state being the key each time, and as a value we have a tuple (parent state, action to get to state)
    #Initially, we have not expanded any node, hence the dictionary is empty
    while not frontier.isEmpty():
        node = frontier.pop()
        if(problem.isGoalState(node[0])):#Check if we have reached the goal state
            #Now, we need to return the path to the goal state
            li = [node[2]]#Store the action that lead to the goal state
            node = expanded.get(node[1])#Additionally, get information for the parent of the goal state
            while(node[0] is not None and node[0] != problem.getStartState()):
                #Store actions until we reach the initial state
                action = node[0]
                li.append(action)
                node = expanded.get(node[1])
            li.reverse()#Reverse the list, as we began storing the path to the goal state from finish to start
            return li
        if(node[0] not in expanded.keys()):
            #Providing we haven't expanded the popped node, add its parent node and action to the dictionary
            parentNode = node[0]
            expanded[parentNode] = (node[2], node[1])
            childrenOfNode = problem.getSuccessors(parentNode)
            for child in childrenOfNode:#For each child, add to the frontier its information regarding the child state, parent state and the action
                childNode = child[0]
                action = child[1]
                frontier.push((childNode, parentNode, action))    
    return []
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    frontier.push((problem.getStartState(), None, None)) # node representation: (state, parent state, action to get to state)
    expanded = {} # Expanded set representation: Basically, we use a dictionary with the current state being the key each time, and as a value we have a tuple (parent state, action to get to state)
    #Initially, we have not expanded any node, hence the dictionary is empty
    while not frontier.isEmpty():
        node = frontier.pop()
        if(problem.isGoalState(node[0])):#Check if we have reached the goal state
            #Now, we need to return the path to the goal state
            li = [node[2]]#Store the action that lead to the goal state
            node = expanded.get(node[1])#Additionally, get information for the parent of the goal state
            while(node[0] is not None and node[0]!= problem.getStartState()):
                #Store actions until we reach the initial state
                action = node[0]
                li.append(action)
                node = expanded.get(node[1])
            li.reverse()#Reverse the list, as we began storing the path to the goal state from finish to start
            return li
        if(node[0] not in expanded.keys()):
            #Providing we haven't expanded the popped node, add its parent node and action to the dictionary
            parentNode = node[0]
            expanded[parentNode] = (node[2], node[1])
            childrenOfNode = problem.getSuccessors(parentNode)
            for child in childrenOfNode:#For each child, add to the frontier its information regarding the child state, parent state and the action
                childNode = child[0]
                action = child[1]
                frontier.push((childNode, parentNode, action))
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    frontier.push((problem.getStartState(), None, None, 0), 0) # node representation: ((current node, path to node, parent node, cost to node), priority)
    expanded = {} # Expanded set representation: Once again, the current state is the dictionary key each time, with the cost to reach the particular state being the extra value
    while not frontier.isEmpty():
        node = frontier.pop()
        if(problem.isGoalState(node[0])):# Check if we have reached the goal state
            #Return the path to the goal state
            li = [node[1]] #
            loopCounter = 0 # The node representation in the frontier is different from the expanded set representation, so we need to be aware of it.
            while(node[0] != problem.getStartState()):
                #Store actions until we reach the initial state
                if(loopCounter == 0):
                    node = expanded.get(node[2])#When popped from the frontier, the information regarding the parent state is the third element
                else:
                    node = expanded.get(node[0])#Howerver, in the expanded set-dictionary this piece of information is stored as the first element
                action = node[1]
                li.append(action)
                loopCounter += 1
            li.reverse()#Reverse the list, as we began storing the path to the goal state from finish to start
            return li
        if(node[0] not in expanded.keys()):
            #If we haven't expanded the popped node/state, add the (parent node, action, cost) as a tuple to the expanded set
            parentNode = node[0]
            expanded[parentNode] = (node[2], node[1], node[3])
            childrenOfNode = problem.getSuccessors(parentNode)
            for child in childrenOfNode:
                childNode = child[0]
                costToChild = child[2] + node[3] # Calculate the cost to reach the child state
                action = child[1]
                frontier.push((childNode, action, parentNode, costToChild), costToChild)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    frontier.push((problem.getStartState(), None, None, 0), 0) # node representation: ((current node, path to node, parent node, cost to node), priority)
    expanded = {} # Expanded set representation: Once again, the current state is the dictionary key each time, with the cost to reach the particular state being the extra value
    while not frontier.isEmpty():
        node = frontier.pop()
        if(problem.isGoalState(node[0])):# Check if we have reached the goal state
            #Return the path to the goal state
            li = [node[1]] #
            loopCounter = 0 # The node representation in the frontier is different from the expanded set representation, so we need to be aware of it.
            while(node[0] != problem.getStartState()):
                #Store actions until we reach the initial state
                if(loopCounter == 0):
                    node = expanded.get(node[2])#When popped from the frontier, the information regarding the parent state is the third element
                else:
                    node = expanded.get(node[0])#Howerver, in the expanded set-dictionary this piece of information is stored as the first element
                action = node[1]
                li.append(action)
                loopCounter += 1
            li.reverse()#Reverse the list, as we began storing the path to the goal state from finish to start
            return li
        if(node[0] not in expanded.keys()):
            #If we haven't expanded the popped node/state, add the (parent node, action, cost) as a tuple to the expanded set
            parentNode = node[0]
            expanded[parentNode] = (node[2], node[1], node[3])
            childrenOfNode = problem.getSuccessors(parentNode)
            for child in childrenOfNode:
                childNode = child[0]
                costToChild = child[2] + node[3] # Calculate the cost to reach the child state
                action = child[1]
                frontier.push((childNode, action, parentNode, costToChild), heuristic(childNode, problem) + costToChild)
    return []
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
