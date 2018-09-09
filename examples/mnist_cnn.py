from ml.cnn import CNN2D
from ml.data import mnist
import numpy as np

c = CNN2D(
    layers=2,
    inp=784,
    out=10,
    kernel_size=[5, 5],
    pool_size=[2, 2],
    filters=[32, 64],
    dimensions=[28, 28],
)
c.fit(data=mnist.train.images, labels=np.asarray(mnist.train.labels, dtype=np.int32), lr=0.001)
c.test(data=mnist.test.images, labels=np.asarray(mnist.test.labels, dtype=np.int32))
