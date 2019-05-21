import svd #import the code
import scipy.io  #only for loading the matlab matrix here
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

# Test matrix from AMOS code
matfile = scipy.io.loadmat('stokes64s.mat')

print(repr(matfile.keys()))

Prob = matfile['Problem'][0][0][2]

print(repr(Prob.shape))

# Once the RowMatrix is ready we can compute our Singular Value Decomposition
svd = svd.computeSVD(Prob,2,True)
print svd.s
print svd.U
print svd.V