# -*- coding: utf-8 -*-
#
# mat2HLbin_Calcium.py

import hdf5storage
import matplotlib.pyplot as plt
import numpy as np
import struct

import read_write as rw

##################################################################
# functions
##################################################################

def read_bin(fname):
  f1 = open(fname, 'rb') # open the binary file
  # get the vertices
  nverts = struct.unpack('i', f1.read(4))[0]
  verts = np.empty([nverts, 3])
  for i in range(nverts):
    verts[i] = struct.unpack('fff', f1.read(12))
  f1.close # close the binary file 
  return verts

# reduced nodes for hololens
def reduce_nodes(verts, tris):
  rvertsi = np.array([range(1, verts.shape[0]+1)], dtype=int) # all vert indices
  rvertsi = np.setdiff1d(rvertsi, tris) # remove surface tri indices
  rvertsi -= 1; # change to zero indexed
  nverts = 0.6 * verts # node reduction factor

  nverts = nverts - np.min(nverts, axis=0) # normalise all verts to non-negative 
  max = (np.max(nverts, axis=0)) # get the range of vertex values

  # create a 4D grid (as an array) for extracting a uniform spatial vertex subset
  # - stores distance to nearest vertex (dnv) and the associated vertex index at each grid point
  # - the integer parts of every vertex coordinate are used to index the grid 
  vgrid = np.zeros((np.concatenate((np.floor(max+1),[2])).astype(int)))
  toohigh = 1000000 # high dummy values for dnv and index
  vgrid.fill(toohigh) 

  ifverts = np.modf(nverts) # get the integer and fractional part of all nverts

  # iterate through rvertsi and store the vert that is closest to each (integer) grid point
  for i in rvertsi:
    dist = np.linalg.norm(ifverts[0][i])
    vgridi = (ifverts[1][i]).astype(int) # grid index is simply the vertex location integer part
    if dist > 0.5: # don't bother with grid points that have no close vertex
      continue
    noise = 0.3 * np.random.ranf() # some spatial dithering to break up an aligned visual
    dist += noise

    # is this vertex closest to the grid point?
    if dist < vgrid[vgridi[0]][vgridi[1]][vgridi[2]][0]: 
      vgrid[vgridi[0]][vgridi[1]][vgridi[2]][0] = dist # store the new closer distance
      vgrid[vgridi[0]][vgridi[1]][vgridi[2]][1] = i # update the associated vertex index

  # extract the close vertex indices
  cvi = vgrid[:,:,:,1]
  cvi = np.extract(cvi < toohigh, cvi)
  return cvi.astype(int)

# write for hololens vis data file
def write_4HL(fname, verts, c_data):
  f1 = open(fname, 'wb')
  f1.write(struct.pack('i', verts.shape[0]))
  for x in verts:
    f1.write(struct.pack('fff', x[0], x[1], x[2]))
  f1.write(struct.pack('i', c_data.shape[1]))
  for r in c_data:
    for c in r:
      f1.write(struct.pack('f', c))
  f1.close
  return

##################################################################
# main program
##################################################################

## read cell data and write hololens files
for cell_num in range(1,8):
  print
  print 'cell number: ', cell_num

  # read mesh file
  fname = 'meshes/4sim_out_N4_p3-p2-p4-' + str(cell_num) + 'tet.bin'
  print 'mesh file: ' + fname
  verts, tris, tets, dfa, dfb, apical, basal, common = rw.read_bin(fname)

  # reduce nodes for hololens
  idx = reduce_nodes(verts, tris)
  rverts = verts[idx]
  print 'vertex reduction:', verts.shape[0], '->', idx.shape[0]

  # read matlab data file
  dist_name = 'cells/Cell' + str(cell_num) + '.mat'
  print 'matlab data file: ' + dist_name 
  dist = hdf5storage.loadmat(dist_name)
  #print 'keys:', dist.keys()
  dist_key = 'c_tot'
  start = 640
  finish = 1307
  ca_data = dist[dist_key][0, 0][idx, start:finish]
  dims = ca_data.shape
  print 'time steps: ' + str(dims[1])
  min = ca_data.min()
  max = ca_data.max()
  print 'min:', '{:0.3f}'.format(min),
  print 'max:', '{:0.3f}'.format(max)

  # write hololens file
  fname = '4HL/4HL_Cell' + str(cell_num) + ".bin"
  print 'hololens data file: ' + fname 
  write_4HL(fname, rverts, (ca_data - min) / (max - min)) # range 0.0 to 1.0

  # plot
  max_row = np.argmax(np.max(ca_data, axis=1))
  plt.plot(np.transpose(ca_data[max_row, :]))

plt.show()


