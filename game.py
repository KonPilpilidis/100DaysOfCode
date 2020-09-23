# This package contains the method necessary for running the simulation of the hole
logging.config.fileConfig(".gitignore/game.log")
logger = logging.getLogger('game')

# General parameters
class Hole:
    """
    This is the object which represents the prison.
    Attributes
        :attribute  CELLS: The int indicating the number of prisoners per floor
        :attribute FLOORS: The int indicating the number of floors in the prison
        :attribute  TOTAL: The int indicating the total duration of the sentence
        :attribute  CYCLE: The int indicating after how many days the prisoner's are moved to a new cell
    """
    FLOORS = 333
    CELLS = 2
    TOTAL = 360
    CYCLE = 30
    def __init__(self,n=FLOORS,m=CELLS,t=TOTAL):
        """
        Init method of a Hole object. It populates the Hole with prisoner's and calculates the calories needed for the platform.
        :param n: The int indicating the number of floors.
        :param m: The int indicating the number of prisoner's per floor.
        :param t: The int indicating the duration of the sentence.
        :return: None
        """
        variables = homebrew.control([n,m,t])
        self.provided_cal = 0  # the variable holding the number of calories the platform carries
        self.prison = []  # the variable holding the prisoners objects
        self.duration = variables[2]

        for i in range(variables[0]):
            self.prison.append([])
            for j in range(variables[1]):
                inmate = Prisoner("{}:{}".format(i,j))
                self.provided_cal += inmate.needs
                self.prison[i].append(inmate)

    def __str__(self):
        """
        the str method of a Hole object
        :return: str
        """
        return "Floors: {} \nCell size: {} \nCalories on platform: {}".format(len(self.prison),len(self.prison[0]),self.provided_cal)

def start(floors=FLOORS,cells=CELLS,time=TOTAL,change=CYCLE):
    """This function populates the hole.
    :param:
    :param:
    :return: None
    """
b_hei = (1.30, 2.20)
b_wei = (40, 250)
b_bmi = (11, 41)
b_age = (18, 65)
THRESHOLD = 7500