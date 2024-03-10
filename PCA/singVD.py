
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt 


def main():
   # a is a tensor.
   # s is a tensor of singular values.
   # u is a tensor of left singular vectors.
   # v is a tensor of right singular vectors.

   x = []
   y = []

   for i in range(0, 10, 1):
      x.append(i)
   print(x)
   
   x = np.array(x)
   y = 2 * x + np.random.uniform(low = -0.5, high = .5, size = 10)

   a = [x, y]
   a = np.array(a)
   print(a.shape)
   #a = np.dot(a, a.T)


   s, u, v = tf.linalg.svd(a)
   s = np.array(s)
   u = np.array(u)
   v = np.array(v)
   print(s)
   print(s.shape)
   print(u.shape)
   u = np.array(u)
   print(v.shape)
   tf.linalg.svd(a, compute_uv=False)

   print(a)

   axis = u[0,:].T
   axis = axis.reshape(1, 2)

   reduced = np.dot(axis, a)
   print(reduced)

   b = np.linalg.pinv(np.dot(axis.T, axis))
   reconstructed = np.dot(b, np.dot(axis.T, reduced))
   reconstructed = abs(reconstructed)
   print(reconstructed)

   plt.plot(x, y, '+')
   plt.plot(reconstructed[0,:], reconstructed[1,:], 'o')
   plt.show()





if __name__ == "__main__":
   main()