# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from mpmath import *
import quandl
from scipy import optimize
import numpy
import sympy
import matplotlib.pyplot as plt

# mp.dps = 4; mp.pretty = True

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # https://users.math.yale.edu/public_html/People/frame/Fractals/FracAndDim/Moran/MoranSolutions.html
    # FindRoot[.5^d + .5^d + .5^d + .25^d == 1,{d,1}]
    # print(findroot(lambda x: .5 ** x + .5 ** x + .5 ** x + .25**x - 1, 0))

    # https://users.math.yale.edu/public_html/People/frame/Fractals/RandFrac/Cartoon/UnifractalCartoons/UnifractalScaling.html
    # |dYi| = (dti)^H

    q = quandl.get("EOD/HD", authtoken="ufbdsyreuGemgDeEfsZH")
    q2 = quandl.Dataset("EOD/HD").data()

    hd_date_price = {}

    cnter = 0
    for cPrice in q.get("Adj_Close"):
        # https://stackoverflow.com/questions/46778680/quandl-python-the-date-column-not-working
        date = str(q.index[cnter]).split(' ')
        hd_date_price[date[0]] = cPrice
        cnter += 1

    # print(hd_date_price.keys())
    # print(hd_date_price.values())

    # for p in list(hd_date_price.values())[1:]:
    #    dY.append(p - list(hd_date_price.values())[p - 1])

    # NOTES
    # log(1) = 0
    # log(0) = Err: Domain

    # H = {} - 2 days, 7 days, 15 days, 30 days [delta]
    # Hurst value for each delta
    H = {}
    delta = 2  #  val of '2' returns value of -1.54
    H[delta] = []
    N = 0

    absDy = []  # list containing only positive changes
    Dy = []  # list of positive and negative changes

    # https://stackoverflow.com/questions/4002598/how-to-get-the-previous-element-when-using-a-for-loop
    # https://www.kite.com/python/answers/how-to-access-every-other-element-in-a-list-using-a-for-loop-in-python#:~:text=Use%20enumerate()%20to%20access,check%20if%20index%20is%20even.
    for index, Y1 in enumerate(list(hd_date_price.values())):
        # print(index, Y1)
        if index % delta == 0:
            N += 1
            try:
                Y2 = list(hd_date_price.values())[index + delta]  # increment to next Y value

                H[delta].append(log10(abs(Y2 - Y1)) / log10(delta))  # compute H

                # print(abs(Y2 - Y1))
                if abs(Y2 - Y1) == 0: # if no change in price, append the same as before
                    absDy.append(absDy[index - 1])
                    Dy.append(Dy[index - 1])
                else:
                    absDy.append(abs(Y2 - Y1))
                    Dy.append(Y2 - Y1)

                # https://users.math.yale.edu/public_html/People/frame/Fractals/
                # Hi = Log|dYi|/Log(dti)
                # https://users.math.yale.edu/public_html/People/frame/Fractals/FracAndDim/Moran/MoranDerivation.html
                # 1 = |dY1|^D + |dY2|^D + |dY3|^D

                # print(log10(abs(Y2 - Y1)) / log10(delta))

            except IndexError:
                break
            except ZeroDivisionError:
                print("Delta cannot be 1. Re-run  with another value of delta")
                break

    # exit()
    # print(len(absDy))
    # print(absDy)
    # print(findroot(lambda x: .5 ** x + .5 ** x + .5 ** x + .25**x - 1, 0))
    # add 1 / r to compress everything into the '= 1' result

    print("N equals:", N)
    fterm = "lambda x: "
    # print(len(absDy))
    cnt = 0
    dYOccurrenceTable = {}
    sumOfDy = 0

    for r in absDy:
    # for r in Dy:

        r = round(r,12)

        # print(r)
        sumOfDy += r

        # add to dictionary of Dy to number of occurrences
        if r not in dYOccurrenceTable:
            dYOccurrenceTable[r] = 1
        elif r in dYOccurrenceTable:
            dYOccurrenceTable[r] += 1

        # create Moran equation based on similarity dimension
        try:
            cnt += 1
            if cnt == len(absDy):
                term = "(1 / " + str(r) + ") ** x  - 1"
            else:
                term = "(1 / " + str(r) + ") ** x  + "

            fterm += term

        except ZeroDivisionError:
            print("divide by 0 error")

    me = "lambda x:"
    # print(len(dYOccurrenceTable.items()))
    tmp = 0
    for term, freq in dYOccurrenceTable.items():

        print(term, freq)

        if tmp < len(dYOccurrenceTable.items()) - 1:
            # Fractal Worlds - page 180 6.4.1
            # me += str(freq) + "/" + str(N) + " * (1/" + str(term) + ") ** x + "
            me += "((" + str(freq) + "/" + str(N) + ") * (1/" + str(term) + ")**x)  + "

        else:
            me += "( (" + str(freq) + "/" + str(N) + ") * (1/" + str(term) + ")  ** x) - 1"

        tmp += 1
        # print("tmp" , tmp)
    # me += ") * " + str(N)
    print(me)
    print("The lambda function is:", findroot(eval(me), -2 ))
    print(optimize.root(eval(me), numpy.array([-2])))
    print()
    #print("The lambda function is:", fterm)
    #print("The computed fractal dimension is:", findroot(eval(fterm), 0))

    # print(optimize.root(eval(me), 0))
    #print(findroot(lambda x: 2 * (1/2) ** x + 2 * (1/3) ** x - 1, 0))  # Fractal Worlds, Page 166

    # print(sympy.nsolve(eval(fterm), (-2,2),  solver='bisect', verify=False))
    #print(optimize.root(eval(fterm), numpy.array([0])))
    #print()

    # print(findroot(lambda x: .5 ** x + .5 ** x + .5 ** x + .25 ** x - 1, 0))
    # https://stackoverflow.com/questions/7719466/i-have-a-string-whose-content-is-a-function-name-how-to-refer-to-the-correspond
    # funct = "lambda x: .5 ** x + .5 ** x + .5 ** x + .25 ** x - 1"

    # print(optimize.root())

    # funct = "lambda x: .5 ** x + .5 ** x +  .5 ** x + .25 ** x - 1"

    # print(optimize.root_scalar(eval(funct), 0))

    # print(optimize.root(eval(funct), 0))
    # print()
    # print(findroot(eval(funct), 0))


    # plt.plot(hd_date_price.keys(), hd_date_price.values())
    # plt.ylabel('Price')
    # plt.show()
