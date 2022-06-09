# -*- coding: utf-8 -*-
#
# mat2bin_Acinus.py

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
for c in range(ncells):
  ml = sc.loadmat("acinus_data/a" + str(c+1) + ".mat") # get acinus data (Matlab)
  #print('keys:', ml.keys())
  #print(ml['time_samples'].shape)
  print(ml['xc'].shape)
  nnodes += ml['xp'].shape[0] # number of nodes
print("nodes: " + str(nnodes))
f.write(struct.pack('i', nnodes))

ntsteps = ml['xc'].shape[1] # number of timesteps (same for all cells)
print("timesteps: " + str(ntsteps))
f.write(struct.pack('i', ntsteps))

for c in range(ncells):                                # for each cells...
  ml = sc.loadmat("acinus_data/a" + str(c+1) + ".mat") # get acinus data (Matlab)
  for p in ml['xp']:                               #   for each node...
    f.write(struct.pack('fff', p[0], p[1], p[2]))  #     write node coordinates

for t in ml['time_samples'][0]: # for each timestep...
  f.write(struct.pack('f', t))  #   write time at step (same for all cells)

for c in range(ncells):            # for each cell...
  ml = sc.loadmat("acinus_data/a" + str(c+1) + ".mat") # get acinus data (Matlab)
  for ts in np.transpose(ml['xc']):  #   for each timestep...
    for n in ts:                     #      for each node.. 
      f.write(struct.pack('f', n))   #         write calcium value

f.close()    # close binary file


