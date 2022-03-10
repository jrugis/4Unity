# -*- coding: utf-8 -*-
#
# mat2bin_Duct.py

import numpy as np
import scipy.io as sc
import struct

uname = '4Unity_duct.bin'                 # binary output file
dname = 'dynamic_data/lumen_prop.mat'     # Matlab data input files
fname = 'dynamic_data/dynamic_flow.mat'   #

##################################################################
# functions
##################################################################

# write lumen line segments to bin file for unity
def write_lsegs(f, duct_prop):
  dcenters = duct_prop['lumen_prop']['disc_centres'][0,0]   # read in duct properties from matlab
  ndiscs = dcenters.shape[0]
  print("duct discs:", ndiscs)
  f.write(struct.pack('i', ndiscs))
  for p in dcenters:
    f.write(struct.pack('fff', p[0], p[1], p[2])) # write disc center coordinates
 
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
write_lsegs(f1, duct_prop)      # write duct disc data (binary)

# write flow data
flow = sc.loadmat(fname)
write_flow(f1, flow['dynamic_flow'])

f1.close()    # close binary file



