import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

#https://medium.com/@mukesh.mithrakumar/principal-component-analysis-with-tensorflow-2-0-395aaf96bc



def normalize(data):
   # creates a copy of data
   X = tf.identity(data)
   # calculates the mean
   X -=tf.reduce_mean(data, axis=0)
   return X



def main():
   # To start working with PCA, let’s start by creating a 2D data set
   #x_data = tf.multiply(5, tf.random.uniform([100], minval=0, maxval=100, dtype = tf.float32, seed = 0))
   #y_data = tf.multiply(2, x_data) + 1 + tf.random.uniform([100], minval=0, maxval=100, dtype = tf.float32, seed = 0)
   x_data = tf.random.uniform([100], minval=0, maxval=10, dtype = tf.float32, seed = 0)
   y_data = tf.multiply(2, x_data) + 1 + tf.random.uniform([100], minval=0, maxval=1, dtype = tf.float32, seed = 0)
   X = tf.stack([x_data, y_data], axis=1)
   #plt.rc_context({‘axes.edgecolor’:’orange’, ‘xtick.color’:’red’, ‘ytick.color’:’red’})
   #plt.plot(X[:,0], X[:,1], '+', color='b')
   #plt.grid()
   #plt.show()

   normalized_data = normalize(X)
   #plt.plot(normalized_data[:,0], normalized_data[:,1], '+', color='b')
   #plt.grid()
   #plt.show()

   # Finding the Eigne Values and Vectors for the data
   eigen_values, eigen_vectors = tf.linalg.eigh(tf.tensordot(tf.transpose(normalized_data), normalized_data, axes=1))
   print("Eigen Vectors: \n{} \nEigen Values: \n{}".format(eigen_vectors, eigen_values))

   X_new = tf.tensordot(tf.transpose(eigen_vectors), tf.transpose(normalized_data), axes=1)
   plt.plot(X_new[0, :], X_new[1, :], '+', color='b')
   plt.xlim(-5, 5)
   plt.ylim(-15, 15)
   plt.grid()
   plt.show()
   


if __name__ == "__main__":
   main()