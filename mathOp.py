import re
from termcolor import colored as coloured


# compile our regular expression pattern
pattern = re.compile("(?<=[0-9])(?=([\-\+\*\/]|$))")

def floatify(x, default=0):
    try: return float(x)
    except: return default


def solveEquation(eqstr):
    terms = []
    total = 0

    # check if parentheses count checks out
    if eqstr.count("(") - eqstr.count(")") != 0:
        print("A parentheses block isn't closed.")
        return total

    # last start index
    lastIndex = 0

    # remove all the whitespace
    eqstr = eqstr.replace(" ", "")

    # parentheses block variables
    depth = 0
    blockStart = 0
    finalEqstr = eqstr

    # solve parentheses blocks
    for i in range(len(eqstr)):
        # set the start of block
        if eqstr[i] == '(':
            if depth == 0:
                blockStart = i

            # increase our block depth
            depth += 1

        # terminate parentheses check when block depth is zero
        if eqstr[i] == ')':
            depth -= 1

            # block zero depth
            if depth == 0:
                parenthesesBlock = eqstr[blockStart + 1 : i]

                # solve the extracted equation
                result = str(solveEquation(parenthesesBlock))

                # and replace the parentheses block with our result
                finalEqstr = finalEqstr.replace(f"({parenthesesBlock})", f"b{result}")

    # ordering lists
    oo = {"b": [], "o": [], "dm": [], "as": []}

    # last term value and reference
    lastTerm = None
    lastTermRef = None

    # split equation string into terms
    for match in pattern.finditer(finalEqstr):
        term = finalEqstr[lastIndex : match.start()]
        lastIndex = match.start()

        # reorder equation (so it complies to the order of operations properly)
        if term.startswith('-'):
            oo['as'].append(term)
            lastTermRef = oo['as']

        elif term.startswith('**'):
            # remove the last term from the previous container
            if lastTermRef is not None:
                lastTermRef.remove(lastTerm)
                oo["o"].append(lastTerm)

            oo['o'].append(term)
            lastTermRef = oo['o']

        elif term.startswith('*'):
            if lastTermRef is not None:
                lastTermRef.remove(lastTerm)
                oo["dm"].append(lastTerm)

            oo['dm'].append(term)
            lastTermRef = oo['dm']

        elif term.startswith('/'):
            if lastTermRef is not None:
                lastTermRef.remove(lastTerm)
                oo["dm"].append(lastTerm)

            oo['dm'].append(term)
            lastTermRef = oo['dm']

        elif term.startswith('+'):
            oo['as'].append(term)
            lastTermRef = oo['as']

        elif term.startswith('b'):
            oo['b'].append(term)
            lastTermRef = oo['b']

        else:
            oo['as'].append(term)
            lastTermRef = oo['as']

        # last term reference
        lastTerm = term

    # join terms back together
    terms += [x for y in oo for x in oo[y]]
    print(terms)

    # solve it, at long last
    for term in terms:
        # strip brackets marker
        if 'b' in term:
            term = term.replace('b', '')

        # determine which operation we should use
        if term.startswith('-'):
            total -= floatify(term[1::])

        elif term.startswith('**'):
            total **= floatify(term[2::])

        elif term.startswith('*'):
            total *= floatify(term[1::])

        elif term.startswith('/'):
            try:
                total /= floatify(term[1::])
            except ZeroDivisionError:
                print(f"Trying to divide by zero! Excluding {term} from this equation.")

        elif term.startswith('+'):
            total += floatify(term[1::])
        else:
            total += floatify(term)

    # return the result of our equation
    return total


def solve(x):
    print(f"\nSolving for \"{x}\"...")
    print(coloured(f"{solveEquation(x):,}", "yellow"))


solve("(10 * 50) * ((20 + 5) * 100)") # expected: 1,250,000
solve("((((50 + 20) - 30) * 10) + ((30 / 2) * 12)) / 10") # expected: 58
solve("10 - 30 * ((50) + (20)) - 10") # expected: -2,100
solve("(2 ** 8) ** 2") # expected: 65,536
solve("((10 + 5) * 12) - (12 + 5)") # expected: 163
solve("7 - 1 x 0 + 3 / 3") # expected: 8
solve("1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 * 0 + 1") # expected: 12
