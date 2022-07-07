#!/usr/bin/env python

"""GameAI.py: INF1771 GameAI File - Where Decisions are made."""
#############################################################
#Copyright 2020 Augusto Baffa
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#############################################################
__author__      = "Augusto Baffa"
__copyright__   = "Copyright 2020, Rio de janeiro, Brazil"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "abaffa@inf.puc-rio.br"
#############################################################

from operator import truediv
import random
from turtle import position
from Map.Position import Position
import numpy as np
# <summary>
# Game AI Example
# </summary>
class GameAI():

    player = Position()
    state = "ready"
    dir = "north"
    score = 0
    energy = 0

    map = []
    coluna = []
    for j in range(34):
        coluna.append(0)
    for i in range(59):
        map.append(coluna)
        

    goalPosition = Position(5,15)
    goalDir = "north"
    itemClose = "false"
    turnOffPrint = False
    action = ""



    # <summary>
    # Refresh player status
    # </summary>
    # <param name="x">player position x</param>
    # <param name="y">player position y</param>
    # <param name="dir">player direction</param>
    # <param name="state">player state</param>
    # <param name="score">player score</param>
    # <param name="energy">player energy</param>
    def SetStatus(self, x, y, dir, state, score, energy):
    
        self.player.x = x
        self.player.y = y
        self.dir = dir.lower()

        self.state = state
        self.score = score
        self.energy = energy
        
        if(self.state == "dead" and not self.turnOffPrint):
            self.PrintUtils()
            self.turnOffPrint = True



    # <summary>
    # Get list of observable adjacent positions
    # </summary>
    # <returns>List of observable adjacent positions</returns>
    def GetObservableAdjacentPositions(self):
        ret = []

        ret.append(Position(self.player.x - 1, self.player.y))
        ret.append(Position(self.player.x + 1, self.player.y))
        ret.append(Position(self.player.x, self.player.y - 1))
        ret.append(Position(self.player.x, self.player.y + 1))

        return ret


    # <summary>
    # Get list of all adjacent positions (including diagonal)
    # </summary>
    # <returns>List of all adjacent positions (including diagonal)</returns>
    def GetAllAdjacentPositions(self):
    
        ret = []

        ret.Add(Position(self.player.x - 1, self.player.y - 1))
        ret.Add(Position(self.player.x, self.player.y - 1))
        ret.Add(Position(self.player.x + 1, self.player.y - 1))

        ret.Add(Position(self.player.x - 1, self.player.y))
        ret.Add(Position(self.player.x + 1, self.player.y))

        ret.Add(Position(self.player.x - 1, self.player.y + 1))
        ret.Add(Position(self.player.x, self.player.y + 1))
        ret.Add(Position(self.player.x + 1, self.player.y + 1))

        return ret
    

    # <summary>
    # Get next forward position
    # </summary>
    # <returns>next forward position</returns>
    def NextPosition(self):
    
        ret = None
        
        if self.dir == "north":
            ret = Position(self.player.x, self.player.y - 1)
                
        elif self.dir == "east":
                ret = Position(self.player.x + 1, self.player.y)
                
        elif self.dir == "south":
                ret = Position(self.player.x, self.player.y + 1)
                
        elif self.dir == "west":
                ret = Position(self.player.x - 1, self.player.y)

        return ret
    

    # <summary>
    # Player position
    # </summary>
    # <returns>player position</returns>
    def GetPlayerPosition(self):
        return self.player


    # <summary>
    # Set player position
    # </summary>
    # <param name="x">x position</param>
    # <param name="y">y position</param>
    def SetPlayerPosition(self, x, y):
        self.player.x = x
        self.player.y = y

    

    # <summary>
    # Observations received
    # </summary>
    # <param name="o">list of observations</param>
    def GetObservations(self, o):

        #cmd = "";
        for s in o:
            
            self.PrintUtils(s)
            if s == "blocked":
                self.SetGoalPositionRandom()
                pass
            
            elif s == "steps":
                pass
            
            elif s == "breeze":
                self.careful = True

            elif s == "flash":
                pass

            elif s == "blueLight":
                self.itemClose = True

            elif s == "redLight":
                if self.energy < 100:
                    self.itemClose = True
                

            elif s == "greenLight":
                pass

            elif s == "weakLight":
                pass
            
            elif str(s).find("enemy") != -1:
                print("\nENEMY\n")
                self.action = "atacar"
                pass


    # <summary>
    # No observations received
    # </summary>
    def GetObservationsClean(self):

        pass
    


    # <summary>
    # Get Decision
    # </summary>
    # <returns>command string to new decision</returns>
    def GetDecision(self):

        if self.state == "dead":
            return ""
        else:
            self.turnOffPrint = False

        if self.action != "":
            command = self.action
            self.action = ""
            print(command)
            return command

        if EqualPositions(self.player,self.goalPosition):
            print("chegou")
            list = self.SetGoalPositionRandom()

        ## para evitar poço
        if self.careful == True:
            i  =1
            # nao sei

        n = random.randint(0,7)
        

        if (self.GetPlayerPosition().x < self.goalPosition.x):
            self.goalDir = "east"
        elif (self.GetPlayerPosition().x > self.goalPosition.x):
            self.goalDir = "west"
        elif (self.GetPlayerPosition().y < self.goalPosition.y):
            self.goalDir = "south"
        elif (self.GetPlayerPosition().y > self.goalPosition.y):
            self.goalDir = "north"


        self.PrintUtils()


    	if (self.itemClose == True):
            return ["pegar_ouro", "pegar_anel", "pegar_powerup"]
        if (self.DecideTurn()):   
            return "virar_direita"
        elif (n == 99):
            print("vai pra esquerda!")
            return "virar_esquerda"
        elif self.dir == self.goalDir:
            return "andar"
        elif n == 3:
            return "atacar"
        elif n == 4:
            return "pegar_ouro"
        elif n == 5:
            return "pegar_anel"
        elif n == 6:
            return "pegar_powerup"
        elif n == 7:
            return "andar_re"

        return ""


    

    def DecideTurn(self):
        if not self.dir == self.goalDir:
            return True
        else:
            return False

    def SetGoalPositionRandom(self):
        x = random.randint(0,58)
        y = random.randint(0,33)
        self.goalPosition = Position(x,y)


    def PrintUtils(self, msg = ""):
        print("~~~~~~ PRINT ~~~~~~")
        if not self.state == "dead":
            print("position: ", (self.player.x, self.player.y))
            print("goal position: ", (self.goalPosition.x, self.goalPosition.y))
            if msg != "":
                print(msg)
        else:
            print("Dead...")
        print("")




def EqualPositions(pos1, pos2):
    if pos1.x == pos2.x and pos1.y == pos2.y:
        return True
    else:
        False