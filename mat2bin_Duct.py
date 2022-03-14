# -*- coding: utf-8 -*-
#
# mat2bin_Duct.py

import numpy as np
import scipy.io as sc
import struct

uname = '_4Unity_duct.bin'                 # binary output file
dname = 'dynamic_data/lumen_prop.mat'     # Matlab data input files
fname = 'dynamic_data/dynamic_flow.mat'   #

##################################################################
# functions
##################################################################

# write duct disc data to bin file for unity
def write_discs(f, duct_prop):
  ndiscs = duct_prop['lumen_prop']['n_disc'][0,0][0,0]    # read in duct properties from matlab
  dcenters = duct_prop['lumen_prop']['disc_centres'][0,0]   
  darea = duct_prop['lumen_prop']['disc_X_area'][0,0][0]
  dleng = duct_prop['lumen_prop']['disc_length'][0,0][0]
  dsegs = duct_prop['lumen_prop']['d_s_Vec'][0,0][0]
  print(dleng)
  
  dvects = np.zeros((ndiscs,3))  # calculate disc direction vectors
  s = 0                                   # previous duct segment
  for i in range(ndiscs):
    if dsegs[i] != s:                     # moved to next duct segment?   
      dvect = dcenters[i+1] - dcenters[i] # use first two segments points for direction 
      s = dsegs[i]
    dvects[i] = dvect                     # same direction for all discs in each segment 

  print("duct discs:", ndiscs)
  f.write(struct.pack('i', ndiscs))                     # number of discs
  for v in dcenters:
    f.write(struct.pack('fff', v[0], v[1], v[2]))       # disc center coordinates
  for x in darea:
    f.write(struct.pack('f', 2.0 * np.sqrt(x / np.pi))) # disc diameters
  for x in dleng:
    f.write(struct.pack('f', x))                        # disc lengths
  for v in dvects:
    f.write(struct.pack('fff', v[0], v[1], v[2]))       # disc direction vectors

# write flow data to bin file for unity
def write_flow(f, flow):
  nsteps = flow.shape[0]
  print("timesteps:", nsteps)
  f.write(struct.pack('i', nsteps))
  fmax = np.max(flow)
  for time_step in flow:
    for df in time_step:   # disc flow
      f.write(struct.pack('f', df / fmax)) 
  return
  
##################################################################
# main program
##################################################################

f1 = open(uname, 'wb')                # create binary file for Unity

duct_prop = sc.loadmat(dname)         # get duct disc data (Matlab)
#print('keys:', duct_prop.keys())
#print(duct_prop['lumen_prop'].dtype)
write_discs(f1, duct_prop)      # write duct disc data (binary)

# write flow data
flow = sc.loadmat(fname)
write_flow(f1, flow['dynamic_flow'])

f1.close()    # close binary file



