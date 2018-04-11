import numpy as np
import pylab as pl

import sys
sys.path.insert(0, '../src/susceptibility_tensor')
sys.path.insert(0, '../build')
from susceptibility_interpolator import chi_ij, chi_ij_integrand
import susceptibility_tensor.susceptibilityPy as susp

#try to prevent SSH logoff from stopping plot
#import matplotlib
#matplotlib.use('Agg')

# Set plot parameters to make beautiful plots
pl.rcParams['figure.figsize']  = 12, 7.5
pl.rcParams['lines.linewidth'] = 1.5
pl.rcParams['font.family']     = 'serif'
pl.rcParams['font.weight']     = 'bold'
pl.rcParams['font.size']       = 20  
pl.rcParams['font.sans-serif'] = 'serif'
#pl.rcParams['text.usetex']     = True
pl.rcParams['axes.linewidth']  = 1.5
pl.rcParams['axes.titlesize']  = 'medium'
pl.rcParams['axes.labelsize']  = 'large'

pl.rcParams['xtick.major.size'] = 8     
pl.rcParams['xtick.minor.size'] = 4     
pl.rcParams['xtick.major.pad']  = 8     
pl.rcParams['xtick.minor.pad']  = 8     
pl.rcParams['xtick.color']      = 'k'     
pl.rcParams['xtick.labelsize']  = 'large'
pl.rcParams['xtick.direction']  = 'in'    

pl.rcParams['ytick.major.size'] = 8     
pl.rcParams['ytick.minor.size'] = 4     
pl.rcParams['ytick.major.pad']  = 8     
pl.rcParams['ytick.minor.pad']  = 8     
pl.rcParams['ytick.color']      = 'k'     
pl.rcParams['ytick.labelsize']  = 'large'
pl.rcParams['ytick.direction']  = 'in'


# In[3]:

#define constants
epsilon0  = 1./(4. * np.pi)
e         = 4.80320680e-10
m         = 9.1093826e-28
c         = 2.99792458e10
epsilon   = -1.

def nu_c(magnetic_field):
    ans = e * magnetic_field / (2. * np.pi * m * c)
    return ans

nuratio = np.logspace(1., 3., 10)

from mpi4py import MPI

comm = MPI.COMM_WORLD
size=comm.Get_size()
rank=comm.Get_rank()

angles = [5, 15, 25, 35, 45, 55, 65, 75, 85]

#save data for plots

B = 1.
n_e = 1.
nu = nuratio * nu_c(B)
theta = 60. * np.pi/180.
theta_e = 10.
p = 3.
gamma_min = 1.
gamma_max = 1000.
gamma_cutoff = 1e10
kappa = 3.5
w = 10.
component = 22
dist = 1
real_part = 1

#nu = 10.*nu_c(B)

#print nu_c(B)
#
#print 'setup done'
#interp = chi_ij(nu, B, n_e, theta, dist, real_part, theta_e, p, gamma_min, gamma_max, gamma_cutoff, kappa, w, component)
#print 'interp done'
#integrated = susp.chi_12_symphony_py(nu, B, n_e, theta, dist, real_part, theta_e, p, gamma_min, gamma_max, gamma_cutoff, kappa, w)
#
#print 'interp    :', interp
#print 'integrated:', integrated
#print 'error     :', np.abs((interp - integrated)/integrated)

spline = np.vectorize(chi_ij)(nu, B, n_e, theta, dist, real_part, theta_e, p, gamma_min, gamma_max, gamma_cutoff, kappa, w, component)
integrated = np.vectorize(susp.chi_22_symphony_py)(nu, B, n_e, theta, dist, real_part, theta_e, p, gamma_min, gamma_max, gamma_cutoff, kappa, w)
error = np.abs((spline - integrated)/integrated)

np.savetxt('chi_22_real_' + '60' + 'deg_PL_error.txt', error)

#np.savetxt('chi_11_real_' + str(angles[rank]) + 'deg_error.txt', error)

#produce plots

#print chi_ij_integrand(1., 1., theta, dist, real_part, component, theta_e, p, gamma_min, gamma_max, gamma_cutoff, kappa, w)

#gamma = np.linspace(1., 10., 10000)
#pl.plot(gamma, np.vectorize(chi_ij_integrand)(gamma, 100., theta, dist, real_part, component, theta_e, p, gamma_min, gamma_max, gamma_cutoff, kappa, w))
#pl.show()

#error = np.loadtxt('chi_11_real_60deg_PL_error.txt')
#pl.loglog(nuratio, error)
#pl.show()
