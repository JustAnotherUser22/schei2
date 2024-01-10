
from keras import models
from keras import layers

"""
test per scrivere e caricare i dati di un modello
"""

checkpoint_path = "D:/script/GenAl/weights/"
checkpoint_name = "population_{0}_entry_{1}"

network = models.Sequential()
network.add(layers.Dense(2, activation='relu', input_shape=(2,)))
network.add(layers.Dense(1))

#network.summary()
print ("parametri prima rete")
print(network.layers[0].get_weights()[0])
print(network.layers[0].get_weights()[1])

network.save_weights(checkpoint_path + checkpoint_name.format(1, 1))

network2 = models.Sequential()
network2.add(layers.Dense(2, activation='relu', input_shape=(2,)))
network2.add(layers.Dense(1))

print ("parametri seconda rete")
print(network2.layers[0].get_weights()[0])
print(network2.layers[0].get_weights()[1])

network2.load_weights(checkpoint_path + checkpoint_name.format(1, 1))

print("parametri della prima rete caricati sulla seconda")
print(network2.layers[0].get_weights()[0])
print(network2.layers[0].get_weights()[1])

layer = network2.layers[0].get_weights()[0]

#print(type(layer))
#print(layer.shape)
print(layer)
layer[1, 1] = 666
print(layer)
