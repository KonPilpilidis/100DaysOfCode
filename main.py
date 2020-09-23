### This is the main executable file for the game the Platform. ###

## Necessary packages
import logging
from random import randint, gauss
import logging.config
logging.config.fileConfig("logging.conf")
import game
logger = logging.getLogger('root')

## Setup logging







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    x=game.Hole()
    print(x)
    for i in range(len(x.prison)):
        for j in range(len(x.prison[i])):
            print(x.prison[i][j])
