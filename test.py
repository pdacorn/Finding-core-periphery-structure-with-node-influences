
import icpa_sparse_matrix
import timeit
import readNet
from importlib import reload
from scipy.sparse import csr_matrix


dt0=readNet.Edge2Sparse('email-Eu-core-department-labels.txt')
dt0_sparse = csr_matrix(dt0)

start = timeit.default_timer()
# maximum number of iterations
maxIter = 20 

#caculate the influence matrix
power = icpa_sparse_matrix.step1(dt0_sparse, iter = maxIter,ep=0.5) 

#the pair id each node belonging to 
pairidnum = icpa_sparse_matrix.step2(power,topNinfluencer = 1)

# choose top 15% of nodes with largest influences as core nodes
#coreratio = 0.15
# choose a minimum number of nodes with total influences no less than 50% of that of all the nodes
influenceratio = 0.5 
corenessnum,corescore =icpa_sparse_matrix.step3(power, influenceratio = influenceratio)
end = timeit.default_timer()
print('Run time: ', end - start)


corenum=[]
for i in corenessnum:
    
    if i ==True:
        corenum.append(1)
    else:
        corenum.append(0)
l=[]
node=[]
print(len(pairidnum))
for i in range(len(pairidnum)):
    l.append(i)
    l.append(pairidnum[i])
    l.append(corenum[i])
    node.append(l)
    l=[]
node