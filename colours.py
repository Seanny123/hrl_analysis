from __future__ import unicode_literals
import numpy as np
import matplotlib.pyplot as plt

def make_plot(data,fig,subplot):
    nphi,nt = data.shape
    phi_coords = np.linspace(0,np.pi*2,nphi+1) - np.pi/2.
    theta_coords = np.linspace(0,np.radians(35),nt+1)

    ax = fig.add_subplot(subplot,)
    ax.set_thetagrids((45,90,135,180,225,270,315,360),(9,12,15,18,21,24,3,6))
    ax.set_rgrids(np.arange(10,35,10),fmt='%s\u00b0')  

    theta,phi = np.meshgrid(phi_coords,theta_coords)
    quadmesh = ax.pcolormesh(theta,phi,data)
    ax.grid(True)
    fig.colorbar(quadmesh,ax=ax)
    return fig,ax


a = np.zeros((360,71)) + np.arange(360)[:,None]
b = np.random.random((360,71))
fig = plt.figure()
t1 = make_plot(a,fig,121)
t2 = make_plot(b,fig,122)
plt.show()