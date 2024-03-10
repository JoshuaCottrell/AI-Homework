from wumpus import ExplorerAgent
from PropKB import KB

import random
import logging

class jcottrel_ExplorerAgent(ExplorerAgent):

    def __init__(self):
        super().__init__()
        self.kb = KB('jcottrelWumpus.kb')
        self.x = 0
        self.y = 0
        self.facing = 0 # Up is 0, right is 1, down is 2, left is 3
        self.exit = False
        self.steps = 0
        self.explored = []
        self.illegal = [(-1, 0), (-1, 1), (-1, 2), (-1, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (0, -1), (1, -1), (2, -1), (3, -1)]

    def moveForward(self):
        if self.facing == 0:
            self.y += 1
        elif self.facing == 1:
            self.x += 1
        elif self.facing == 2:
            self.y -= 1
        elif self.facing == 3:
            self.x -= 1
    def moveBackward(self):
        if self.facing == 0:
            self.y -= 1
        elif self.facing == 1:
            self.x -= 1
        elif self.facing == 2:
            self.y += 1
        elif self.facing == 3:
            self.x += 1


    def program(self, percept):
        self.steps += 1
        self.explored.append((self.x, self.y))
        print(self.kb.audit())

        self.kb.tell(f'-wumpus{self.x}{self.y}') # If I am alive there is not a wumpus on my square
        self.kb.tell(f'-pit{self.x}{self.y}') # If I am alive there is not a pit on my square

        if self.steps == 1 and (percept[0] == 'Stench' or percept[1] == 'Breeze'):
            return 'Climb'
        
        if self.kb.ask('wumpus00') == True and self.kb.ask('wumpus01') == True and self.kb.ask('wumpus02') == True:
            self.exit = True
        
        if self.exit == False and (self.steps > 80):
            self.exit = True
        
        # Update kb with new percepts
        if (percept[3] == 'Bump'):
            self.kb.tell(f'wall{self.x}{self.y}')
            self.moveBackward()
        
        if (percept[0] == 'Stench'):
            self.kb.tell(f'stench{self.x}{self.y}')
        else:
            self.kb.tell(f'-stench{self.x}{self.y}')
        
        if (percept[1] == 'Breeze'):
            self.kb.tell(f'breeze{self.x}{self.y}')
        else:
            self.kb.tell(f'-breeze{self.x}{self.y}')
        
        if (percept[4] == 'Scream'):
            for x in range(3):
                for y in range(3):
                    self.kb.retract(f"wumpus{x}{y}")
                    self.kb.retract(f"stench{x}{y}")
            self.kb.tell("scream")

        # Always grab the gold if you can, then try to leave
        if (percept[2] == 'Glitter'):
            self.exit = True
            logging.debug("Doing action {}.".format('Grab'))
            return 'Grab'
        

        # Choose and log action
        actions = ['TurnRight', 'TurnLeft']
        action = 'Forward'

        if self.exit == True:
            if (self.x, self.y) == (0,0):
                logging.debug("Doing action {}.".format('Climb'))
                return 'Climb'
            else:
                x = self.x
                y = self.y
                self.moveForward()
                if (self.x, self.y) in self.illegal:
                    self.moveBackward()
                    self.facing = (self.facing + 1) % 4
                    return 'TurnRight'
                if ((self.x, self.y) in self.explored):
                    if (self.x < x or self.y < y):
                        action = 'Forward'
                    else:
                        self.moveBackward()
                        self.facing = (self.facing + 1) % 4
                        action = 'TurnRight'
                else:
                    action = random.choices(['Forward', 'TurnRight'], [2, 18], k=1)[0]
                    if action == 'TurnRight':
                        self.moveBackward()
                        self.facing = (self.facing + 1) % 4
                return action

            
        while(1):
        
            # Update coordinates
            if action == 'TurnRight':
                self.facing = (self.facing + 1) % 4
                break
            elif action == 'TurnLeft':
                self.facing = (self.facing - 1) % 4
                break
            elif action == 'Forward':
                self.moveForward()
                if (self.x, self.y) in self.explored:
                    action = random.choices(['Forward', 'TurnRight'], [2, 18], k=1)[0]
            
            if action != 'Forward':
                self.moveBackward()
                continue

            # Don't go out of bounds
            if (self.x < 0 or self.y < 0 or self.x > 3 or self.y > 3):
                self.moveBackward()
                action = random.choice(actions)
            # If thats a wall or a pit don't do it
            elif (self.kb.ask(f'wall{self.x}{self.y}') == True or self.kb.ask(f'pit{self.x}{self.y}') == True):
                action = random.choice(actions)
                self.moveBackward()
            # If thats the wumpus kill it
            elif self.kb.ask(f'wumpus{self.x}{self.y}') == True:
                self.moveBackward()
                action = 'Shoot'
                break
            # If its not the wumpus and not a pit then go there
            elif self.kb.ask(f'wumpus{self.x}{self.y}') == False and self.kb.ask(f'pit{self.x}{self.y}') == False:
                break
            else:
                self.moveBackward()
                action = random.choice(actions)

        logging.debug("Doing action {}.".format(action))
        # print(self.kb.audit())
        return action