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
    def __init__(self,n=FLOORS,m=CELLS):
        """
        Init method of a Hole object: populates the Hole with inmate's and calculates the calories needed for the platform.
        :param n: int indicating the number of floors.
        :param m: int indicating the number of inmates per floor.
        :param t: int indicating the duration of the sentence.
        :return: None
        """
        n,m,t = [homebrew.notInt(x) for x in [n,m,t]]
        self.__provided_cal = 0                           # float: number of calories the platform carries
        self.__prison = {}                                # dict: holding the inmates objects
        id = 0
        for i in range(n):
            self.__prison[i] = {}
            for j in range(m):
                id +=1
                self.__prison[i][j] = Inmate(id)
                self.__provided_cal += self.__prison[i][j].curr_needs
        logger.INFO(print(self))
    def __str__(self):
        """
        str method of a Hole object
        :return: str
        """
        return "Object Hole - Floors: {} \nCell size: {} \nCalories on platform: {}".format(len(self.__prison),len(self.__prison[0]),self.__provided_cal)
    def getter_provided_calories(self):
        """
        Method to get the number of calories the platform carries
        :return: float
        """
        return self.__provided_cal
    def setter_provided_calories(self):
        """
        Method to re-calculate the number of calories a platform should carry (ex. after new inmates are introduced)
        :return: None
        """
        self.__provided_cal = sum({k: sum(v.values()) for k, v in self.__prison.items()}.values())
    def feed(self):
        """
        The method starts the platform full with food which is eaten along the way. When the food is totally eaten, it
        increases the hunger of the remaining inmates.
        :method eat: The method that calls the necessary functions for the inmates to eat.
        :return: None
        """
        def calc_consumption(self, loc, available):
            """
            The method calls the function that makes the inmates of a floor to start eating and if there is not enough
            calls the function that makes them respond to the lack of food.
            :param loc: The floor of the prison which is being fed
            :param available: The quantity of available food
            :return:
            """
            claims = []
            consumption = 0
            for i in range(len(self.prison[loc])):
                ate = self.prison[loc][i].eat() * (self.prison[loc][i].alive == 1)
                consumption += ate
                claims.append(ate)
            if consumption <= available:
                for i in range(len(self.prison[loc])):
                    if self.prison[loc][i].alive == 1:
                        self.prison[loc][i].hunger() -= self.prison[loc][i].eat()
            else:
                response = {}
                for i in range(len(self.prison[loc])):
                    if self.prison[loc][i].alive == 1:
                        response[self.prison[loc][i].id] = self.prison[loc][i].notEnough()
            return claims
        food = self.provided_cal
        for i in range(len(self.prison)):
            if food > 0:
                food -= calc_consumption(i, food)
            else:
                for j in range(len(self.prison[i])):
                    if self.prison[i][j].alive == 1:
                        self.prison[i][j].hunger += self.prison[i][j].curr_needs
    def organise(self):
        """
        The method removes dead inmates, relocates inmates from non-full floors together with other inmates from
        non-full floors. Generates inmates to fill the Hole. Relocates all inmates.
        ** In the film, it was not clear whether an inmate can be at the same level more than once.
        :return: list of lists
        """
        pass




class Inmate(object):
    """
    Object inmate responds to the amount of food available on the platform and possesses an object.
    Methods:
    __init__: Generates a random gender, weight, height, age, BMI and number of calories the object needs per day.
        :returns None
    __str__: string method of a class Inmate
        :returns str
    *getters: methods that return the biometric characteristics of an inmate (gender, height, weight) and
        - These characteristics cannot be changed by the user.
    weight_change:
        :returns None
    """
    def __init__(self,id,greed):
        """
        Init method of a Inmate object.
        Each inmate's caloric needs are calculated according to a random gender, age, weight, and height based on the
        Mifflin St Jeor Equation.
        Hunger is a variable holding the caloric deficit/surplus of the inmate.
        :param greed: float between 1 and MAX_FOOD / curr_needs represents how much an inmate tries to overeat.
        """
        self.__id = id
        self.__man = randint(0, 1)
        age = randint(b_age[0],b_age[1])
        self.__height = homebrew.randtrunc(b_hei[0],b_hei[1],AV_HEI_M * (self.__man == 1) + AV_HEI_W * (self.__man == 0),SD_HEI_B)
        bmi = homebrew.randtrunc(b_bmi[0],b_bmi[1],AV_BMI,SD_BMI)
        self.__weight, self.__min_weight = ((self.__height/100) ** 2) * bmi, ((self.__height/100) ** 2) * MIN_BMI
        self.__weight = round(self.__weight, 2)
        self.__height = round(self.__height, 2)
        self.__init_needs = round(FACTOR_W * self.__weight + 6.25 * self.__height - 5 * age + (self.__man == 1) * 5 - 161 * (self.__man == 0),2)
        self.curr_needs = self.__init_needs
        assert (type(greed) == float or type(float) == int) and \
               1 <= greed <= MAX_FOOD / self.curr_needs, "arg greed did not have a valid value"
        self.hunger = 0
        self.__alive = 1
        logger.info(print(self))
    def __str__(self):
        """
        The string method of an object of Inmate type.
        :return: string
        """
        return "Object Inmate {} (Greed {}): {} {} - W: {} H: {} / N: {}/{} ({})".format(self.id,self.greed,
                                            'man  ' if self.man==1 else 'woman','alive' if self.alive == 1 else 'dead',
                                            round(self.weight,1),round(self.height,1),self.curr_needs,self.init_needs,
                                            self.hunger)
    def getter_id(self):
        """
        Method that returns the ID of an inmate
        :return: int
        """
        return self.__id
    def getter_gender(self):
        """
        Method that returns the gender of an inmate
        :return: str
        """
        return 'man' if self.__man == 1 else 'woman'
    def getter_height(self):
        """
        Method that returns the height of an inmate
        :return: float
        """
        return self.__height
    def getter_weight(self):
        """
        Method that returns the weight of an inmate
        :return: float
        """
        return self.__weight
    def getter_init_needs(self):
        """
        Method that returns the initial caloric needs of an inmate
        :return: float
        """
        return self.__init_needs
    def die(self):
        """
        Setter method for the state of an inmate (alive to dead)
        :return: None
        """
        if self.__alive == 1:
            self.alive == 0
        else:
            logger.warning("Just tries to kill a dead inmate {}".format(self.__id))
    def equip(self,item):
        """
        Method gives an item of type Possession to an inmate
        :param item: object Possession
        :return: None
        """
        assert type(item) == Possession,"arg item has an invalid value"
        self.possession = item
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
    def eat(self):
        """
        Method that returns the maximum that an inmate will try to eat.
        :return: float
        """
        return self.greed * self.greed
    def response(self):
        """
        The method contains the inmate's behavior after different events:
        Events list:
        1. Not enough food:
            a. The other inmate(s) attacked
            b. The other inmate(s) did not attack
            c. After attack,
        :return:
        """
class Possession(object):
    """
    Objects of the type Possessions are equipped by the inmates. Each inmate can possess one object and use any object
    left by dead inmates to which he / she has access
    Methods: __init__
    """
    def __init__(self,lethality=0,caloric_needs=0,caloric_value=0):
        self.__lethality = lethality
        self.__caloric_needs = caloric_needs
        self.__caloric_value = caloric_value

class Weapon(Possession):
    """
    Objects of the subclass Weapon are Possessions
    """
    def __init__(self,lethality,caloric_needs=0,caloric_value=0):
        super.__init__(lethality,caloric_needs,caloric_value)
