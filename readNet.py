import codecs
import numpy as np


def Edge2Sparse(datapath):
    """
    read an input network of unweighted network

    input:
    --------
    input network in terms of edge list, for eample, email-Eu-core-department-labels.txt from http://snap.stanford.edu/data/
    
    output:
    --------
    adjacency matrix of the input network
   
    """
    fe = codecs.open(datapath, mode='r',
                         encoding='utf-8')  
    lineE = fe.readline()  # read files as lines
    listE1 = []
    lE = []
    nodeE1 = []
    nodeE2 = []
    max1 = 0
    num = []
    while lineE:
        a = lineE.split()
        b1 = a[0:1]  # select the number of bits to read
        for i1 in b1:
            i1 = int(i1)
            if max1 < i1:
                max1 = i1

            nodeE1.append(i1)

        b2 = a[1:2]
        for i2 in b2:
            i2 = int(i2)
            if max1 < i2:
                max1 = i2

            nodeE2.append(i2)

        lE.append(i1)
        lE.append(i2)

        listE1.append(lE)  
        lE = []
        lineE = fe.readline()
    fe.close()
    print(max1)
    print(len(listE1))
    aE = np.zeros((1005, 1005))
    k = 0

    for i in listE1:
        aE[i[0]][i[1]] = 1
        aE[i[1]][i[0]] = 1
    return aE
