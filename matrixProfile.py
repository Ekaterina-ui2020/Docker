import math
import numpy as np
from scipy import signal


def user_input():
    while True:
        try:
            file1 = input("Enter the name of the file contain first time series(.bin.npy): ")
            Ta_try = np.load(file1, mmap_mode='r')
        except FileNotFoundError or ValueError:  # problems with the file
            continue  # ask for file again
        else:  # all good
            break
    while True:
        try:
            file2 = input("Enter the name of the file contain second time series(.bin.npy): ")
            Tb_try = np.load(file2, mmap_mode='r')
        except FileNotFoundError or ValueError:
            continue
        else:
            break
    # get correct shapes
    try:  # see if more than one time series
        Ta_try.shape[1]
    except IndexError:  # it has only one time series
        Ta = Ta_try  # use it
    else:  # more then one time series
        Ta = Ta_try[0]  # only use the first one

    try:  # see if more than one time series
        Tb_try.shape[1]
    except IndexError:  # it has only one time series
        Tb = Tb_try  # use it
    else:  # more then one time series
        Tb = Tb_try[0]  # only use the first one

    while True:
        try:
            m = int(input("Enter the subsequence length as integer: "))
        except ValueError:
            print("It must be integer!")
            continue
        else:
            if m > min(Ta.shape[0], Tb.shape[0]):
                print("The subsequence length is bigger than time series")
                continue
            else:
                break

    return Ta, Tb, m


# ***********************************ComputeMeanStd(T, Q)***************************************
# This function calculates means of Q and each subset of T and
# the standard deviation of Q and each subset of T
def ComputeMeanStd(Q, T):
    n = len(T)
    m = len(Q)
    size = n - m + 1
    muT = np.zeros(size)  # the means of the subsets of T size m
    muQ = np.mean(Q)  # the mean of Q
    sdT = np.zeros(size)  # the standard deviations of the subsets of T size m
    sdQ = np.std(Q)
    for i in range(0, n - m + 1):
        x = T[i: i + m]  # creat subsets of T
        muT[i] = np.mean(x)  # calculate means foe each subset
        sdT[i] = np.std(x)  # calculate standard deviations foe each subset with m in denom
    return muQ, sdQ, muT, sdT


# *************************************MASS(T, Q)***********************************************
# THis function calculates the Z-Normalized Euclidian distance between
# Q and each subset of T
def MASS(Q, T):
    n = len(T)
    m = len(Q)
    QT = np.array(signal.fftconvolve(T, Q[::-1], mode='valid'))
    mQ, sQ, mT, sTm = ComputeMeanStd(Q, T)
    D = np.zeros(n - m + 1)
    for i in range(0, n - m + 1):
        # D[i]=math.sqrt(2*m*(1-(QT[i]-m*mQ*mT[i])/(m*sQ*sTm[i]))) #from the paper
        try:
            D[i] = math.sqrt(2 * m * (1 - (QT[i] - m * mQ * mT[i]) / (m * sQ * sTm[i])))  # from the paper
        except ValueError:  # catch the rounding error
            D[i] = math.sqrt(2 * m * (1 - (QT[i] - m * mQ * mT[i] - 0.000000000000001) / (m * sQ * sTm[i])))
    return D


def STAMP(Ta, Tb, m):
    na = Ta.shape[0]
    size = na - m + 1
    Pab = np.zeros(size)
    Iab = np.zeros(size, dtype='int')
    idxes = np.arange(0, size)
    for idx in idxes:
        D = MASS(Ta[idx:idx + m], Tb)
        Pab[idx] = np.amin(D)
        Iab[idx] = np.argmin(D)
    return Pab, Iab


def main():
    print("This program calculates the matrix profile for series Ta and Tb from user provided files and user provided "
          "subsequence length m.")
    print("If files contain more then one time series, the first one will be used.")
    print("The program stores the matrix profile Pab and matrix profile index Iab in 'Profile.txt' and "
          "'Index.txt' files.")

    Ta, Tb, m = user_input()
    print("Calculating Matrix profile...")
    Pab, Iab = STAMP(Ta, Tb, m)
    # save to the files
    np.savetxt("Index.txt", Iab)
    np.savetxt("Profile.txt", Pab)
    print("Done")


if __name__ == "__main__":
    main()
