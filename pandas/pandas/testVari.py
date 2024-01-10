import numpy as np
import matplotlib.pyplot as plt
import random

def shiftArray():
    v = np.array([1, 2, 3, 4])
    print(v)
    v = np.roll(v, -1)
    print(v)
    np.roll()

def plotChangingGraph():
    data = [0]
    plt.ion()
    plt.show()
    
    for i in range(10):
        n = random.random()
        data.append(n)
        plt.plot(data, 'k')
        plt.draw()
        plt.pause(0.5)

def openFileAndPlotBarPlot():
   f = open("pandas/weights.txt", 'r')
   lines = f.readlines()
   f.close()

   header = lines[0].replace('\n', '')
   header = list(header.split(','))
   header.remove('')
   firstbar = lines[1].replace('\n', '')#.replace(',',';').replace('.',',')
   firstbar = list(firstbar.split(','))
   firstbar.remove('')
   for i in range(len(firstbar)):
       firstbar[i] = float(firstbar[i])
   

   plt.bar(header, firstbar)
   plt.yscale(value = 'linear')
   plt.show()

def printConnStringhe():
    fruit_names = ['Coffee', 'Salted Caramel', 'Pistachio']
    fruit_counts = [4000, 2000, 7000]

    fig, ax = plt.subplots()
    bar_container = ax.bar(fruit_names, fruit_counts)
    ax.set(ylabel='pints sold', title='Gelato sales by flavor', ylim=(0, 8000))
    ax.bar_label(bar_container)
    plt.show()

#https://www.statology.org/numpy-shift/
#define custom function to shift elements
def shift_elements(arr, num, fill_value):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result[:] = arr
    return result

if __name__ == "__main__":
   #plotChangingGraph()
   #openFileAndPlotBarPlot()
   #printConnStringhe()
   #shiftArray()

   data = np.array([1, 2, 3, 4, 5, 6])
   data = shift_elements(data, 2, nan)
   print(data)