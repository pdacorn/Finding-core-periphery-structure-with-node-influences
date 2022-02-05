import numpy as np
import timeit
from scipy.sparse import identity
from scipy.sparse import csr_matrix

def step1(sparse_mat, iter = 10,ep=0.5):  
    '''
    calculate the influence value
    
    parameter:
    ----
    sparse_mat: scipy.sparse.csr.csr_matrix
       sparse adjacency matrix of the input network
    iter: int
       number of iteration
    ep: float
       hyperparameter

    returns
    ----
    power: numpy.ndarray
       influence matrix of the input network

    '''  
    #initialize inference parameters
    res = np.inf
    n = sparse_mat.shape[0]
    power = np.identity(n).astype(np.float32)
    sparse_mat = sparse_mat.astype(np.float32) 
    #the sum of the row of the sparse matrix aims to normalization
    degree2 = np.transpose(np.sum(np.abs(np.array(sparse_mat.todense())),1))+1e-20
    degree2=degree2.reshape(-1,1)
    #calculate the identity matrix, corresponding to \beta/(1+\beta)*identity matrix in our article
    one_ep_eye = (1-ep)*np.identity(n).astype(np.float32)
    #calculate influence matrix
    for i in range(iter):
        start = timeit.default_timer()
        power0=power
        res0=res
        start_temp = timeit.default_timer()
        #corresponding to Eq.(8) in our article
        power = power*ep+one_ep_eye
        end_temp = timeit.default_timer()
        print('Run time init: ', end_temp - start_temp)
        start_temp = timeit.default_timer()
        power = sparse_mat.dot(power)
        end_temp = timeit.default_timer()
        print('Run time matmul: ', end_temp - start_temp)
        start_temp = timeit.default_timer()
        #normalize the influence matrix        
        power=power/degree2
        end_temp = timeit.default_timer()
        print('Run time power/degree: ', end_temp - start_temp)    
        end = timeit.default_timer()
        print('Run time: ', end - start)
        res = np.mean(np.abs(power - power0))
        print('Diff: ', res)
        #stop interating when the difference doesn't change much
        if res >= 0.99*res0: 
            break
    power = np.array(power)      
    return power

def step2(power,topNinfluencer = 1):
    '''
    calculate the pair id of each node belonging to 

    parameter: 
    ----
    power: numpy.ndarray
      matrix of influence value of email network

    topNinfluencer: int
      number of nodes with top influences

    returns:
    ----
    pairidnum : numpy.ndarray
      pair id of each node belonging to

    '''
    start = timeit.default_timer()
    #initialize the local parameters
    from scipy.sparse import csr_matrix
    maxinfmat = csr_matrix(power.shape)
    power0 = np.copy(power)
    n = np.shape(power)[0]
    # Build an sparse adjacency matrix maxinfmat,
    #  where connections between each node and the node has the max influcen on it are one
    #  and all the other entries are zero
    for i in range(topNinfluencer):
        id = np.argmax(power0, axis=1)
        maxinfmat = maxinfmat + csr_matrix((np.ones(n), (range(n), id)), power.shape)
        for j in range(n):
            power0[j,id[j]] = -1


    # ---separate nodes into multiple pairs---
    '''
    ------nodes in the same pair is found by that iteratively finds the current node and the node that has the greatest influence on it, until the found node has been visited----
    parameters:
    ----
    isvisited: ndarray
      if node i is visited, then isvisited[i]=0, otherwise, isvisited[i]=-1; aim to prevent infinite loop to find neiborhood 
    
    cachelistsize: int
      the pair's size

    currentlist: ndarray
      nodes' id containing in current pair
    
    currentid: int
      current node's id

    maxinfmatUd: scipy.sparse.csr.csr_matrix
      the connections between each node in the adjacency matrix and the node with the greatest influence on it are one, and all the other entries are zero

    pairidnum: int
      pair id   
    '''
    # convert to symmetric matrix
    maxinfmatUd = maxinfmat + maxinfmat.transpose()
    #initialize local parameters
    cachelist = np.zeros(n, dtype=np.int)
    cachelistsize = 0
    isvisited = -np.ones(n)
    pairidnum = -np.ones(n, dtype=np.int) 
    totalcom = 0
    for i in range(n):
        if isvisited[i] == -1:            
            cachelistsize = 0
            currentlist = [] 
            currentlist.append(i)
            isvisited[i] = 0           
            while(len(currentlist) != 0):
                currentid = currentlist.pop()
                cachelist[cachelistsize] = currentid
                cachelistsize += 1
                neighbors = maxinfmatUd[currentid,:].nonzero()[1]
                for j in neighbors:            
                    if isvisited[j] == -1:# 成环了就用isvisited
                        currentlist.append(j)
                        isvisited[j] = 0     
            for j in range(cachelistsize):
                pairidnum[cachelist[j]] = totalcom
            totalcom += 1               
    end = timeit.default_timer()       
    print('Run time (mycp_2b): ', end - start)
    return pairidnum 

def step3(power, coreratio = -1, influenceratio = -1): 
    '''
    calculate if the node is a core or a periphery, and the core value

    there are two ways to separate the core nodes and the periphery nodes: one is to choose the top 'coreratio' nodes as core nodes directly,
    the other is to choose a minimum number of nodes with total influences no less than 'influenceratio' of that of all the nodes.

    parameter:
    -----
    power: numpy.ndarray
      matrix of influence value of email network

    coreratio: float
      choose top 'coreratio' of nodes with largest influences as core nodes

    influenceratio: float
      choose a minimum number of nodes with total influences no less than 'influenceratio' of that of all the nodes

    returns:
    ----
    corenessnum: array[bool]
      if node i is a core node, corenessnum[i]=1, otherwise, corenessnum[i]=0

    core: array[float]
      the node core score
    '''
    if coreratio == -1 and influenceratio == -1:
       print("Either coreratio or influenceratio should be passed, but not both. ")
       return 
    if coreratio == -1 and influenceratio == -1:
       print("Either coreratio or influenceratio should be passed, but not neither. ")
       return
    start = timeit.default_timer()
    core = np.mean(power,0)
    n = len(core)
    # coreratio = 0.1
    if coreratio != -1 :
        threshold = np.sort(core)[np.round(n*(1-coreratio)).astype(int)]
        corenessnum = (core>threshold)

    # influenceratio = 0.5
    if influenceratio != -1 :
        coresort = np.sort(core)[::-1]
        threshold = coresort[np.where(np.cumsum(coresort)>influenceratio)[0][0]]
        corenessnum = (core>threshold)
    end = timeit.default_timer()       
    print('Run time (mycp_3): ', end - start)
    return corenessnum,core       






