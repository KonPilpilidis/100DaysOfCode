## This packege contains usefull homebrew functions
logging.config.fileConfig(".gitignore/auxiliary.log")
logger = logging.getLogger('auxiliary')

def randtrunc(a=None,b=None,mu=0.0,sd=1.0):
    """
    Returns a random value following a normal distribution between a and b with a mean of mu and a standard deviation of sd.
    When one number is given, the method tests whether the number is lower or higher that the mean of the distribution.
    and truncates the distribution either left or right.
    :param a:  first truncation point possible
    :param b: second truncation point
    :param mu: mean of the distribution
    :param sd: standard deviation of distribution
    :return: a float
    """
    assert type(a) != str,  "The minimum value needs to be numeric."
    assert type(b) != str,  "The maximum value needs to be numeric."
    assert type(mu) != str,"The average value needs to be numeric."
    assert type(sd) != str, "The st. deviation needs to be numeric."
    if a == mu or b == mu:
        logger.warning("Method randtrunc - unexpected arguments: minimum or maximum is equal to mean")
        return mu
    elif a == b and (a!=None and b != None):
        logger.warning("Method randtrunc - unexpected arguments: minimum is equal to maximum")
        return a
    elif a == b and a == None:
        logger.info("Method randtrunc - unexpected arguments: no minimum or maximum values were provided")
        return random.gauss(mu,sd)
    elif a == None and b < mean:
        a = b
        b = float('inf')
        logger.debug("Method randtrunc - b was used as the minimum value")
    elif b == None and a > mean:
        b = a
        a = float('-inf')
        logger.debug("Method randtrunc - a was used as the maximum value")
    elif b < a:
        step = a
        a = b
        b = step
        logger.debug("Method randtrunc - minimum and maximum were passed in the reverse order")
    elif a == None and b > mean:
        a = float('-inf')
        logger.debug("Method randtrunc - left truncated")
    elif b == None and a < mean:
        b = float('inf')
        logger.debug("Method randtrunc - right truncated")
    else:
        logger.debug("Method randtrunc - both sides truncated")
    if sd == 0:
        return mu
    num = random.gauss(mu,sd)
    while num <= a or num >= b:
        num = random.gauss(mu,sd)
    logger.info("Randtrunc(a={},b={},mu={},sd={})={}".format(a,b,mu,sd,num))
    return num

def control(variablelist):
    """
    The method takes a list of variables and converts them to integers by rounding the number
    :return variablelist:
    """
    for i in range(len(variablelist)):
        if type(variablelist[i]) == float:
            variablelist[i] = round(variablelist[i])
            logger.debug("Initialization - Arg:{} was recasted to int".format(1+i))
        else:
            pass
    return variablelist