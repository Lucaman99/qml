r"""
Intro to QAOA
=========================

.. meta::
    :property="og:description": Learn how to implement QAOA with PennyLane
    :property="og:image": https://pennylane.ai/qml/_images/qaoa_layer.png

The Quantum Approximate Optimization Algorithm (QAOA) is a widely-studied
method for solving combinatorial optimization problems on NISQ devices.
The applications of QAOA are broad and far-reaching, and the performance
of the algorithm is of great interest to the quantum computing research community.

.. figure:: ../demonstrations/qaoa_module/qaoa_circuit.png
    :align: center
    :width: 90%

The goal of this tutorial is to introduce the basic concepts of QAOA and
to guide you through PennyLane’s built-in QAOA
functionality. You will learn how to use time evolution to establish a
connection between Hamiltonians and quantum circuits, and how to layer
these circuits to create more powerful algorithms. These simple ingredients,
together with the ability to optimize quantum circuits, are the building blocks of QAOA. By focusing
on the fundamentals, PennyLane provides general and flexible capabilities that can be tailored and
refined to implement QAOA for a wide variety of problems. In the last of the tutorial, you will
learn how to bring these pieces together and deploy a complete workflow for using QAOA to solve the
minimum vertex cover problem. Let's get started! 🎉


Circuits and Hamiltonians
-------------------------

When considering quantum circuits, it is often convenient to define them by a
series of quantum gates. But there are many instances where
it is useful to think of a quantum circuit in terms of a
`Hamiltonian <https://en.wikipedia.org/wiki/Hamiltonian_(quantum_mechanics)>`__.
Indeed, gates are physically implemented by performing time evolution under a carefully engineered
Hamiltonian. These transformations are described by the time evolution operator,
which is a unitary defined as:"""

######################################################################
#  .. math:: U(\hat{H}, \ t) \ = \ e^{-i \hat{H} t / \hbar}.
#
# .. figure:: ../demonstrations/qaoa_module/ham_circuit.png
#     :align: center
#     :width: 70%
#
# The time evolution operator is determined completely in terms of a Hamiltonian
# :math:`\hat{H}` and a scalar :math:`t` representing time. In fact, any unitary
# :math:`U` can be written in the form :math:`e^{i \gamma H}`, where :math:`\gamma` is a scalar
# and :math:`H` is a Hermitian operator,
# interpreted as a Hamiltonian. Thus, time evolution establishes a connection that allows us to
# describe quantum circuits in terms of Hamiltonians. 🤯
#
# In general, implementing a quantum circuit that exactly exponentiates a Hamiltonian
# with many non-commuting terms, i.e., a Hamiltonian of the form:
#
# .. math:: H \ = \ H_1 \ + \ H_2 \ + \ H_3 \ + \ \cdots \ + \ H_N
#
# is very challenging. Instead, we can use the
# `Trotter-Suzuki <https://en.wikipedia.org/wiki/Lie_product_formula>`__ decomposition formula
#
# .. math:: e^{A \ + \ B} \ \approx \ \Big(e^{A/n} e^{B/n}\Big)^{n},
#
# to implement an *approximate* time-evolution unitary:
#
# .. math:: U(\hat{H}, t, n) \ = \ \displaystyle\prod_{j \ = \ 1}^{n}
#           \displaystyle\prod_{k} e^{-i \hat{H}_k t / n} \ \ \ \ \ \ \ \ \ \ \hat{H} \
#           = \ \displaystyle\sum_{k} \hat{H}_k,
#
# where :math:`U` approaches :math:`e^{-i \hat{H} t}` as :math:`n`
# becomes larger.
#
# In PennyLane, this is implemented using the ``qml.templates.ApproxTimeEvolution`` template.
# For example,  (TODO: add  example, with circuit printout)
#


######################################################################
# Layering circuits
# -----------------
#
# Think of all the times you have copied a text or image, then pasted it repeatedly to create
# many duplicates. This is also a useful feature when designing quantum algorithms!
# The idea of repetition is ubiquitous in quantum computing:
# from amplitude amplification in `Grover’s algorithm
# <https://en.wikipedia.org/wiki/Grover%27s_algorithm>`__
# to layers in `quantum neural networks
# <https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.1.033063>`__,
# and `Hamiltonian simulation
# <https://en.wikipedia.org/wiki/Hamiltonian_simulation>`__, repeated application
# of a circuit is a central tool in quantum algorithms.
#
#
# .. figure:: ../demonstrations/qaoa_module/repeat.png
#     :align: center
#     :width: 100%
#
#
# Circuit repetition is implemented in PennyLane using the ``qml.layer`` function. This method
# allows us to take a function containing either quantum operations, a template, or even a single
# quantum gate, and repeatedly apply it to a set of wires.
#
# .. figure:: ../demonstrations/qaoa_module/qml_layer.png
#     :align: center
#     :width: 90%
#
# To create a larger circuit consisting of many repetitions, we pass the circuit to be
# repeated as an argument and specify the number of repetitions:
# (TODO: add code snippet with circuit printout)
#

######################################################################
#
# .. figure:: ../demonstrations/qaoa_module/layer.png
#     :align: center
#     :width: 90%
#
# We have learnt how time evolution can be used to create circuits from Hamiltonians,
# and how these can be layered to create longer circuits. This means we are now ready to
# explore QAOA.
#


######################################################################
# QAOA
# ----
#
# The quantum approximate optimization algorithm (QAOA) is a general technique that can be used
# to find approximate solutions to combinatorial optimization problems, in particular problems
# that can be cast as searching for an optimal bitstring. QAOA consists of the following
# steps:
#
# 1. Define a *cost Hamiltonian* :math:`H_C` such that its ground state
#    encodes the solution to the optimization problem.
#
# 2. Define a *mixer Hamiltonian* :math:`H_C`.
#
# 3. Construct the circuits :math:`e^{-i \gamma H_C}` and :math:`e^{-i\alpha H_M}`. We call
#    these the *cost* and *mixer layers*, respectively.
#
# 4. Choose a parameter :math:`n\geq 1` and build the circuit
#
#    .. math:: U_{\text{QAOA}}(\boldsymbol\gamma, \ \boldsymbol\alpha) \ = \ e^{-i \alpha_n H_M}
#              e^{-i \gamma_n H_C} \ ... \ e^{-i \alpha_1 H_M} e^{-i \gamma_1 H_C},
#
#    consisting of repeated application of the cost and mixer layers.
#
# 5. Prepare an initial state, apply :math:`U(\boldsymbol\gamma,\boldsymbol\alpha)`,
#    and use classical techniques, e.g. gradient descent, to optimize the parameters.
#
# 6. After the circuit has been optimized, measurements of the output state reveal
#    approximate solutions to the optimization problem.
#
# In summary, the starting point of QAOA is the specification of cost and mixer Hamiltonians.
# We then use time evolution and layering to create a variational circuit and optimize its
# parameters. Finally, we sample from the circuit to get an approximate solution to
# the optimization problem. Let's see it in action! 🚀
#

######################################################################
# Minimum Vertex Cover with QAOA
# ------------------------------
#
# Our goal is to find the `minimum vertex
# cover <https://en.wikipedia.org/wiki/Vertex_cover>`__ of a graph.
# A vertex cover is a collection of vertices such that
# each edge in the graph contains at least one of the vertices in the cover. Hence,
# these vertices "cover" all the edges.
# We wish to find the vertex cover that has the
# smallest possible number of vertices. Vertex covers can be represented by a bit string
# where each bit denotes whether the corresponding vertex is present in the cover. For example,
# the bit string 1001 represents a cover consisting of the first and last vertex.
#
# .. figure:: ../demonstrations/qaoa_module/minvc.png
#     :align: center
#     :width: 90%
#
# To implement QAOA with PennyLane, we first import the necessary dependencies:
#


import pennylane as qml
from pennylane import qaoa
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx


######################################################################
# We also define the four-vertex graph for which we
# want to find the minimum vertex cover:

# Defines the graph
edges = [(0, 1), (1, 2), (2, 0), (2, 3)]
graph = nx.Graph(edges)

# Draws the graph
nx.draw(graph)
plt.show()


######################################################################
# There are two minimum vertex covers of this graph: the vertices 0 and 2,
# and the vertices 1 and 2. These can be respectively represented by the bit strings 1010 and
# 0110. The goal of the algorithm is to sample these bit strings with high probability.
#
# The PennyLane QAOA module has a collection of built-in optimization
# problems, including minimum vertex cover. For each problem, you can retrieve the cost Hamiltonian
# as well as a recommended mixer Hamiltonian. This
# makes it straightforward to obtain the Hamiltonians for specific problems while still
# permitting the flexibility to make other choices, for example by adding constraints or
# experimenting with different mixers.
#
# In our case, the cost
# Hamiltonian has two ground states, :math:`|1010\rangle` and :math:`|0110\rangle`, coinciding
# with the solutions of the problem. The recommended
# mixer Hamiltonian is designed such that, starting from a state representing a valid cover,
# we never leave the space of valid covers when evolving under the cost or mixer Hamiltonians.

cost_h, mixer_h = qaoa.min_vertex_cover(graph)

print("Cost Hamiltonian")
print(cost_h)
print("--------------------")
print("Mixer Hamiltonian")
print(mixer_h)

######################################################################
# A single layer of QAOA consists of time evolution under these
# Hamiltonians. While it is possible to use `ApproxTimeEvolution`, the QAOA module allows you to
# build the cost and mixer layers directly using the functions ``cost_layer()`` and
# ``mixer_layer()``, which take as input the respective Hamiltonian and variational parameters:


def qaoa_layer(gamma, alpha):
    qaoa.cost_layer(gamma, cost_h)
    qaoa.mixer_layer(alpha, mixer_h)

######################################################################
# We are now ready to build the full variational circuit. The number of wires is equal to
# the number of vertices of the graph. We initialize the state to a valid
# cover, in this case the state :math:`|1111\rangle`.
# For this example, we employ a circuit consisting of two QAOA layers:


wires = range(4)
depth = 2


# Defines the full QAOA circuit
def circuit(params, **kwargs):
    # prepares initial state
    for w in wires:
        qml.PauliX(wires=w)
    # creates repetitions of the QAOA layer
    qml.layer(qaoa_layer, depth, params[0], params[1])


######################################################################
# Note that ``qml.layer`` allows us to pass variational parameters
# ``params[0]`` and ``params[1]`` into each layer of the circuit. That's it! The last
# step is PennyLane's specialty: optimizing the circuit parameters.
#
# The cost function is the expectation value of :math:`H_C`, which we want to minimize. The
# function ``qml.VQECost`` is designed for this purpose: it returns the
# expectation value of an input Hamiltonian with respect to the circuit's output state.
# We also define the device on which the simulation is
# performed. We use the PennyLane-Qulacs plugin to
# run the circuit on the Qulacs simulator:
#

# Defines the device
dev = qml.device("qulacs.simulator", wires=wires)

# Defines the cost function
cost_function = qml.VQECost(circuit, cost_h, dev)


######################################################################
# Finally, we optimize the cost function using the built-in
# ``qml.GradientDescentOptimizer``. We perform optimization for forty steps and initialize the
# parameters randomly from a normal distribution:


# Defines the optimizer, steps, and initial parameters
optimizer = qml.GradientDescentOptimizer()
steps = 40
params = np.random.normal(0, 1, (2, 2))

# Optimizes the cost function
for i in range(steps):
    params = optimizer.step(cost_function, params)
    print("Step {} / {}".format(i + 1, steps))

# Prints the optimal parameters
print("Optimal Parameters: {}".format(params))


######################################################################
# With the optimal parameters, we can now reconstruct the probability
# landscape. We redefine the
# full QAOA circuit with the optimal parameters, but this time we
# return the probabilities of measuring each bitstring:
#

@qml.qnode(dev)
def probability_circuit(gamma, alpha):
    circuit([gamma, alpha])
    return qml.probs(wires=wires)


probs = probability_circuit(params[0], params[1])


######################################################################
# Finally, we can display a bar graph showing the probability of
# measuring each bitstring:

plt.style.use("seaborn")
plt.bar(range(2 ** len(wires)), probs)
plt.show()


######################################################################
# The states
# :math:`|10\rangle \ = \ |1010\rangle` and
# :math:`|6\rangle \ = \ |0110\rangle` have the highest probabilities of
# being measured, just as expected!


pos = nx.spring_layout(graph)

plt.figure(figsize=(9, 4))
plt.subplot(121)
nx.draw(graph, pos, node_color=["r", "b", "r", "b"])
plt.subplot(122)
nx.draw(graph, pos, node_color=["b", "r", "r", "b"])
plt.show()

######################################################################
# TODO: Add example with Hamiltonian arithmetic
# TODO: Add conclusion
