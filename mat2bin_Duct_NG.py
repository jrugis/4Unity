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

# get lumen segment start and end indices (into discs)
def get_lidx(duct_prop):
  dsegs = duct_prop['lumen_prop']['d_s_Vec'][0,0][0]     # duct segment per disc (strange indexing!)
  lidx = np.zeros((dsegs[-1],2), dtype=int)              # final disc duct segment is the segment count
  s = 1  # previous segment number (Note: the first start index is already set to zero)
  for idx, seg in enumerate(dsegs):
    if seg != s:
      lidx[s,0bad_test] = idx        # start index
      lidx[s-1,1] = idx-1    # previous end index
      s = seg
  lidx[-1,1] = dsegs.shape[0] - 1 # final end index
  return lidx
  
# write lumen line segments to bin file for unity
def write_lsegs(f, lidx, duct_prop):
  dcenters = duct_prop['lumen_prop']['disc_centres'][0,0]   # read in duct properties from matlab
  dlengths = duct_prop['lumen_prop']['disc_length'][0,0][0] #     uses strange indexing!
  nsegs = lidx.shape[0]
  print("duct segments:", nsegs)
  f.write(struct.pack('i', nsegs))
  for i in range(nsegs):
    lvect = dcenters[lidx[i,0]+1] - dcenters[lidx[i,0]]          # segment direction vector
    pstart = dcenters[lidx[i,0]] - (0.5 * lvect)                 # segment start point 
    pend   = dcenters[lidx[i,1]] + (0.5 * dlengths[lidx[i,1]] * lvect) # segment end point
    f.write(struct.pack('fff', pstart[0], pstart[1], pstart[2])) # write start point
    f.write(struct.pack('fff', pend[0], pend[1], pend[2]))       # write end point
 
# write flow data to bin file for unity
def write_flow(f, lidx, flow):
  nsteps = flow.shape[0]
  print("timesteps:", nsteps)
  f.write(struct.pack('i', nsteps))
  fmax = np.max(flow)
  for time_step in flow:
    for idx in lidx:
      f.write(struct.pack('f', time_step[idx[1]] / fmax)) 
  return
  
##################################################################
# main program
##################################################################

f1 = open(uname, 'wb')                # create binary file for Unity

duct_prop = sc.loadmat(dname)         # get duct segment data (Matlab)
#print('keys:', duct_prop.keys())
#print(duct_prop['lumen_prop'].dtype)
lidx = get_lidx(duct_prop)            # get lumen segment start and end indices
write_lsegs(f1, lidx, duct_prop)      # write duct segment data (binary)

# write flow data
flow = sc.loadmat(fname)
write_flow(f1, lidx, flow['dynamic_flow'])

f1.close()    # close binary file



