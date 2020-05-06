from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import scipy.fftpack as sfft
import random
import imageio
import cv2
from pylab import *
from mpl_toolkits.mplot3d import Axes3D

def epsilon(u_int, target_im):
    max = np.max(u_int[target_im==1]) #Max value of the obtained intensity at the tweezers position
    min = np.min(u_int[target_im==1]) #Min value of the obtained intensity at the tweezers position
    error = (max-min)/(max+min)
    print("Error :", error)
    return error

def join_phase_ampl(phase,ampl):
    tmp=np.zeros((ampl.shape[0],ampl.shape[1]),dtype=complex)
    for a in range(0,ampl.shape[0]):
        for b in range(0,ampl.shape[1]):
            tmp[a,b] = ampl[a,b]*np.exp(phase[a,b]*1.j)

    return tmp

def Beam_shape(sizex,sizey,sigma,mu):
    x, y = np.meshgrid(np.linspace(-1,1,sizex), np.linspace(-1,1,sizey))
    d = np.sqrt(x*x+y*y)
    g = np.exp(-( (d-mu)**2 / ( 2.0 * sigma**2 ) ) )
    return g

def surface_plot (matrix, **kwargs):
    # acquire the cartesian coordinate matrices from the matrix
    # x is cols, y is rows
    (x, y) = np.meshgrid(np.arange(matrix.shape[0]), np.arange(matrix.shape[1]))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, matrix, **kwargs)
    return (fig, ax, surf)

def norm(matrix):
    min=np.min(matrix);max=np.max(matrix);
    return((matrix-min)/(max-min))

def bin_norm_clip(matrix):  # Function that clips the values to 0-255 (SLM standard)
    matrix=np.array(target_im, dtype=np.uint8)
    matrix=norm(matrix)
    return(matrix)


def weights(w,target_im,w_prev,std_int): # This weight function works only where the intensity == 1 (discrete tweezers)
    w[target_im==1] = ((target_im[target_im==1] / std_int[target_im==1]) ** 0.5) * w_prev[target_im==1]
    return (w)

def discretize_phase(phase):
    phase=np.round((phase+np.pi)*255/(2*np.pi))
    return(phase)

def undiscretize_phase(phase):
    phase=phase/255*(2*np.pi)-np.pi
    return(phase)

target_im = Image.open("Img/point-13_100x100.bmp")
target_im=norm(target_im)   # Image in intensity units [0,1]
SIZE_X,SIZE_Y=target_im.shape
plt.imshow(target_im)
plt.colorbar()
plt.show()

# The initial weights are all = 1.
w=np.ones((SIZE_X,SIZE_Y))
# The amplitude in the fourier plane is a Gaussian (beam)
PS_shape=Beam_shape(SIZE_X,SIZE_Y,255,0)
#plt.imshow(PS_shape)
#plt.colorbar()
#plt.show()'''
# Previous weights (setting it = the image we obtain a total weight of 1 at the first iteration)
w_prev=target_im  ## Weights of the previous step (for the first one is just the amplitude of the target)
# General initializzations
errors=[]
u=np.zeros((SIZE_X,SIZE_Y),dtype=complex)
# Random phase at the first iteration
phase=2*np.pi*np.random.rand(SIZE_X,SIZE_Y)-np.pi

for rep in range(30):
    # Fourier plane, random phase (at the round 1) and gaussian beam
    u=join_phase_ampl(phase,PS_shape.T)
    # To the real plane...
    u = sfft.fft2(u)
    u = sfft.fftshift(u)
    # Calculate the intensity
    int=np.square(np.abs(u))
    # Let's renormalize the intensity in the range [0,1]
    std_int=norm(int)
    # What's the distance from the target intensity?
    errors.append(epsilon(std_int, target_im))
    phase=np.angle(u)
    ## Here I don't care about the discretization of the phase because we're in real space (that is actually the fourier plane for the code)
    #Generate weights and use them to obtain u
    w=weights(w,target_im,w_prev,std_int)
    w=norm(w)
    w_prev=w
    u=join_phase_ampl(phase,w)
    # Back to our fourier plane
    u = sfft.ifftshift(u)
    u = sfft.ifft2(u)
    # The phase that we need to imprint by the SLM is :
    phase=np.angle(u)
    # This part discretizes the values of phase. The SLM can only produce values in the range [0,255]
    # that corresponds to [0,2pi]. Some values (e.g. 0.5 => 0.5 * 2pi/255) cannot be reproduced by the SLM
    # This discretization takes that in account. (The final phase will be the discretized one)
    phase=discretize_phase(phase)
    Final_ampl_phase=phase
    phase=undiscretize_phase(phase)


plt.imshow(std_int)
plt.colorbar()
plt.show()
plt.imshow(Final_ampl_phase)
plt.colorbar()
plt.show()