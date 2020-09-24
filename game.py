import logging
from copy import deepcopy
from random import randint, gauss

logger = logging.getLogger('game')

import homebrew
# General parameters: the hole
FLOORS = 333        # int indicating the number of inmates per floor
CELLS = 2           # int indicating the number of floors in the prison
TOTAL = 360         # int indicating the total duration of the sentence
CYCLE = 30          # int indicating after how many days the inmates are moved to a new cell
# General parameters: the inmates
## Height
b_hei = (140, 220)  # minimum and maximum height for an inmate
AV_HEI_M = 165      # int for the average height for a male inmate
AV_HEI_W = 155      # int for the average height for a male inmate
SD_HEI_B = 10       # int for the sd of height for inmates
## Weight
b_wei = (35, 200)   # minimum and maximum weight for an inmate
b_bmi = (18, 41)    # minimum and maximum body mass index for an inmate
AV_BMI= 26.7        # int for the average BMI. Since the movie is spanish, I take the average BMI in Spain according to Wikipedia
SD_BMI= 3           # int for the sd of the BMI (arbitrarily chosen)
FACTOR_W = 10       # int unit change of cal.needs for a unit change in weight according to the Mifflin St Jeor Equation.
## Other
b_age = (18, 65)    # minimum and maximum age of inmates. The employees of the Hole claim that there are no children in the Hole
CAL_P_KG = 7500     # int calories needed to lose or gain a kilo
MAX_FOOD = 6500     # int maximum calories an inmate can eat (before his stomach rips)
MIN_BMI  = 11       # int the BMI after which inmates die of starvation

class Hole:
    """
    An instance of the Hole at a specific point in time.
    Methods:
    __init__: generates and populates a Hole with a platform
        :returns None
    __str__: string method of a class Hole
        :returns str
    feed: moves the Platform and allows inmates to eat
        :returns None
    cycle: removes corpses, re-populates the prison and relocates the inmates
        :returns None
    """
    def __init__(self,n=FLOORS,m=CELLS,t=TOTAL):
        """
        Init method of a Hole object: populates the Hole with inmate's and calculates the calories needed for the platform.
        :param n: int indicating the number of floors.
        :param m: int indicating the number of inmates per floor.
        :param t: int indicating the duration of the sentence.
        :return: None
        """
        n,m,t = [homebrew.notInt(x) for x in [n,m,t]]
        self.provided_cal = 0                           # float: number of calories the platform carries
        self.prison = {}                                # dict: holding the inmates objects
        self.duration = t
        id = 0
        for i in range(n):
            self.prison[i] = {}
            for j in range(m):
                id +=1
                self.prison[i][j] = Inmate(id)
                self.provided_cal += self.prison[i][j].curr_needs
    def __str__(self):
        """
        str method of a Hole object
        :return: str
        """
        return "Floors: {} \nCell size: {} \nCalories on platform: {}".format(len(self.prison),len(self.prison[0]),self.provided_cal)
    def feed(self):
        """
        The method starts the platform full with food which is eaten along the way. When the food is totally eaten, it
        increases the hunger of the remaining inmates.
        :method eat: The method that calls the necessary functions for the inmates to eat.
        :return: None
        """
        def eat(self, loc, available):
            """
            The method calls the function that makes the inmates of a floor to start eating and if there is not enough
            calls the function that makes them respond to the lack of food
            :param loc: The floor of the prison which is being fed
            :param available: The quantity of available food
            :return:
            """
            claims = 0
            for i in range(len(self.prison[loc])):
                claims += self.prison[loc][i].claim() * (self.prison[loc][i].alive == 1)
            if claims > available:
                response = {}
                for i in range(len(self.prison[loc])):
                    if self.prison[loc][i].alive == 1:
                        response[self.prison[loc][i].id] = self.prison[loc][i].notEnough()
            return claims
        food = self.provided_cal
        for i in range(len(self.prison)):
            if food > 0:
                food -= eat(i, food)
            else:
                for j in range(len(self.prison[i])):
                    if self.prison[i][j].alive == 1:
                        self.prison[i][j].hunger += self.prison[i][j].curr_needs
    def cycle(self):
        """
        The method removes dead inmates, relocates inmates from non-full floors together with other inmates from
        non-full floors. Generates inmates to fill the Hole. Relocates all inmates.
        ** In the film, it was not clear whether an inmate can be at the same level more than once.
        :return: list of lists
        """
        pass




class Inmate(object):
    """
    An instance of an inmate.
    Methods:
    __init__: Generates a random gender, weight, height, age, BMI and number of calories the object needs per day.
        :returns None
    __str__: string method of a class Inmate
        :returns str
    weight_change:
        :returns None
    """
    def __init__(self,id):
        """
        Init method of a Inmate object.
        Each inmate's caloric needs are calculated according to a random gender, age, weight, and height based on the
        Mifflin St Jeor Equation.
        Hunger is a variable holding the caloric deficit/surplus of the inmate.
        """
        self.id = id
        self.man = randint(0, 1)
        age = randint(b_age[0],b_age[1])
        self.height = homebrew.randtrunc(b_hei[0],b_hei[1],AV_HEI_M * (self.man == 1) + AV_HEI_W * (self.man == 0),SD_HEI_B)
        bmi = homebrew.randtrunc(b_bmi[0],b_bmi[1],AV_BMI,SD_BMI)
        self.weight, self.min_weight = ((self.height/100) ** 2) * bmi, ((self.height/100) ** 2) * MIN_BMI
        self.weight = round(self.weight, 2)
        self.height = round(self.height, 2)
        self.init_needs = round(FACTOR_W * self.weight + 6.25 * self.height - 5 * age + (self.man == 1) * 5 - 161 * (self.man == 0),2)
        self.curr_needs = self.init_needs
        self.hunger = 0
        self.alive = 1
    def __str__(self):
        """
        The string method of an object of Inmate type.
        :return: string
        """
        return "{}: {} {} - W: {} H: {} / N: {}/{} ({})".format(self.id,'man  ' if self.man==1 else 'woman','alive' if self.alive == 1 else 'dead',
                                                                round(self.weight,1),round(self.height,1),self.curr_needs,self.init_needs,self.hunger)
    def weight_change(self):
        """
        The method changes the BMI and the weight of an inmate and calculates whether he/she is dead.
        :return: None
        """
        if self.hunger >= abs(CAL_P_KG):
            if self.hunger > 0:
                self.weight -= 1
                self.curr_needs -= FACTOR_W
            else:
                self.weight += 1
                self.curr_needs += FACTOR_W
            self.bmi = self.weight / (self.height ** 2)
            if self.bmi < MIN_BMI:
                self.alive = 0
