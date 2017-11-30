"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.  
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted 
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen. 
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you 
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of 
    aliens.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.
    
    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None] 
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Invaders.  Only add the getters and setters that you need for 
    Invaders. You can keep everything else hidden.
    
    You may change any of the attributes above as you see fit. For example, may want to 
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        lastkeys: the number of keys pressed in the last animation frame [int >= 0]
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        self._ship = Ship()
        self._aliens = None
        self._bolts = []
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                            linewidth=2,linecolor='turquoise')
        self._lives = 3
        self._time = 0
        self.lastkeys = 0
        self._createAliens()
        
    #HELPER METHODS FOR __INIT__
    #: the width of the game display 
    #GAME_WIDTH  = 800
    #: the height of the game display
    #GAME_HEIGHT = 700
    
    def _createAliens(self):
        self._aliens=[]
        for i in range(ALIENS_IN_ROW):
            temp = []
            for j in range(ALIEN_ROWS):
                if j == 0:
                    #self._aliens[i][j] = Alien(x=(ALIEN_H_SEP + ALIEN_WIDTH//2) + i*(ALIEN_H_SEP+ALIEN_WIDTH),y=GAME_HEIGHT - ALIEN_CEILING - j*(ALIEN_V_SEP+ALIEN_HEIGHT), source = ALIEN_IMAGES[0])
                    temp.append(Alien(X=(ALIEN_H_SEP + ALIEN_WIDTH//2) + i*(ALIEN_H_SEP+ALIEN_WIDTH),Y=GAME_HEIGHT - ALIEN_CEILING - j*(ALIEN_V_SEP+ALIEN_HEIGHT), W = ALIEN_WIDTH, H = ALIEN_HEIGHT, LW = 0, FC = None, S = ALIEN_IMAGES[2]))
                elif j == 1 or j == 2:
                    #self._aliens[i][j] = Alien(x=(ALIEN_H_SEP + ALIEN_WIDTH//2) + i*(ALIEN_H_SEP+ALIEN_WIDTH),y=GAME_HEIGHT - ALIEN_CEILING - j*(ALIEN_V_SEP+ALIEN_HEIGHT), source = ALIEN_IMAGES[1])
                    temp.append(Alien(X=(ALIEN_H_SEP + ALIEN_WIDTH//2) + i*(ALIEN_H_SEP+ALIEN_WIDTH),Y=GAME_HEIGHT - ALIEN_CEILING - j*(ALIEN_V_SEP+ALIEN_HEIGHT), W = ALIEN_WIDTH, H = ALIEN_HEIGHT, LW = 0, FC = None, S = ALIEN_IMAGES[1]))
                else:
                    #self._aliens[i][j] = Alien(x=(ALIEN_H_SEP + ALIEN_WIDTH//2) + i*(ALIEN_H_SEP+ALIEN_WIDTH),y=GAME_HEIGHT - ALIEN_CEILING - j*(ALIEN_V_SEP+ALIEN_HEIGHT), source = ALIEN_IMAGES[2])
                    temp.append(Alien(X=(ALIEN_H_SEP + ALIEN_WIDTH//2) + i*(ALIEN_H_SEP+ALIEN_WIDTH),Y=GAME_HEIGHT - ALIEN_CEILING - j*(ALIEN_V_SEP+ALIEN_HEIGHT), W = ALIEN_WIDTH, H = ALIEN_HEIGHT, LW = 0, FC = None, S = ALIEN_IMAGES[0]))
            self._aliens.append(temp)
    
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt):        
        if input.is_key_down('left') and self._ship.x > SHIP_WIDTH/2:
            self._ship.moveShipLeft()
        if input.is_key_down('right') and self._ship.x < GAME_WIDTH-(SHIP_WIDTH/2):
            self._ship.moveShipRight()
        self._pressBolt(input)
        # print("1: " + str(self._bolts))
        for bolt in range(len(self._bolts)):
            self._bolts[bolt].moveBolt()
            # print("2 " + str(self._bolts))
            if self._bolts[bolt].y > GAME_HEIGHT:
                del self._bolts[bolt]
                # print("3 " + str(self._bolts))
        
    
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        for i in range(ALIENS_IN_ROW):
            for j in range(ALIEN_ROWS):
                self._aliens[i][j].draw(view)
        self._ship.draw(view)
        self._dline.draw(view)
        for x in range(len(self._bolts)):
            self._bolts[x].draw(view)
                
    # HELPER METHODS FOR COLLISION DETECTION
    
    # HELPER METHOD FOR DETERMINE STATE
    def _playerBoltExists(self):
        for x in range(len(self._bolts)):
            if self._bolts[x].getVelocity() > 0:
                return True
            else:
                return False
        
    
    def _pressBolt(self, input):
        """
        Determines if there was a key press
        
        This method checks for a key press, and if there is one, creates a
        player bolt.  A key press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as we hold down the key.
        The user must release the key and press it again to change the state.
        
        Acknowledgements: Uses code inspired by Walker M. White
        Source: https://www.cs.cornell.edu/courses/cs1110/2017fa/assignments/assignment7/samples/state.py
        """
            # Determine the current number of keys pressed
        curr_keys = input.key_count
            # Only change if we have just pressed the keys this animation frame
        change = curr_keys > 0 and self.lastkeys == 0 and input.is_key_down('spacebar')
        
        if change and self._playerBoltExists == False:
               # Click happened.  Change the state
            self._bolts.append(Bolt(self._ship.x,self._ship.y+SHIP_HEIGHT/2))
        
            # Update last_keys
        self.lastkeys= curr_keys
