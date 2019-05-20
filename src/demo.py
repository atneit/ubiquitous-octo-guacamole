# easy way to install pyspark, no need for big configuration
import findspark
findspark.init()

import svd #import the code

import scipy.io #only for loading the matlab matrix here

# Test matrix from AMOS code
matfile = scipy.io.loadmat('shallow_water1.mat')

print(repr(matfile.keys()))

Prob = matfile['Problem'][0][0][2]

print(repr(Prob.shape))

# Once the RowMatrix is ready we can compute our Singular Value Decomposition
svd = svd.computeSVD(Prob,2,True)
print svd.s
print svd.U
print svd.V