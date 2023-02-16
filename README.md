# Finding core-periphery structure with node influences

This code implements the influence-based core-periphery detection algorithm (ICPA) in python for detecting multiple core-periphery pairs given adjacency networks. This work can be cited as follows:

>Xin Shen, Sarah Aliko, Yue Han, Jeremy I Skipper, & Chengbin Peng. (2021). Finding core-periphery structures with node influences. IEEE Transactions on Network Science and Engineering, In press 10.1109/TNSE.2021.3138436.

## Running influence-based core-periphery detection algorithm (ICPA) models
From `Test.py`, we can see how to use the uploaded files.

Firstly, **you may create the adjacency matrix with the following approach**.

Besides email-Eu-core-department-labels.txt, many other data sets are available, for example, at http://snap.stanford.edu/data

(see line 2-10 in Test.py)
```python
import icpa_sparse_matrix
import timeit
import readNet
from importlib import reload
from scipy.sparse import csr_matrix

dt0=readNet.Edge2Sparse('email-Eu-core-department-labels.txt')
dt0_sparse = csr_matrix(dt0)
```
The returned dt0_sparse is a sparse adjacency matrix.

Secondly, **you can obtain pair identities and core scores from our algorithm (ICPA) outputs**
1. The parameter `corenessnum` indicates whether a node is a core or a periphery. Here, zero indicates a periphery node, and one indicates a core node.
(see line 26 in Test.py)
``` python
corenessnum,corescore =icpa_sparse_matrix.step3(power, influenceratio = influenceratio)
```
2. The parameter of `pairidnum` indicates each node's pair id.
(see line 20 in Test.py)
``` python
pairidnum = icpa_sparse_matrix.step2(power,topNinfluencer = 1)
```

