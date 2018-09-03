import tensorflow as tf
from ml.error import Error
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    print("Warning: Can't graph from terminal")
import numpy as np


class NeuralNetwork:
    def __init__(self, layers, inp, out, activation):
        try:
            self.activation = activation
        except KeyError:
            print("Invalid Activation Function")
        self.layers = layers
        self.input = inp
        self.output = out
        self.W = []
        self.b = []
        self.x = tf.placeholder(tf.float32, shape=[None, self.input])
        self.yy = tf.placeholder(tf.float32, shape=[None, self.output])
        self.z = self.create_layer(0, self.input, self.layers, self.x, False)
        self.y = self.create_layer(1, self.layers, self.output, self.z, False)
        self.J = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.yy, logits=self.y))

    def fit(self, steps, data, labels, graph=False, check=50, lr=0.001):
        if steps > len(data):
            steps = len(data)
        losses = []
        check_at = int(len(data) / 2)
        optimize = tf.train.AdamOptimizer(learning_rate=lr)
        min = optimize.minimize(self.J)
        self.s = tf.Session()
        self.s.run(tf.global_variables_initializer())
        x_c = data[check_at].reshape(1, self.input)
        y_c = labels[check_at].reshape(1, self.output)
        for i in range(steps):
            x_val = data[i].reshape(1, self.input)
            y_val = labels[i].reshape(1, self.output)
            if i % check == 0:
                losses.append(self.s.run(self.J, feed_dict={self.x: x_c, self.yy: y_c}))
            self.s.run(min, feed_dict={self.x: x_val, self.yy: y_val})
        if graph:
            plt.plot(range(len(losses)), losses)
            plt.show()

    def create_layer(self, layer_number, input_size, output_size, x, nonlinear=True):
        with tf.variable_scope(f"layer_{layer_number}"):
            self.W = tf.get_variable("W", [input_size, output_size])
            self.b = tf.get_variable("b", [1, output_size])
            y = tf.matmul(x, self.W) + self.b
            if nonlinear:
                y = self.activation(self.y)
            return y

    @staticmethod
    def _check_length(arr1, arr2):
        if len(arr1) != len(arr2):
            raise Error("Length of the test arrays should be the same!")
        return False

    def predict(self, x):
        ret = []
        for i in range(len(x)):
            ret.append(self.s.run(self.y, feed_dict={self.x: x[i]}))
        return ret

    def test(self, test_x, test_y):
        self._check_length(test_x, test_y)
        num_c = 0
        for i in range(len(test_x)):
            r = self.s.run(self.y, feed_dict={self.x: test_x[i].reshape(1, self.input)})
            if np.argmax(r[0]) == np.argmax(test_y[i]):
                num_c += 1
        acc = num_c / len(test_x)
        print("Accuracy: {}%".format(acc*100))
        return acc

    def save(self, file_name):
        saver = tf.train.Saver()
        saver.save(self.s, "./" + str(file_name))
        self.s.close()

    def load(self, file_name):
        load = tf.train.Saver()
        self.s = tf.Session()
        load.restore(self.s, file_name)