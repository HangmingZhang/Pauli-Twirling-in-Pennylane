#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pennylane as qml
from pennylane import numpy as np
import itertools


# In[2]:


class PauliTwirling:
    def __init__(self, n_qubits):
        self.n_qubits = n_qubits
    
    def twirlinglayer(self, measurements_str: str, pauli_op_n_qubits: list,
                      noise_channel: "qml.QubitChannel function", channel_paras, channel_wires,
                      circuit: "function", *args, **kwargs):
        # channel_paras: it could be a float when the noise_channel is defined by qml.AmplitudeDamping
        # or a list when the noise_channel is defined by qml.QubitChannel.
        # *args, **kwargs: parameters of circuit.
        
        measurements_split = list(measurements_str)
        
        measurements = self.__save_measurements(measurements_split)
        
        circuit(*args, **kwargs)
        
        # Here’s the direct implementation of the Pauli twirling method
        # —it’s based on the mathematical formulation itself
        # and may differ slightly from practical approaches.
        # However, our main goal here is to use the code
        # to verify the mathematical principles behind Pauli twirling.
        
        self.__add_twirling_layer(pauli_op_n_qubits)
        
        noise_channel(channel_paras, channel_wires)
        
        self.__add_twirling_layer(pauli_op_n_qubits)
        
        return qml.expval(self.__create_measurement_ops(measurements))
    
    def paulitwirling(self, dev: "qml.device for paulitwirling", measurements_str: str,
                     noise_channel: "qml.QubitChannel function", channel_paras, channel_wires,
                      circuit: "function", *args, **kwargs):
        twirled_expectation_value_lst = []
        pauli_ops_n_qubits = self.__get_pauli_ops_n_qubits()
        
        for pauli_op_n_qubits in pauli_ops_n_qubits:
            e = qml.QNode(self.twirlinglayer, dev)(measurements_str, pauli_op_n_qubits,
                                            noise_channel, channel_paras, channel_wires,
                                            circuit, *args, **kwargs)
            twirled_expectation_value_lst.append(e)
            
        e = np.mean(twirled_expectation_value_lst)
        return e
    
       
    def __save_measurements(self, measurements_split):
        measurements = []
        for i, measurement_str in enumerate(measurements_split):
            if measurement_str == "I":
                continue
            elif measurement_str == "X":
                measurements.append(qml.PauliX(i))
            elif measurement_str == "Y":
                measurements.append(qml.PauliY(i))
            elif measurement_str == "Z":
                measurements.append(qml.PauliZ(i))
            else:
                raise ValueError("measurements_str can only be 'I', 'X', 'Y' or 'Z'.")
        return measurements
    
    def __create_measurement_ops(self, measurements):
        measurement_ops = measurements[0]
        for i in range(1, len(measurements)):
            measurement_ops = measurement_ops @ measurements[i]
        return measurement_ops
    
    
    def __get_pauli_ops_n_qubits(self):
        pauli_ops = ["I", "X", "Y", "Z"]
        pauli_ops_n_qubits = list(itertools.product(pauli_ops, repeat=self.n_qubits))
        return pauli_ops_n_qubits
    
    def __add_twirling_layer(self, pauli_op_n_qubits):
        for i, pauli_op in enumerate(pauli_op_n_qubits):
            if pauli_op == "I":
                qml.Identity(wires=i)
                
            elif pauli_op == "X":
                qml.PauliX(wires=i)
                    
            elif pauli_op == "Y":
                qml.PauliY(wires=i)
                    
            elif pauli_op == "Z":
                qml.PauliZ(wires=i)
                
            else:
                print("Unexpected error!")


# In[ ]:


# Great! We've successfully written the code for Pauli twirling.
# But how does one know if our code is correct?
# Next, we'll verify the correctness of the code from two aspects.

