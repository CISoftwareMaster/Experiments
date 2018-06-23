from datetime import datetime


def prng(base=2**32, x=43814981931, y=44319):
    # generate a pseudo random number using a seed
    prng.seed = (prng.seed * x + y) % base
    return prng.seed / base

def generateBirthdates(personCount) -> list:
    birthdays = []
    # use the machine's current microsecond as our seed
    prng.seed = datetime.now().time().microsecond

    # generate birthdays
    for i in range(personCount):
        birthdays.append(round(prng() * 365))
    return birthdays

def findMatch(birthdays: list) -> bool:
    n = len(birthdays)
    # try to find a match in the birthday list
    for i in range(n):
        sample = birthdays[i]
        for j in range(n):
            if sample == birthdays[j] and i != j:
                return True
    return False


def probability(n=50, cycles=10000):
    score = 0

    # perform a Monte Carlo Simulation
    for _ in range(cycles):
        # test if two people share the same birthday
        # within a group of {n} people.
        if findMatch(generateBirthdates(n)):
            score += 1

    # calculate the probability
    chance = (score / cycles) * 100
    print("The probability of two people sharing the same birthday")
    print(("within a group of %i people is: %.2f" % (n, chance)) + "%")
