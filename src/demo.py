import svd  #import the code
import qr  #import the code
import scipy.io  #only for loading the matlab matrix here
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

func = svd.computeSVD
#func = qr.computeQR

mat = "A"

if mat is "A":
    A = scipy.sparse.csr_matrix(scipy.io.loadmat('IEEERTS96Adjacency.mat')['A'])

    print(repr(A.shape))

    # Once the RowMatrix is ready we can compute our Singular Value Decomposition
    res = func(A)
elif mat is "B":
    # Test matrix from AMOS code
    matfile = scipy.io.loadmat('stokes64s.mat') #12000 x 12000

    print(repr(matfile.keys()))

    Prob = matfile['Problem'][0][0][2]

    print(repr(Prob.shape))

    # Once the RowMatrix is ready we can compute our Singular Value Decomposition
    res = func(Prob)
elif mat is "C":
    # Test matrix from AMOS code
    matfile = scipy.io.loadmat('bcsstk13.mat') #2000 x 2000

    print(repr(matfile.keys()))

    Prob = matfile['Problem'][0][0][1]

    print(repr(Prob.shape))

    # Once the RowMatrix is ready we can compute our Singular Value Decomposition
    res = func(Prob)

print(res)