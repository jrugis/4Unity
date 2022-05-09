# -*- coding: utf-8 -*-
#
# mat2bin_Duct.py

import numpy as np
import scipy.io as sc
import struct

uname = '_4Unity_duct.bin'                # binary output file
dname = 'dynamic_data/Lumen_prop.mat'     # Matlab data input files
fname = 'dynamic_data/dynamic_flow.mat'   #
cname = 'dynamic_data/dynamic_data.mat'   #

##################################################################
# globals
##################################################################

# ********* HARD CODED *************
ndisc = 191  # number of discs
ndvars = 6   #    "      disc vars: flow + 5x concentrations (Na, K, Cl, HCO, pH) 
ncell = 111  #    "      active cells
ncvars = 5   #    "      cell concentrations (Na, K, Cl, HCO, pH)                     
# **********************************

##################################################################
# functions
##################################################################

# convert H to pH
def H_pH(ml_c):
  for row in ml_c:
    for i in range(ndisc):
      idx = ncell*ncvars + i*(ndvars-1) + 4
      row[idx] = -np.log10(row[idx]/1000.0)

# write fixed duct data to bin file for unity
def write_fixed(f,  ml):
  ndiscs = ml['lumen_prop']['n_disc'][0,0][0,0]    # read in duct properties from matlab
  dcenters = ml['lumen_prop']['disc_centres'][0,0]   
  darea = ml['lumen_prop']['disc_X_area'][0,0][0]
  dleng = ml['lumen_prop']['disc_length'][0,0][0]
  dsegs = ml['lumen_prop']['d_s_Vec'][0,0][0]
  
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
def write_dynamic(f, ml_f, ml_c):
  nsteps = ml_f.shape[0]
  print("timesteps:", nsteps)
  f.write(struct.pack('i', nsteps))       # number of time steps
  # ********* HARD CODED *************
  f.write(struct.pack('ii', 0, 4000))     # stimulation ON / OFF time steps
  # **********************************

  for i in range(nsteps):
    # ********* HARD CODED *************
    if i <= 5000: t = i * 0.1    #  5000 steps with 0.1s period
    else: t = 500.0 + (i - 5000) #  remaining steps with 1s period
    # **********************************
    f.write(struct.pack('f', t))          # simulation time at each step   

  f.write(struct.pack('i', (ndisc * ndvars) + (ncell * ncvars))) # total number of simulated values

  # minimum and maximum dynamic values
  for n in range(ncvars):
    #f.write(struct.pack('f', ml_c[:,n:ncvars*ncell:ncvars].min()))  # minimum cell concentrations
    a = ml_c[:,n:ncvars*ncell:ncvars]         # minimum cell concentrations 
    f.write(struct.pack('f', a[a!=0].min()))  # skip "dead" cells
  f.write(struct.pack('f', ml_f.min()))                                # minimum flow value
  for n in range(ndvars-1):
    f.write(struct.pack('f', ml_c[:,ncvars*ncell+n::ndvars-1].min()))  # minimum disc concentrations
  for n in range(ncvars):
    f.write(struct.pack('f', ml_c[:,n:ncvars*ncell:ncvars].max()))  # maximum cell concentrations
  f.write(struct.pack('f', ml_f.max()))                                # maximum flow value
  for n in range(ndvars-1):
    f.write(struct.pack('f', ml_c[:,ncvars*ncell+n::ndvars-1].max()))  # maximum disc concentrations
  
  # for each time step...
  for df, dc in zip(ml_f, ml_c):   
    for val in df: 
      f.write(struct.pack('f', val))     # write flow data
    for val in dc: 
      f.write(struct.pack('f', val))     # write concentration data
  return
  

##################################################################
# main program
##################################################################

f1 = open(uname, 'wb')         # create binary file for Unity

ml = sc.loadmat(dname)         # get duct disc data (Matlab)
#print('keys:', ml.keys())
#print(ml['lumen_prop'].dtype)
write_fixed(f1, ml)      # write fixed duct data (binary)

# write dynamic data
ml_flow = sc.loadmat(fname)  # disc flow rates
ml_conc = sc.loadmat(cname)  # cell and disc concentrations
#print('keys:', ml_conc.keys())
#print(ml_conc['zzzz'].dtype)
#print(ml_conc['zzzz'].shape)
#H_pH(ml_conc['dynamic_data']) # convert H to pH
#print('keys:', ml_flow.keys())
#rint(ml_flow['flowrate'].dtype)
#rint(ml_flow['flowrate'].shape)
write_dynamic(f1, ml_flow['flowrate'], ml_conc['zzzz'])

f1.close()    # close binary file



