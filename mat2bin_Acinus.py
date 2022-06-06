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
nacinii = 14  # number of acinii
# **********************************

##################################################################
# main program
##################################################################

for n in range(nacinii):
  f = open("_4Unity_acinus_c" + str(n+1) + ".bin", 'wb') # create binary file for Unity
  ml = sc.loadmat("acinus_data/a" + str(n+1) + ".mat") # get acinus data (Matlab)
  #print('keys:', ml.keys())
  #print(ml['time_samples'].shape)
  #print(ml['xc'].shape)
  nnodes = ml['xp'].shape[0]  # number of nodes
  ntsteps = ml['xc'].shape[1] # number of timesteps
  print("cell_" + str(n+1) + "   " + str(nnodes) + " nodes, " + str(ntsteps)+ " timesteps" )

  f.write(struct.pack('i', nnodes))
  for p in ml['xp']:
    f.write(struct.pack('fff', p[0], p[1], p[2]))    # node coordinates

  f.write(struct.pack('i', ntsteps))
  for t in ml['time_samples'][0]:
    f.write(struct.pack('f', t))    # time at step

  for nc in ml['xc']:              # for each node...
    for c in nc:                   #   for each timestep.. 
      f.write(struct.pack('f', c)) #      write calcium value

  f.close()    # close binary file


