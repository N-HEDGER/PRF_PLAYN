import sys
import os
import popeye
import nilearn
from nilearn import surface
import numpy as np
from joblib import Parallel, delayed



# Get variables for current job
n_jobs=int(sys.argv[1])
HEM=sys.argv[2]
chunk=int(sys.argv[3])
outputpath=sys.argv[4]
stimdir=sys.argv[5]
datadir=sys.argv[6]

#os.environ["OMP_NUM_THREADS"] = "1"



print('Fitting data'+chunk+HEM)





# Get the stimulus.
import numpy as np

dm = np.load(os.path.join(stimdir,'design_matrix.npy'))

# put time dimension last for popeye
dm = np.moveaxis(dm,0,2)

# binarize
dm[dm<0.5] = 0
dm[dm>0.5] = 1

# remove fixation point
dm[49,88,:] = 0
dm[49,89,:] = 0
dm[50,88,:] = 0
dm[50,89,:] = 0

#revert y axis
dm = dm[::-1,:,:] # this is how popeye wants y dim (0 point is top of dm)

N_TIMEPOINTS = np.shape(dm)[2]

print('loaded stimulus')




# Get the data

import dill


def load(filename):
	input_file = open(filename, 'rb')
	obj = dill.load(input_file)
	return obj

def dill_save(obj,filename):
    with open(filename,'wb') as output:
        dill.dump(obj,output)


if HEM=='l':
	datatofit=os.path.join(datadir,'BIGLHEM.pkl')
elif HEM =='r':
	datatofit=os.path.join(datadir,'BIGRHEM.pkl')





data=load(datatofit)
print('loaded data'+datatofit)
print(data.shape)


vindex=[]

vindex=Parallel(n_jobs=n_jobs,verbose=1)(delayed(np.std)(meanvolL[:,fn])  for fn in range(data.shape[-1]))

stds=np.array(vindex)

idxs=np.squeeze(np.where(stds!=0))


splits=np.array_split(idxs, 100)


idx=splits[chunk]


print(str(len(idx)),'Vertices to fit')



# The model itself.

import ctypes, multiprocessing
import numpy as np
import sharedmem
import popeye.og_hrf as og
import popeye.utilities as utils
from popeye.visual_stimulus import VisualStimulus


TR = 1.5

stimulus = VisualStimulus(stim_arr = dm,viewing_distance = 225, screen_width =  69.84,scale_factor = 1,
                          tr_length = TR,
                          dtype = np.short)

model = og.GaussianModel(stimulus, utils.double_gamma_hrf)



# Define the grids and bounds.

grid_size = 4 

# X location grid
x_grid = (-10,10)

# Y location grid
y_grid = (-5,5)

# SD location grid. Here the minimum is set to 1 pixel. 
s_grid = (1/stimulus.ppd,10)

# This would seem to have to be the beta parameter?
b_grid = (0.1,1.0)

# This would seem to baseline parameter? (or alternatively hrf delay)
h_grid = (-1.0,1.0)


x_bound = (-50,50)

y_bound = (-50,50)

s_bound = (0.001, 10)

b_bound = (1e-8,None)

u_bound = (None,None)

h_bound = (-3.0,3.0)

## package the grids and bounds
grids = (x_grid, y_grid, s_grid, h_grid)

bounds = (x_bound, y_bound, s_bound, h_bound, b_bound, u_bound)




from joblib import Parallel, delayed

#from dask.distributed import Client
import joblib


import multiprocessing




from joblib import Parallel, delayed, parallel_backend

with parallel_backend("multiprocessing"):
	res=Parallel(n_jobs=n_jobs,verbose=200)(delayed(og.GaussianFit)(model,data[:N_TIMEPOINTS,vertex],grids,bounds,Ns=grid_size,verbose=0,voxel_index=(0,0,vertex),auto_fit=True)for vertex in idx)
  


dill_save(res,os.path.join(outputpath,chunk+HEM+'.pkl'))

print('Saved results for region'+ROI+HEM)




