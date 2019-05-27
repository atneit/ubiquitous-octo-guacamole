import pyspark
from pyspark.sql import SQLContext

from pyspark.mllib.common import callMLlibFunc, JavaModelWrapper
from pyspark.mllib.linalg.distributed import RowMatrix

### based on this solution http://stackoverflow.com/questions/33428589/pyspark-and-pca-how-can-i-extract-the-eigenvectors-of-this-pca-how-can-i-calcu/33500704#33500704


def convertDenseVector(i):
    return i.toArray()

class QR(JavaModelWrapper):
    @property
    def Q(self):
        return self.call("Q")
    @property
    def R(self):
        return self.call("R")

def computeQR(A):
    """
    Computes the QR decomposition of the RowMatrix.
    """

    sc = pyspark.SparkContext()
    conf = pyspark.SparkConf()
    conf.set("spark.executor.memory", '20g')
    conf.set('spark.executor.cores', '1')
    conf.set('spark.cores.max', '1')
    conf.set("spark.driver.memory", '20g')

    sm = sc.parallelize(A.toarray(), numSlices=32)
    row_matrix = RowMatrix(sm)

    java_model = row_matrix._java_matrix_wrapper.call("tallSkinnyQR", True)
    qr = QR(java_model)
    print qr.Q
    print qr.R
    return qr