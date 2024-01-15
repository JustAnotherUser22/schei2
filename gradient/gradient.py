import numpy as np
import matplotlib.pyplot as plt 

#square = lambda x: x**2

def square(x):
   return x*x

def gradient1D():
   dx = 0.001

   #x = list(range(-10, 11, 0.1))
   x = np.arange(-2, 2, dx)   #np.arange funziona anche con step non interi!
   x = np.array(x)
   y = square(x)
   
   print(x)
   print(y)

   firstDerivative = np.gradient(y, dx)
   print(firstDerivative)

   secondDerivative = np.gradient(firstDerivative)
   
   plt.plot(x, y)
   plt.plot(x, firstDerivative)
   plt.plot(x, secondDerivative)
   plt.show()

def gradient2D():
   dx = 0.001
   dy = 1
   
   x = np.arange(-2, 2, dx)
   y = np.arange(-2, 2, dy)
   x, y = np.meshgrid(x, y)
   z = x**2 + y**2

   #grad_x = np.gradient(z, 0.001, axis = 0)
   #grad_y = np.gradient(z, 1, axis = 1)
   #grad_x, grad_y = np.gradient(z)
   grad_x, grad_y = np.gradient(z, dy, dx)   #non so perchè sia questo l'ordine di dx e dy ma così funziona

   fig = plt.figure()
   ax = fig.add_subplot(111, projection='3d')
      
   ax.plot_surface(x, y, z)
   ax.plot_surface(x, y, grad_x)
   ax.plot_surface(x, y, grad_y)

   ax.set_xlabel('X Label')
   ax.set_ylabel('Y Label')
   ax.set_zlabel('Z Label')

   plt.show()
   
def gradient3D():
   dx = 1
   dy = 1
   dz = 1
   
   x = np.arange(-5, 5, dx)
   y = np.arange(-5, 5, dy)
   z = np.arange(-5, 5, dz)
   x, y, z = np.meshgrid(x, y, z)
   function = x**2 + y**2 + z**2

   fig = plt.figure()
   ax = fig.add_subplot(111, projection='3d')
      
   img = ax.scatter(x, y, z, c = function, cmap = plt.hot())
   fig.colorbar(img) 
   plt.show()

   grad_x, grad_y, grad_z = np.gradient(function)

   #img = ax.scatter(x, y, z, c = grad_x, cmap = plt.hot())
   #fig.colorbar(img) 
   #plt.show()



def main():
   #gradient1D()
   #gradient2D()
   gradient3D()


if __name__ == "__main__":
   main()