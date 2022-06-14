import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sc
import struct
import mayavi.mlab as mv

ml = sc.loadmat("acinus_data/a1.mat")

t = ml['time_samples'][0]
c = np.transpose(ml['xc'])
p = ml['xp']

t.shape
c.shape
p.shape

plt.plot(t, c[:,:201]);
plt.show()

plt.plot(t, c[:,201:402]);
plt.show()

plt.plot(t, c[:,[0,201,402]]);
plt.show()


np.count_nonzero(c==0) # has value 0

mv.points3d(p[:,0],p[:,1],p[:,2], scale_factor=.5); # all points

pp = p[np.where(c==0)[1]]
mv.points3d(pp[:,0],pp[:,1],pp[:,2], scale_factor=.5);  # 0 value points