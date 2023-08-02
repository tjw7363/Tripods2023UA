"""
Train a discrete neural net using only endomorphisms
"""

from pathlib import Path

path = str(Path(__file__).parent.parent.absolute() / "src")
import sys
sys.path.insert(0, path)

from discrete_neural_net import Neuron, Layer, NeuralNet
from binary_image_polymorphisms import RotationAutomorphism, polymorphism_neighbor_func, hamming_distance, ReflectionAutomorphism, IndicatorPolymorphism
from mnist_training_binary import binary_train_for_zero, show

# Our neural net will have one input.
layer0 = Layer(('x',))

# There is only a single output neuron and no hidden layers.
neuron0 = Neuron(RotationAutomorphism(1), ('x',))

layer1 = Layer([neuron0])

#Tryna add a second neuron
neuron1 = Neuron(RotationAutomorphism(2), ('x',))
layer1 = Layer([neuron0,neuron1])

#Add a third neuron
neuron2 = Neuron(IndicatorPolymorphism(), (neuron0,neuron1))
layer2 = Layer([neuron2])



net = NeuralNet([layer0, layer1, layer2])

# The MNIST training set will be used to train this discrete neural net to detect the handwritten digit 0.
# Load some binary images from the modified MNIST training set.
training_pairs = binary_train_for_zero(100)

# We can check out empirical loss with respect to this training set.
# Our loss function will be the Hamming distance.
print(net.empirical_loss(training_pairs, loss_func=lambda x, y: hamming_distance(x[0], y[0])))
print()

# Use the training set for a list of constant images to use for swapping/blanking endomorphisms.
constant_images = [pair[0]['x'] for pair in training_pairs]

net.train(training_pairs, lambda op: polymorphism_neighbor_func(op, 4, constant_images=constant_images),
          100, lambda x, y: hamming_distance(x[0], y[0]), report_loss=True)


