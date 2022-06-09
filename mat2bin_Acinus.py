# -*- coding: utf-8 -*-
#
# mat2bin_Acinus.py

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sc
import struct

##################################################################
# globals
##################################################################

# ********* HARD CODED *************
ncells = 14  # number of acinii
# **********************************

##################################################################
# main program
##################################################################

f = open("_4Unity_acinus.bin", 'wb') # create binary file for Unity

nnodes = 0 
for c in range(ncells): # for each cell...
  ml = sc.loadmat("acinus_data/a" + str(c+1) + ".mat") # get acinus data (Matlab)
  #print('keys:', ml.keys())
  #print(ml['time_samples'].shape)
  #print(ml['xc'].shape)
  nnodes += ml['xp'].shape[0] # number of nodes
print("nodes: " + str(nnodes))
f.write(struct.pack('i', nnodes))

ntsteps = ml['xc'].shape[1] # number of timesteps (same for all cells)
print("timesteps: " + str(ntsteps))
f.write(struct.pack('i', ntsteps))

for c in range(ncells): # for each cell...
  ml = sc.loadmat("acinus_data/a" + str(c+1) + ".mat") # get acinus data (Matlab)
  for p in ml['xp']:                               #   for each node...
    f.write(struct.pack('fff', p[0], p[1], p[2]))  #     write node coordinates

for t in ml['time_samples'][0]: # for each timestep...
  f.write(struct.pack('f', t))  #   write time at step (same for all cells)

C = np.empty(0)
for c in range(ncells): # for each cell...
  ml = sc.loadmat("acinus_data/a" + str(c+1) + ".mat") # get acinus data (Matlab)
  C = np.append(C, ml['xc'])
C = np.transpose(np.reshape(C,(nnodes,ntsteps)))

for row in C:                    # for each timestep...
  for col in row:                #   for each node.. 
    f.write(struct.pack('f', col)) #     write calcium value

f.close()    # close binary file

plt.plot(ml['time_samples'][0], C[:,0])
plt.show()
