# -*- coding: utf-8 -*-
#
# mat2bin_Duct.py

import matplotlib.cm as mp
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sc
import struct

#import read_write as rw

##################################################################
# functions
##################################################################

# write duct lumen disc values
def write_disc(f, vals):
  f.write(struct.pack('i', vals.shape[0]))    # number of vals
  for val in vals:
    f.write(struct.pack('fff', val[0], val[1], val[2]))
  return

# write lumen line segments to hololens file
#def write_lsegs_4HL(f, lsegs):
#  f.write(struct.pack('i', lsegs.shape[0]))                      # segment count
#  for seg in lsegs:
#    f.write(struct.pack('fff', seg[0][0], seg[0][1], seg[0][2])) # start point
#    f.write(struct.pack('fff', seg[1][0], seg[1][1], seg[1][2])) # end point
#  return

# write lumen flow data to hololens file
#def write_fdata_4HL(start, finish, stride, f, fdata):
#  count = fdata[0][0][start:finish:stride].shape[0] # time step count     
#  print 'time steps:', count
#  min = fdata[37][0][start:finish:stride].min() # HARD CODED TO EXIT SEGMENT!!!
#  max = fdata[37][0][start:finish:stride].max() # HARD CODED TO EXIT SEGMENT!!!
#  #print 'data min/max:', min, max
#  f.write(struct.pack('i', count))
#  for seg in fdata:
#    trim = seg[0][start:finish:stride] / max
#    #print trim.max()
#    for t in trim:
#      f.write(struct.pack('f', t))                  # flow rate (per segment)
#  return

##################################################################
# main program
##################################################################

uname = '4Unity_duct.bin'
dname = 'dynamic_data/lumen_prop.mat'
print()

# create binary file for Unity
f1 = open(uname, 'wb')
print('       Unity duct data file: ' + uname)

# convert and write duct lumen disc data
print('Matlab duct properties file: ' + dname)
duct_prop = sc.loadmat(dname)
#print('keys:', duct_prop.keys())
#print(duct_prop['lumen_prop'].dtype)
write_disc(f1, duct_prop['lumen_prop']['disc_centres'][0,0])




# write lumen tree data
#write_lsegs_4HL(f1, rw.read_lumen(tname))

# write flow data
#print 'matlab data file: ' + fname
#dist = sc.loadmat(fname)
##print 'keys:', dist.keys()
#write_fdata_4HL(9500, 30840, 32, f1, dist[dist_key])
#plt.plot(dist[dist_key][37, 0][9500:30840:32])
#plt.show()

# close binary file
f1.close()
print()


