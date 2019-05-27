import pyspark
from pyspark.sql import SQLContext

from pyspark.mllib.common import callMLlibFunc, JavaModelWrapper
from pyspark.mllib.linalg.distributed import RowMatrix

### based on this solution http://stackoverflow.com/questions/33428589/pyspark-and-pca-how-can-i-extract-the-eigenvectors-of-this-pca-how-can-i-calcu/33500704#33500704


def convertDenseVector(i):
    return i.toArray()

class SVD(JavaModelWrapper):
    """Wrapper around the SVD scala case class"""
    @property
    def U(self):
        """ Returns a RowMatrix whose columns are the left singular vectors of the SVD if computeU was set to be True."""
        u = self.call("U")
        if u is not None:
           return map(convertDenseVector, RowMatrix(u).rows.collect())

    @property
    def s(self):
        """Returns a DenseVector with singular values in descending order."""
        return self.call("s").toArray()

    @property
    def V(self):
        """ Returns a DenseMatrix whose columns are the right singular vectors of the SVD."""
        return self.call("V").toArray()

def computeSVD(A, k=2, computeU=True, rCond=1e-9):
    """
    Computes the singular value decomposition of the RowMatrix.
    The given row matrix A of dimension (m X n) is decomposed into U * s * V'T where
    * s: DenseVector consisting of square root of the eigenvalues (singular values) in descending order.
    * U: (m X k) (left singular vectors) is a RowMatrix whose columns are the eigenvectors of (A X A')
    * v: (n X k) (right singular vectors) is a Matrix whose columns are the eigenvectors of (A' X A)
    :param k: number of singular values to keep. We might return less than k if there are numerically zero singular values.
    :param computeU: Whether of not to compute U. If set to be True, then U is computed by A * V * sigma^-1
    :param rCond: the reciprocal condition number. All singular values smaller than rCond * sigma(0) are treated as zero, where sigma(0) is the largest singular value.
    :returns: SVD object
    """

    sc = pyspark.SparkContext()
    conf = pyspark.SparkConf()
    conf.set("spark.executor.memory", '20g')
    conf.set('spark.executor.cores', '1')
    conf.set('spark.cores.max', '1')
    conf.set("spark.driver.memory", '20g')

    sm = sc.parallelize(A.toarray(), numSlices=8)
    row_matrix = RowMatrix(sm)

    java_model = row_matrix._java_matrix_wrapper.call("computeSVD", int(k), computeU, float(rCond))
    svd = SVD(java_model)
    print svd.s
    print svd.U
    print svd.V
    return svd