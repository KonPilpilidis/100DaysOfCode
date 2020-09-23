import logging
from random import randint, gauss

logger = logging.getLogger('game')

import homebrew
# General parameters: the hole
FLOORS = 333
CELLS = 2
TOTAL = 360
CYCLE = 30
# General parameters: the inmates
## Height
b_hei = (140, 220)
AV_HEI_M = 165
AV_HEI_W = 155
SD_HEI_B = 10
## Weight
b_wei = (35, 200)
b_bmi = (18, 41)
AV_BMI= 26.7     # Since the movie is spanish, I take the average BMI in Spain according to Wikipedia
SD_BMI= 3
FACTOR_W = 10    # The impact of weight on caloric needs
## Other
b_age = (18, 65) # The employees of the Hole claim that there are no children in the Hole
CAL_P_KG = 7500  # The number of calories needed to lose or gain a kilo
MAX_FOOD = 6500  # An arbitrary number for how many calories a prisoner can eat in one sitting
MIN_BMI  = 11    # The BMI after which prisoners are expected to die of starvation

class Hole:
    """
    This is the object which represents the prison.
    Attributes
        :attribute  CELLS: The int indicating the number of prisoners per floor
        :attribute FLOORS: The int indicating the number of floors in the prison
        :attribute  TOTAL: The int indicating the total duration of the sentence
        :attribute  CYCLE: The int indicating after how many days the prisoner's are moved to a new cell
    """
    def __init__(self,n=FLOORS,m=CELLS,t=TOTAL):
        """
        Init method of a Hole object. It populates the Hole with prisoner's and calculates the calories needed for the platform.
        :param n: The int indicating the number of floors.
        :param m: The int indicating the number of prisoner's per floor.
        :param t: The int indicating the duration of the sentence.
        :return: None
        """
        n,m,t = [homebrew.notInt(x) for x in [n,m,t]]
        self.provided_cal = 0  # the variable holding the number of calories the platform carries
        self.prison = []  # the variable holding the prisoners objects
        self.duration = t
        id = 0
        for i in range(n):
            self.prison.append([])
            for j in range(m):
                id +=1
                inmate = Prisoner(id)
                self.provided_cal += inmate.curr_needs
                self.prison[i].append(inmate)

    def __str__(self):
        """
        the str method of a Hole object
        :return: str
        """
        return "Floors: {} \nCell size: {} \nCalories on platform: {}".format(len(self.prison),len(self.prison[0]),self.provided_cal)




class Prisoner(object):
    def __init__(self,id):
        """
        Init method of a Prisoner object.
        Each prisoner's caloric needs are calculated according to a random gender, age, weight, and height based on the
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
        The string method of an object of Prisoner type.
        :return: string
        """
        return "{}: {} {} - W: {} H: {} / N: {}/{} ({})".format(self.id,'man  ' if self.man==1 else 'woman','alive' if self.alive == 1 else 'dead',
                                                                round(self.weight,1),round(self.height,1),self.curr_needs,self.init_needs,self.hunger)
    def weight_change(self):
        """
        The method changes the BMI and the weight of a prisoner and calculates whether he/she is dead.
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
